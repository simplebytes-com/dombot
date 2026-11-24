#!/usr/bin/env python3
"""Reconcile exported DD sale terms through DomBot's supported API.

Default is a read-only plan. --apply requires exact date/amount matches,
backs up the current bundle, edits existing event IDs, then verifies read-back.
Source files, cookies and output belong outside Git.
"""
import argparse
import csv
import json
import subprocess
from datetime import datetime
from decimal import Decimal
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--url', required=True)
    p.add_argument('--cookie-file', type=Path, required=True)
    p.add_argument('--sales-csv', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    args.output.mkdir(mode=0o700, parents=True, exist_ok=True)
    base = args.url.rstrip('/')

    def call(method, values):
        result = subprocess.run([
            'curl', '--fail-with-body', '-sS', '--max-time', '120',
            '-b', str(args.cookie_file), '-H', 'Content-Type: application/json',
            '-H', 'Origin: ' + base, '--data-binary', '@-', base + '/api/' + method,
        ], input=json.dumps({'args': values}), text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(f'{method} failed: {result.stdout[:200]}')
        data = json.loads(result.stdout)
        if 'error' in data:
            raise RuntimeError(data['error'])
        return data['result']

    def save(name, value):
        target = args.output / name
        target.write_text(json.dumps(value, indent=2))
        target.chmod(0o600)

    before = json.loads(call('exportData', []))
    ns = before['namespaces']
    notes = {n['domain']: n['text'] for n in ns['domain-notes'].values() if n['eventId'] is None}
    plan = []
    rows = list(csv.DictReader(args.sales_csv.open()))
    seen = set()
    for row in rows:
        domain = row['domain_domain'].strip().lower()
        if domain in seen:
            raise ValueError('Duplicate source sale: ' + domain)
        seen.add(domain)
        source_day = datetime.strptime(' '.join(row['saleDate'].split()[:4]), '%a %b %d %Y').date().isoformat()
        matches = [e for e in ns['domain-events'].values()
                   if e['type'] == 'sold' and e['domain'] == domain
                   and e['date'] == source_day
                   and Decimal(e['amount']) == Decimal(row['salePrice'])]
        if len(matches) != 1:
            raise ValueError('Expected exactly one matching sale: ' + domain)
        event = matches[0]
        if event['currency'] != 'USD':
            raise ValueError('Source export is USD, current sale is not: ' + domain)
        gross, net = Decimal(row['salePrice']), Decimal(row['priceAfterCommission'])
        fees = gross - net
        if fees < 0 or fees > gross:
            raise ValueError('Invalid source fee/net: ' + domain)
        rate_fee = (gross * Decimal(row['commissionPercentage']) / 100).quantize(Decimal('.01'))
        if abs(fees - rate_fee) > Decimal('.01'):
            raise ValueError('Source commission and net disagree: ' + domain)
        terms = {
            'platform': row['platform'], 'method': row['method'],
            'paymentStatus': 'unconfirmed',
            'monthlyAmount': row['ltoMonthlyPrice'] or None,
            'termMonths': int(row['ltoTermMonths']) if row['ltoTermMonths'] else None,
        }
        if event.get('fees') is not None and Decimal(event['fees']) != fees:
            raise ValueError('Current fees differ; manual reconciliation needed: ' + domain)
        if event.get('saleImport') is not None and event['saleImport'] != terms:
            raise ValueError('Current import terms differ: ' + domain)
        update = {
            'domainName': domain, 'eventId': event['id'],
            'saleDate': event['date'], 'amount': event['amount'],
            'currency': event['currency'], 'fees': str(fees.quantize(Decimal('.01'))),
            'saleImport': terms, 'notes': notes.get(domain, ''),
        }
        plan.append({'eventId': event['id'], 'update': update,
                     'changes': event.get('saleImport') != terms or event.get('fees') is None})
    save('plan.json', plan)
    if args.apply:
        # Do not overwrite the original recovery snapshot on an idempotent retry.
        if not (args.output / 'before-bundle.json').exists():
            save('before-bundle.json', before)
        for item in plan:
            if item['changes']:
                call('setSale', [item['update']])
        after = json.loads(call('exportData', []))
        save('after-bundle.json', after)
        for item in plan:
            actual = after['namespaces']['domain-events'][item['eventId']]
            assert Decimal(actual['fees']) == Decimal(item['update']['fees'])
            assert actual['saleImport'] == item['update']['saleImport']
        changed_ids = {item['eventId'] for item in plan}
        for event_id, event in ns['domain-events'].items():
            actual = after['namespaces']['domain-events'][event_id]
            if event_id not in changed_ids:
                assert actual == event, event_id
            else:
                for key in set(event) - {'updatedAt', 'fees', 'saleImport'}:
                    assert actual.get(key) == event[key], (event_id, key)
        assert len(after['namespaces']['domain-events']) == len(ns['domain-events'])
        for name in ['domain-notes', 'registrar-accounts', 'registrar-credentials',
                     'domain-for-sale', 'domain-list-prices', 'imported-domains']:
            assert after['namespaces'][name] == ns[name], name
    summary = {'applied': args.apply, 'sales': len(plan),
               'changes': sum(item['changes'] for item in plan),
               'installmentContracts': sum(r['method'] == 'LTO' for r in rows),
               'grossContractValue': str(sum(Decimal(r['salePrice']) for r in rows)),
               'netContractValue': str(sum(Decimal(r['priceAfterCommission']) for r in rows)),
               'confirmedReceipts': None}
    save('summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Prepare, never apply, a DD CSV migration against a Dombot snapshot.

Usage: prepare-dd-migration.py DOMAINS.csv SALES.csv BEFORE.json APPRAISALS.json OUTDIR
Inputs and outputs contain private portfolio data: keep them outside Git.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path


def main():
    domains_path, sales_path, before_path, appraisals_path, out_path = map(Path, sys.argv[1:])
    out_path.mkdir(mode=0o700, parents=True, exist_ok=True)
    domains = list(csv.DictReader(domains_path.open()))
    sales = list(csv.DictReader(sales_path.open()))
    before = json.loads(before_path.read_text())['result']['domains']
    synced = {d['domainName'].lower(): d for d in before}
    appraisals = defaultdict(list)
    for a in json.loads(appraisals_path.read_text()):
        appraisals[a[0].lower()].append(a)
    sale_by_name = {s['domain_domain'].lower(): s for s in sales}
    assert len(sale_by_name) == len(sales), 'Multiple sales per name need manual mapping'
    assert len({d['Domain'].lower() for d in domains}) == len(domains), 'Duplicate domain rows'
    assert not any(d['Status'] in ('sold', 'dropped') and d['Domain'].lower() in synced for d in domains), 'Archive status conflicts with live registrar'
    assert {d['Domain'].lower() for d in domains if d['Status'] == 'sold'} == set(sale_by_name), 'Sold records and sales export differ'
    rows = []
    for line, d in enumerate(domains, 2):
        name = d['Domain'].lower().strip()
        status = d['Status']
        assert status in ('owned', 'atom', 'broker', 'sold', 'dropped'), status
        row = {'line': line, 'domain': name, 'status': status if status in ('sold', 'dropped') else 'owned'}
        if status in ('atom', 'broker'):
            row['folder'] = {'atom': 'Atom', 'broker': 'Broker'}[status]
        purchase = {'date': d['Ownership Date']}
        if d['Acquisition Price'] and Decimal(d['Acquisition Price']) > 0:
            purchase.update(amount=d['Acquisition Price'], currency='USD')
        # Do not infer registration vs aftermarket purchase from price alone.
        if 'hand reg' in d['Notes'].lower():
            purchase['type'] = 'registered'
        row['purchase'] = purchase
        if name not in synced and status not in ('sold', 'dropped'):
            registration = {}
            known = {'GoDaddy.com, LLC': 'godaddy', 'Spaceship, Inc.': 'spaceship', 'Dynadot Inc': 'dynadot', 'Porkbun LLC': 'porkbun', 'NameCheap, Inc.': 'namecheap'}
            registrar = d['Registrar']
            if registrar in known:
                registration['registrar'] = known[registrar]
            elif registrar:
                registration['registrarLabel'] = registrar
            for source, dest in [('Registration Date', 'createdDate'), ('Expiration Date', 'expirationDate')]:
                if d[source]:
                    registration[dest] = d[source]
            row['registration'] = registration
            # Keep live registrar renewal estimates authoritative for synced names.
            if d['Renewal Price'] and Decimal(d['Renewal Price']) > 0:
                row['renewal'] = {'amount': d['Renewal Price'], 'currency': 'USD'}
        prices = {}
        for source, dest in [('Buy Now Price', 'amount'), ('Min Offer', 'minOffer'), ('Floor Price', 'floor')]:
            if d[source] and Decimal(d[source]) > 0:
                amount = Decimal(d[source])
                assert amount == int(amount), f'Fractional asking price: {name}'
                prices[dest] = str(int(amount))
        if 'amount' in prices:
            assert all(int(prices[k]) <= int(prices['amount']) for k in ('minOffer', 'floor') if k in prices), f'Inconsistent prices: {name}'
        if prices:
            row['listPrice'] = dict(prices, currency='USD')
        notes = [d['Notes'].strip()] if d['Notes'].strip() else []
        notes.append('[DD snapshot 2026-10-15; amounts USD; historical data, not live quotes]')
        notes.append('DD status: ' + status)
        if d['Display Name'] and d['Display Name'] != name:
            notes.append('Display name: ' + d['Display Name'])
        for field in ('Auction Date', 'Renewal Price', 'GD Estimated Value', 'GOD Value', 'Estibot Value', 'Average Value', 'Break Even', 'Hold Time Years', 'Total Renewal Cost'):
            if d[field]:
                notes.append(field + ': ' + d[field])
        if d['Registrar']:
            notes.append('DD registrar: ' + d['Registrar'])
        if d['NS1'] or d['NS2']:
            notes.append('DD nameservers: ' + '; '.join(filter(None, (d['NS1'], d['NS2']))))
        if name in synced:
            for source, dest in [('Registration Date','createdDate'),('Expiration Date','expirationDate')]:
                if d[source] and d[source] != (synced[name].get(dest) or '')[:10]:
                    notes.append('DD ' + source + ': ' + d[source] + ' (live registrar retained)')
        if status == 'dropped':
            notes.append('Actual drop date not supplied by DD; archive event date is migration date.')
        sale = sale_by_name.get(name)
        if sale:
            date = datetime.strptime(' '.join(sale['saleDate'].split()[:4]), '%a %b %d %Y').date().isoformat()
            row['sale'] = {'date': date, 'amount': format(Decimal(sale['salePrice']), 'f'), 'currency': 'USD'}
            notes.append('DD sale details: ' + '; '.join(k + '=' + sale[k] for k in ('platform','method','commissionPercentage','priceAfterCommission','ltoMonthlyPrice','ltoTermMonths','notes') if sale[k]))
            if sale['method'] == 'LTO':
                notes.append('Sale amount is contract total, not verified cash received; installment completion is not tracked in Dombot.')
        if appraisals[name]:
            notes.append('DD appraisal history (displayed USD values):')
            for a in appraisals[name]:
                extra = ('; range ' + a[3]) if a[3] not in ('', '-') else ''
                if a[7]:
                    extra += '; ' + a[7]
                notes.append(f'{a[8]} | {a[1]} | {a[2]}{extra}')
        row['notes'] = '\n'.join(notes)
        assert len(row['notes']) <= 4000, f'Notes too long: {name}'
        for date in [purchase.get('date'), *(row.get('registration', {}).get(k) for k in ('createdDate','expirationDate'))]:
            if date:
                datetime.strptime(date, '%Y-%m-%d')
        rows.append(row)
    summary = {
        'sourceRows': len(rows), 'matchedSynced': sum(r['domain'] in synced for r in rows),
        'newActive': sum(r['domain'] not in synced and r['status'] == 'owned' for r in rows),
        'archive': sum(r['status'] != 'owned' for r in rows),
        'folders': dict(Counter(r['folder'] for r in rows if 'folder' in r)),
        'purchaseAmounts': sum('amount' in r['purchase'] for r in rows),
        'askingPrices': sum('listPrice' in r for r in rows),
        'manualRenewalPrices': sum('renewal' in r for r in rows),
        'appraisalRows': sum(len(v) for v in appraisals.values()),
        'appraisalsWithoutDomain': sorted(set(appraisals) - {r['domain'] for r in rows}),
        'maxNoteLength': max(len(r['notes']) for r in rows),
    }
    for filename, value in [('normalized-rows.json', rows), ('migration-summary.json', summary)]:
        path = out_path / filename
        path.write_text(json.dumps(value, indent=2))
        path.chmod(0o600)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

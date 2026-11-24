import { beforeEach, expect, it } from 'vitest';
import { MemoryDocStore } from './doc-store';
import { configureStore, hydrateStores } from './namespace';
import { buildBundle, importBundle } from './bundle';
import { runMigrations } from './migrations';

const app = { version: '2.2.2', platform: 'test' };
let store: MemoryDocStore;
beforeEach(async () => {
  store = new MemoryDocStore();
  configureStore(store);
  await hydrateStores();
});

it('archives retired events before migration removes them and retains flags in backups', async () => {
  const dropped = { id: 'old', domainName: 'example.com', type: 'dropped' };
  const sold = { id: 'sale', domainName: 'sale.com', type: 'sold' };
  await store.put('meta', 'schemaVersion', 3);
  await store.put('domain-for-sale', 'example.com', true);
  await store.putMany('domain-events', [
    ['old', dropped],
    ['sale', sold],
  ]);
  await runMigrations(store, store);
  await runMigrations(store, store);
  await hydrateStores();
  expect(await store.list('domain-events')).toEqual({ sale: sold });
  const b = buildBundle(app);
  expect(b.namespaces['legacy-domain-events']).toEqual({ old: dropped });
  expect(b.namespaces['domain-for-sale']).toEqual({ 'example.com': true });
});

it('round-trips flags and original retired events from a v8 backup through v10', async () => {
  const dropped = { id: 'old', domainName: 'example.com', type: 'dropped' };
  await importBundle(
    JSON.stringify({
      ...buildBundle(app),
      version: 8,
      namespaces: {
        'domain-for-sale': { 'example.com': true, 'keep.com': false },
        'domain-events': { old: dropped },
      },
    }),
  );
  const exported = buildBundle(app);
  expect(exported.version).toBe(10);
  expect(exported.namespaces['domain-events']).toEqual({});
  expect(exported.namespaces['legacy-domain-events']).toEqual({ old: dropped });
  expect(exported.namespaces['domain-for-sale']).toEqual({
    'example.com': true,
    'keep.com': false,
  });
  configureStore(new MemoryDocStore());
  await hydrateStores();
  await importBundle(JSON.stringify(exported));
  expect(buildBundle(app).namespaces['legacy-domain-events']).toEqual({
    old: dropped,
  });
  expect(buildBundle(app).namespaces['domain-for-sale']).toEqual(
    exported.namespaces['domain-for-sale'],
  );
});

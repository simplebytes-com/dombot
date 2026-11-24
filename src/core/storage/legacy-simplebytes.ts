import { Namespace } from './namespace';

// Preserve the retired fork flag in storage and full backups. It has no
// controls or pricing semantics in the upstream UI.
new Namespace<boolean>('domain-for-sale');

// Upstream schema v5 removes dropped/archived events. Keep the original
// records outside the active ledger so history can still be recovered.
export const LEGACY_EVENTS_NAMESPACE = 'legacy-domain-events';
new Namespace<unknown>(LEGACY_EVENTS_NAMESPACE);

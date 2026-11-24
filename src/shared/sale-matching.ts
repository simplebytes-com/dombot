import {
  ACQUISITION_TYPES,
  DomainEventType,
  type DomainEvent,
} from './domain-events';
import type { MarketSale } from './markets';

/** Providers can report a distributed sale on different completion dates. */
export const SAME_SALE_DAYS = 14;

/** A linked sale from another account, without a repurchase between dates. */
export function overlapsMarketSale(
  event: DomainEvent,
  sale: MarketSale,
  events: readonly DomainEvent[],
): boolean {
  const date = event.date;
  const soldOn = sale.soldOn;
  if (
    event.domain !== sale.name ||
    event.type !== DomainEventType.Sold ||
    !event.marketSale ||
    event.marketSale.startsWith(`${sale.accountId}:`) ||
    !date ||
    !soldOn ||
    !(
      Math.abs(Date.parse(date) - Date.parse(soldOn)) <=
      SAME_SALE_DAYS * 86_400_000
    )
  )
    return false;
  const from = date < soldOn ? date : soldOn;
  const to = date > soldOn ? date : soldOn;
  return !events.some(
    (e) =>
      e.domain === sale.name &&
      ACQUISITION_TYPES.has(e.type) &&
      e.date &&
      e.date > from &&
      e.date <= to,
  );
}

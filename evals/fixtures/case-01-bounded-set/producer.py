"""Audit event producer: emits the full record for each operation."""

from gate import apply_gate


def on_event(event) -> dict:
    record = {
        "event_id": event.id,
        "actor": event.actor,
        "action": event.action,
        "resource": event.resource,
        "occurred_at": event.occurred_at,
        "outcome": event.outcome,
        "on_behalf_of": event.delegator,
        "correction_of": event.corrects,
    }
    return apply_gate(record)

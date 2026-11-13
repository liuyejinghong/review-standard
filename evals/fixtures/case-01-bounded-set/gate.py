"""Export gate: only allowlisted fields reach the archive."""

ALLOWED_FIELDS = {
    "event_id",
    "actor",
    "action",
    "resource",
    "occurred_at",
    "outcome",
}


def apply_gate(record: dict) -> dict:
    return {k: v for k, v in record.items() if k in ALLOWED_FIELDS}

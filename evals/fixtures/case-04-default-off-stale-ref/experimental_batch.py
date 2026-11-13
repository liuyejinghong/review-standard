"""Optional experimental batch-migration model."""

BATCH_CAP_ENABLED = False


def capped_count(requested: int, allowance: int) -> int:
    if not BATCH_CAP_ENABLED:
        return requested
    if allowance <= 0:
        return 0
    return min(requested, allowance)


class Job:
    def __init__(self, remaining: int) -> None:
        self.remaining = remaining
        self.stage1_done = False


def migrate_stage(job: Job, requested: int, allowance: int) -> bool:
    count = capped_count(requested, allowance)
    if BATCH_CAP_ENABLED and count <= 0 and requested > 0:
        return False
    job.remaining -= count
    job.stage1_done = True
    return True

from core.constants import JOB_STATUS_TRANSITIONS

def can_transition(current: str, next_status: str) -> bool:
    return next_status in JOB_STATUS_TRANSITIONS.get(current, [])

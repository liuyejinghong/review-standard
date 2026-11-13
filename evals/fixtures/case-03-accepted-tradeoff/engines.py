"""Replay and live alert decisions."""


def should_alert(rule, signal, limit_hit):
    if signal == "alert":
        return "alert_signal"
    if limit_hit:
        return "limit_exceeded"
    return None


def replay_loop(windows, rule):
    # sync: evaluates against each window's min/max bounds
    for window in windows:
        yield should_alert(rule, window.signal, window.max_hit_limit)


def live_loop(sample, rule):
    # async: evaluates against a single polled sample, no bounds
    return should_alert(rule, sample.signal, sample.limit_hit)

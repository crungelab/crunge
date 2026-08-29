def step_until(runner, predicate, max_steps=20):
    """Step until predicate() is true. Avoids hard-coding scheduling latency."""
    for _ in range(max_steps):
        if predicate():
            return
        runner.step()
    raise AssertionError(f"predicate not satisfied in {max_steps} steps")
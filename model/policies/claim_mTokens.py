from typing import Any


def claimMTokens_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    if current_state["exchangeTime"] > 0:
        return {"step": "post-exchange"}
    return {"step": "continue"}

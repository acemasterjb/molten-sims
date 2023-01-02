from typing import Any


def exchange_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    deposit_started = False
    for agent in current_state["agents"]:
        if agent["DAI"] == 0:
            deposit_started = True
            break

    daoBalance_can_be_charged = current_state["DAO_treasury"]["daoToken_balance"] > 0

    exchange_possible = (
        deposit_started or current_state["exchangeTime"] == 0
    ) and daoBalance_can_be_charged
    exchange_criteria_met = exchange_possible and current_state["totalDeposited"] > 0

    if exchange_criteria_met:
        return {"step": "exchanging"}
    if current_state["exchangeTime"] > 0:
        return {"step": "post-exchange"}
    return {"step": "continue"}


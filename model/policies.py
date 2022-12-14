from datetime import datetime
from typing import Any


def deposit_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    if current_state["exchangeTime"] == 0:
        return {"step": "depositing"}
    return {"action": "continue"}


def refund_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    if current_state["exchangeTime"] == 0:
        agents: list[dict[str, Any]] = current_state["agents"]
        agents_to_keep = []
        for agent in agents:
            if agent["DAI"] == 0:
                agents_to_keep.append(agent)
        return {"step": "depositing", "agents": agents_to_keep}
    return {"action": "continue"}
    


def exchange_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    exchange_criteria_met = (
        current_state["exchangeTime"] == 0 and current_state["totalDeposited"] > 0
    )
    if exchange_criteria_met:
        return {"step": "exchanging"}
    return {"step": "depositing"}
    


def claimMTokens_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    if current_state["exchangeTime"] > 0:
        return {"step": "post-exchange"}
    return {"action": "continue"}
    


def vote_liquidate_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    agents = sys_params["agents"]
    has_claimed = 0
    for i_agent in range(0, len(agents) - 1):
        if current_state["mTokensClaimed"][agents[i_agent]["address"]]:
            has_claimed += 1
    if has_claimed >= 5 and current_state["exchangeTime"] > 0:
        return {"step": "post-exchange"}
    return {"action": "continue"}
    


def liquidate_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    criteria_for_liquidation_met = (
        current_state["totalDeposited"] == current_state["totalVotedForLiquidation"]
    )
    if criteria_for_liquidation_met:
        current_state["liquidationTime"] = (
            datetime.utcnow().replace(microsecond=0).timestamp()
        )
        return {"step": "unanimous liquidation vote"}
    return {"action": "continue"}
    


def claim_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    if current_state["liquidationTime"] > 0:
        return {"step": "post-liquidation"}
    return {"action": "continue"}
    

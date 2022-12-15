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
    return {"step": "continue"}


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
    return {"step": "continue"}


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


def claimMTokens_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    if current_state["exchangeTime"] > 0:
        return {"step": "post-exchange"}
    return {"step": "continue"}


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

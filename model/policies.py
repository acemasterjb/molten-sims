from random import uniform
from typing import Any


def deposit_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    default = {"step": "continue"}
    if current_state["exchangeTime"] == 0:
        dice_roll = uniform(0.1, 0.9)

        agents = current_state["agents"].copy()
        current_deposits = current_state["deposited"]
        agents_to_keep: list[dict[str, Any]] = []

        for agent in agents:
            agent_address = agent["address"]
            deposit_criteria_met = (
                agent["DAI"] > 0
                and current_deposits[agent_address] == 0
                and agent["probabilities"]["deposit"] >= dice_roll
            )

            if deposit_criteria_met:
                agents_to_keep.append(agent)

        if len(agents_to_keep) > 0:
            return {"step": "depositing", "agents": agents_to_keep}
        else:
            return default
    return default


def refund_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    default = {"step": "continue"}
    if current_state["exchangeTime"] == 0:
        dice_roll = uniform(0.1, 0.9)

        agents = current_state["agents"].copy()
        current_deposits = current_state["deposited"]
        agents_to_keep: list[dict[str, Any]] = []

        for agent in agents:
            agent_address = agent["address"]
            deposit_criteria_met = (
                agent["DAI"] == 0
                and current_deposits[agent_address] > 0
                and agent["probabilities"]["refund"] >= dice_roll
            )

            if deposit_criteria_met:
                agents_to_keep.append(agent)

        if len(agents_to_keep) > 0:
            return {"step": "depositing", "agents": agents_to_keep}
        else:
            return default
    return default


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
    default = {"step": "continue"}
    dice_roll = uniform(0.1, 0.9)

    agents: list[dict[str, Any]] = current_state["agents"]
    agents_to_keep = []
    for i_agent in range(len(agents) - 1):
        agent_will_vote = (
            (not current_state["votedForLiquidation"][agents[i_agent]["address"]])
            and current_state["deposited"][agents[i_agent]["address"]] > 0
            and agents[i_agent]["probabilities"]["liquidate"] >= dice_roll
        )
        if agent_will_vote:
            agents_to_keep.append(agents[i_agent])

    if len(agents_to_keep) > 0 and current_state["exchangeTime"] > 0:
        return {"step": "post-exchange", "agents": agents_to_keep}
    else:
        return default


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
        return {"substep": "unanimous liquidation vote"}
    return {"substep": "continue"}


def claim_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    default = {"step": "continue"}
    dice_roll = uniform(0.1, 0.9)

    agents: list[dict[str, Any]] = current_state["agents"]
    agents_to_keep = []
    for i_agent in range(len(agents) - 1):
        agent_will_vote = (
            current_state["totalVotedForLiquidation"] == current_state["totalDeposited"]
            and agents[i_agent]["DAO"] == 0
            and agents[i_agent]["probabilities"]["claim"] >= dice_roll
        )
        if agent_will_vote:
            agents_to_keep.append(agents[i_agent])

    if len(agents_to_keep) > 0 and current_state["exchangeTime"] > 0:
        return {"step": "post-liquidation", "agents": agents_to_keep}
    else:
        return default

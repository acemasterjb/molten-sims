from random import uniform
from typing import Any


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


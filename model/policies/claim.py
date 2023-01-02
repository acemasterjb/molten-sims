from random import uniform
from typing import Any


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

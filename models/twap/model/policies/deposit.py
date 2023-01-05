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

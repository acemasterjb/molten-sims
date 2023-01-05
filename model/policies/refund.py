from random import randint, uniform
from typing import Any


def refund_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    default = {"step": "continue"}
    if current_state["exchangeTime"] == 0:
        dice_roll = uniform(0.1, 0.9)

        agents = current_state["agents"]
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
                refund_amount = randint(
                    1 * 10 ** sys_params["deposit_decimals"],
                    current_deposits[agent_address],
                )
                agents_to_keep.append((agent, refund_amount))

        if len(agents_to_keep) > 0:
            return {"step": "depositing", "agents": agents_to_keep}
        else:
            return default
    return default

from random import uniform
from typing import Any


def claimMTokens_policy(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
):
    default = {"step": "continue"}
    dice_roll = uniform(0.1, 0.9)

    agents = current_state["agents"]
    agents_to_keep: list[dict[str, Any]] = []
    mTokensClaimed: dict[bytes, bool] = current_state["mTokensClaimed"]
    deposits = current_state["deposited"]

    for agent in agents:
        criteria_to_claim_met = (
            deposits[agent["address"]] > 0
            and not mTokensClaimed[agent["address"]]
        )

        if criteria_to_claim_met:
            agents_to_keep.append(agent)

    if len(agents_to_keep) > 0 and current_state["exchangeTime"] > 0:
        return {"step": "post-exchange", "agents": agents_to_keep}
    return default

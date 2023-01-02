from copy import deepcopy
from random import uniform
from typing import Any


def claimMTokens_set_claimed(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mTokensClaimed", current_state["mTokensClaimed"])
    if policy_inputs["step"] != "post-exchange":
        return default

    dice_roll = uniform(0.1, 0.9)

    agents = current_state["agents"]
    i_claimer = -1
    for i_agent in range(0, len(agents) - 1):
        if current_state["deposited"][agents[i_agent]["address"]] > 0:
            i_claimer = i_agent
            break

    if i_claimer < 0:
        return default

    claimer = agents[i_claimer]
    agent_opts_to_not_claim = claimer["probabilities"]["claimMTokens"] < dice_roll
    if agent_opts_to_not_claim:
        return default

    claimer_address: bytes = agents[i_claimer]["address"]

    mTokensClaimed: dict[bytes, bool] = deepcopy(current_state["mTokensClaimed"])
    mTokensClaimed[claimer_address] = True

    return ("mTokensClaimed", mTokensClaimed)


def claimMTokens_credit_funder(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("agents", current_state["agents"])
    if policy_inputs["step"] != "post-exchange":
        return default

    agents = deepcopy(current_state["agents"])
    i_claimer = -1
    for i_agent in range(0, len(agents) - 1):
        if current_state["mTokensClaimed"][agents[i_agent]["address"]]:
            i_claimer = i_agent
            break

    claimer_address = agents[i_claimer]["address"]
    agents[i_claimer]["mDAO"] += (
        current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"]
        / sys_params["exchange_rate"]
    )

    return ("agents", agents)

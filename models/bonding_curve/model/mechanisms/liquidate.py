from copy import deepcopy
from typing import Any


def vote_liquidate_update_total(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("totalVotedForLiquidation", current_state["totalVotedForLiquidation"])
    if policy_inputs["step"] != "post-exchange":
        return default

    agents = policy_inputs["agents"]
    voter = agents[-1]

    voter_address = voter["address"]
    total_voted_for_liquidation = current_state["totalVotedForLiquidation"]

    return (
        "totalVotedForLiquidation",
        total_voted_for_liquidation + current_state["deposited"][voter_address],
    )


def vote_liquidate_set_voted(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("votedForLiquidation", current_state["votedForLiquidation"])
    if policy_inputs["step"] != "post-exchange":
        return default

    voted_for_liquidation = deepcopy(current_state["votedForLiquidation"])
    agents = policy_inputs["agents"]
    voter = agents[-1]

    voter_address = voter["address"]
    voted_for_liquidation[voter_address] = True

    return ("votedForLiquidation", voted_for_liquidation)


def liquidate_tokens(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["substep"] != "unanimous liquidation vote":
        return ("liquidationTime", current_state["liquidationTime"])

    return ("liquidationTime", substep)

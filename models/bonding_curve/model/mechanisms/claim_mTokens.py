from copy import deepcopy
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

    agents = policy_inputs["agents"]
    claimer_address: bytes = agents[-1]["address"]

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

    current_agents: list[dict] = deepcopy(current_state["agents"])
    i_agent = current_agents.index(policy_inputs["agents"][-1])
    claimer_address = current_agents[i_agent]["address"]

    current_agents[i_agent]["mDAO"] += current_state["mTokens_allocation"][
        claimer_address
    ]

    return ("agents", current_agents)


def claimMTokens_clear_allocation(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mTokens_allocation", current_state["mTokens_allocation"])
    if policy_inputs["step"] != "post-exchange":
        return default

    current_agents: list[dict] = deepcopy(current_state["agents"])
    i_agent = current_agents.index(policy_inputs["agents"][-1])
    claimer_address = current_agents[i_agent]["address"]

    mTokens_allocation = deepcopy(current_state["mTokens_allocation"])
    mTokens_allocation[claimer_address] = 0

    return ("mTokens_allocation", mTokens_allocation)


def claimMTokens_debit_molten(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mToken_balance", current_state["mToken_balance"])
    if policy_inputs["step"] != "post-exchange":
        return default

    current_agents: list[dict] = deepcopy(current_state["agents"])
    i_agent = current_agents.index(policy_inputs["agents"][-1])
    claimer_address = current_agents[i_agent]["address"]

    return (
        "mToken_balance",
        current_state["mToken_balance"]
        - current_state["mTokens_allocation"][claimer_address],
    )

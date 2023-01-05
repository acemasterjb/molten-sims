from copy import deepcopy
from typing import Any

from ..state_variables import initial_state


def deposit_into_funder_account(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("deposited", current_state["deposited"])
    if policy_inputs["step"] != "depositing":
        return default

    agents: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    current_deposits: dict[bytes, int] = deepcopy(current_state["deposited"])

    depositer, _ = agents[-1]
    funder_address: bytes = depositer["address"]
    deposit_amount: int = depositer["DAI"]

    current_deposits.update(
        {funder_address: current_deposits[funder_address] + deposit_amount}
    )

    return ("deposited", current_deposits)


def deposit_and_deplete_DAI(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("agents", current_state["agents"])
    if policy_inputs["step"] != "depositing":
        return default

    agents: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    current_agents: list[dict[str, Any]] = deepcopy(current_state["agents"])

    i_agent = current_agents.index(agents[-1][0])
    current_agents[i_agent].update({"DAI": 0})
    return ("agents", current_agents)


def deposit_and_update_total(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("totalDeposited", current_state["totalDeposited"])
    if policy_inputs["step"] != "depositing":
        return default

    agents: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    current_agents: list[dict[str, Any]] = current_state["agents"]
    i_agent = current_agents.index(agents[-1][0])

    deposit_amount = initial_state["agents"][i_agent]["DAI"]

    return ("totalDeposited", current_state["totalDeposited"] + deposit_amount)


def deposit_and_allocate_mTokens(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mTokens_allocation", current_state["mTokens_allocation"])
    if policy_inputs["step"] != "depositing":
        return default

    agents: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    mTokens_allocation: dict[bytes, int] = deepcopy(current_state["mTokens_allocation"])

    agent, mint_weight = agents[-1]
    agent_address = agent["address"]

    mTokens_allocation.update({agent_address: mint_weight})

    return ("mTokens_allocation", mTokens_allocation)

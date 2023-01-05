from copy import deepcopy
from typing import Any

from ..state_variables import initial_state


def refund_funder_account(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("deposited", current_state["deposited"])
    if policy_inputs["step"] != "depositing":
        return default

    agent_payloads: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    current_deposits: dict[bytes, int] = deepcopy(current_state["deposited"])

    depositer, refund_amount = agent_payloads[-1]
    funder_address: bytes = depositer["address"]

    current_deposits.update(
        {funder_address: current_deposits[funder_address] - refund_amount}
    )

    return ("deposited", current_deposits)


def refund_and_credit_DAI(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("agents", current_state["agents"])
    if policy_inputs["step"] != "depositing":
        return default

    agent_payload: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    current_agents: list[dict[str, Any]] = deepcopy(current_state["agents"])

    agent, _ = agent_payload[-1]
    i_agent = current_agents.index(agent)
    current_agents[i_agent].update({"DAI": initial_state["agents"][i_agent]["DAI"]})
    return ("agents", current_agents)


def refund_and_update_total(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("totalDeposited", current_state["totalDeposited"])
    if policy_inputs["step"] != "depositing":
        return default

    agent_payload: list[tuple[dict[str, Any], int]] = policy_inputs["agents"]
    current_agents: list = current_state["agents"]
    agent, _ = agent_payload[-1]
    i_agent = current_agents.index(agent)

    deposit_amount: int = initial_state["agents"][i_agent]["DAI"]

    return ("totalDeposited", current_state["totalDeposited"] - deposit_amount)

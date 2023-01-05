from copy import deepcopy
from typing import Any


def claim_update_funder_balances(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("agents", current_state["agents"])
    if policy_inputs["step"] != "post-liquidation":
        return default

    agents = deepcopy(policy_inputs["agents"])
    claimer_address = agents[-1]["address"]
    mToken_balance = agents[-1]["mDAO"]

    unclaimed_mToken_balance = (
        0
        if current_state["mTokensClaimed"][claimer_address]
        else current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"]
        / sys_params["exchange_rate"]
    )
    claimable_balance = mToken_balance + unclaimed_mToken_balance

    agents[-1]["mDAO"] = 0
    agents[-1]["DAO"] += claimable_balance

    return ("agents", agents)


def claim_update_molten_mToken_balance(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mToken_balance", current_state["mToken_balance"])
    if policy_inputs["step"] != "post-liquidation":
        return default

    agents = policy_inputs["agents"]

    claimer_address = agents[-1]["address"]

    unclaimed_mToken_balance = (
        0
        if current_state["mTokensClaimed"][claimer_address]
        else current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"]
        / sys_params["exchange_rate"]
    )

    return (
        "mToken_balance",
        current_state["mToken_balance"] - unclaimed_mToken_balance,
    )

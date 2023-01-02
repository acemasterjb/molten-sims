from copy import deepcopy
from datetime import datetime
from typing import Any


def exchange_set_exchange_time(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "exchanging":
        return ("exchangeTime", current_state["exchangeTime"])

    return ("exchangeTime", datetime.utcnow().replace(microsecond=0).timestamp())


def exchange_send_mTokens(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "exchanging":
        return ("daoToken_balance", current_state["daoToken_balance"])

    total_deposited = current_state["totalDeposited"]

    return (
        "mToken_balance",
        total_deposited
        * 10 ** sys_params["mToken_decimals"]
        / sys_params["exchange_rate"],
    )


def exchange_transfer_to_dao(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "exchanging":
        return ("daoToken_balance", current_state["daoToken_balance"])

    total_deposited = current_state["totalDeposited"]
    dao_token_balance_delta = (
        total_deposited
        * 10 ** sys_params["daoToken_decimals"]
        / sys_params["exchange_rate"]
    )

    treasury = deepcopy(current_state["DAO_treasury"])
    treasury["depositToken_balance"] += total_deposited
    treasury["daoToken_balance"] -= dao_token_balance_delta

    return ("DAO_treasury", treasury)


def exchange_transfer_to_molten(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "exchanging":
        return ("daoToken_balance", current_state["daoToken_balance"])

    total_deposited = current_state["totalDeposited"]
    dao_token_balance_delta = (
        total_deposited
        * 10 ** sys_params["daoToken_decimals"]
        / sys_params["exchange_rate"]
    )

    return (
        "daoToken_balance",
        current_state["daoToken_balance"] + dao_token_balance_delta,
    )

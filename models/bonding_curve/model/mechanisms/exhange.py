from copy import deepcopy
from typing import Any

from ..utils.accounting import calculate_weights


def get_mToken_mint_weight(
    spot_price: int,
    supply: int,
    curve_pad_ratio: float,
    dao_decimals: int,
) -> int:
    start_weight, end_weight = calculate_weights(
        spot_price, 0, supply, curve_pad_ratio, dao_decimals
    )
    return end_weight - start_weight


def exchange_set_exchange_time(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "exchanging":
        return ("exchangeTime", current_state["exchangeTime"])

    return ("exchangeTime", substep)


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

    mint_weight = get_mToken_mint_weight(
        sys_params["exchange_rate"],
        total_deposited,
        sys_params["curve_pad_ratio"],
        sys_params["daoToken_decimals"],
    )

    return ("mToken_balance", mint_weight)


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
    dao_token_balance_delta = get_mToken_mint_weight(
        sys_params["exchange_rate"],
        total_deposited,
        sys_params["curve_pad_ratio"],
        sys_params["daoToken_decimals"],
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
    mint_weight = get_mToken_mint_weight(
        sys_params["exchange_rate"],
        total_deposited,
        sys_params["curve_pad_ratio"],
        sys_params["daoToken_decimals"],
    )

    return (
        "daoToken_balance",
        current_state["daoToken_balance"] + mint_weight,
    )

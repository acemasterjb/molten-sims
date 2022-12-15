from datetime import datetime
from random import uniform
from typing import Any

from .state_variables import initial_state


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

    agents: list[dict[str, Any]] = policy_inputs["agents"]
    current_deposits = current_state["deposited"].copy()

    depositer = agents[-1]
    funder_address = depositer["address"]
    deposit_amount = depositer["DAI"]

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

    agents: list[dict[str, Any]] = policy_inputs["agents"].copy()
    current_agents: list[dict[str, Any]] = current_state["agents"].copy()

    i_agent = current_agents.index(agents[-1])
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

    agents: list[dict[str, Any]] = policy_inputs["agents"]
    current_agents: list[dict[str, Any]] = current_state["agents"]
    i_agent = current_agents.index(agents[-1])

    deposit_amount = initial_state["agents"][i_agent]["DAI"]

    return ("totalDeposited", current_state["totalDeposited"] + deposit_amount)


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

    dice_roll = uniform(0.1, 0.9)

    agents: list[dict[str, Any]] = current_state["agents"]
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        substep_criteria_met = (
            agents[i_agent]["DAI"] == 0
            and current_state["deposited"][agents[i_agent]["address"]] > 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    refunder = agents[i_funder]
    agent_opts_to_not_deposit = refunder["probabilities"]["refund"] < dice_roll
    if agent_opts_to_not_deposit:
        return default

    funder_address = refunder["address"]
    to_be_refunded = current_state["deposited"][funder_address]

    current_deposits = current_state["deposited"].copy()
    current_deposits.update(
        {funder_address: current_state["deposited"][funder_address] - to_be_refunded}
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

    agents: list[dict[str, Any]] = current_state["agents"].copy()
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        substep_criteria_met = (
            agents[i_agent]["DAI"] == 0
            and current_state["deposited"][agents[i_agent]["address"]] == 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    agents[i_funder]["DAI"] = initial_state["agents"][i_funder]["DAI"]
    return ("agents", agents)


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

    agents: list[dict[str, Any]] = policy_inputs["agents"]
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        substep_criteria_met = (
            agents[i_agent]["DAI"] > 0
            and current_state["deposited"][agents[i_agent]["address"]] == 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    to_be_refunded = initial_state["agents"][i_funder]["DAI"]

    return ("totalDeposited", current_state["totalDeposited"] - to_be_refunded)


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

    treasury = current_state["DAO_treasury"].copy()
    treasury["depositToken_balance"] += current_state["totalDeposited"]
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


def exchange_charge_dao(
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

    treasury = current_state["DAO_treasury"].copy()
    treasury["daoToken_balance"] -= dao_token_balance_delta

    return ("DAO_treasury", treasury)


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

    claimer_address = agents[i_claimer]["address"]

    mTokensClaimed = current_state["mTokensClaimed"].copy()
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

    agents = current_state["agents"].copy()
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

    voted_for_liquidation = current_state["votedForLiquidation"].copy()
    agents = policy_inputs["agents"]
    voter = agents[-1]

    voter_address = voter["address"]
    voted_for_liquidation[voter_address] = True

    return ("votedForLiquidation", voted_for_liquidation)


def liquidate(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["substep"] != "unanimous liquidation vote":
        return ("liquidationTime", current_state["liquidationTime"])

    return ("liquidationTime", datetime.utcnow().replace(microsecond=0).timestamp())


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

    agents = policy_inputs["agents"].copy()
    claimer_address = agents[-1]["address"]
    mToken_balance = agents[-1]["mDAO"]

    unclaimed_mToken_balance = (
        0
        if current_state["mTokensClaimed"][claimer_address]
        else current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"]
        / sys_params["exchangeRate"]
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

    agents = policy_inputs["agents"].copy()

    claimer_address = agents[-1]["address"]

    unclaimed_mToken_balance = (
        0
        if current_state["mTokensClaimed"][claimer_address]
        else current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"]
        / sys_params["exchangeRate"]
    )

    return (
        "mToken_balance",
        current_state["mToken_balance"] - unclaimed_mToken_balance,
    )

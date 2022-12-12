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

    dice_roll = uniform(0.1, 0.9)

    agents: list[dict[str, Any]] = current_state["agents"]
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        agent_address = agents[i_agent]["address"]
        deposits = current_state["deposited"]

        substep_criteria_met = (
            agents[i_agent]["DAI"] > 0 and deposits[agent_address] == 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    depositer = agents[i_funder]
    agent_opts_to_not_deposit = depositer["probabilities"]["deposit"] < dice_roll
    if agent_opts_to_not_deposit:
        return default

    funder_address = depositer["address"]
    deposit_amount = depositer["DAI"]

    current_deposits = current_state["deposited"]
    current_deposits.update(
        {funder_address: current_state["deposited"][funder_address] + deposit_amount}
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

    agents: list[dict[str, Any]] = current_state["agents"]
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        substep_criteria_met = (
            agents[i_agent]["DAI"] > 0
            and current_state["deposited"][agents[i_agent]["address"]] > 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    agents[i_funder]["DAI"] = 0
    return ("agents", agents)


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

    agents: list[dict[str, Any]] = current_state["agents"]
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        substep_criteria_met = (
            current_state["agents"][i_agent]["DAI"] == 0
            and current_state["deposited"][agents[i_agent]["address"]] > 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    deposit_amount = initial_state["agents"][i_funder]["DAI"]

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

    current_deposits = current_state["deposited"]
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

    agents: list[dict[str, Any]] = current_state["agents"]
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

    agents: list[dict[str, Any]] = current_state["agents"]
    i_funder = -1
    for i_agent in range(0, len(agents) - 1):
        substep_criteria_met = (
            current_state["agents"][i_agent]["DAI"] > 0
            and current_state["deposited"][agents[i_agent]["address"]] == 0
        )
        if substep_criteria_met:
            i_funder = i_agent
            break

    if i_funder < 0:
        return default

    to_be_refunded = initial_state["agents"][i_funder]["DAI"]

    return ("totalDeposited", current_state["totalDeposited"] - to_be_refunded)


def exchange(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "exchanging":
        return ("daoToken_balance", current_state["daoToken_balance"])

    current_state["exchangeTime"] = datetime.utcnow().replace(microsecond=0).timestamp()
    total_deposited = current_state["totalDeposited"]
    current_state["mToken_balance"] = (
        total_deposited
        * 10 ** sys_params["mtoken_decimals"][0]
        / sys_params["exchange_rate"][0]
    )

    current_state["totalDeposited"] = 0
    sys_params["DAO_treasury"][0]["depositToken_balance"] += total_deposited

    dao_token_balance_delta = (
        total_deposited
        * 10 ** sys_params["daoToken_decimals"][0]
        / sys_params["exchange_rate"][0]
    )
    sys_params["DAO_treasury"][0]["daoToken_balance"] -= dao_token_balance_delta
    return (
        "daoToken_balance",
        current_state["daoToken_balance"] + dao_token_balance_delta,
    )


def claimMTokens(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mtokensClaimed", current_state["mtokensClaimed"])
    if policy_inputs["step"] != "post-exchange":
        return default

    dice_roll = uniform(0.1, 0.9)

    agents = sys_params["agents"]
    i_claimer = -1
    for i_agent in range(0, len(agents) - 1):
        if current_state["deposited"][agents[i_agent]] > 0:
            i_claimer = i_agent
            break

    if i_claimer < 0:
        return default

    claimer = agents[i_claimer]
    agent_opts_to_not_claim = claimer["probabilities"]["claimMTokens"] < dice_roll
    if agent_opts_to_not_claim:
        return default

    claimer_address = agents[i_claimer]["address"]
    if current_state["deposited"][claimer_address] == 0:
        return default

    if current_state["mtokensClaimed"][claimer_address]:
        return default
    # current_state["mtokensClaimed"][claimer_address] = True

    sys_params["agents"][i_claimer]["mDAO"] += (
        current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"][0]
        / sys_params["exchange_rate"][0]
    )

    return (
        "mtokensClaimed",
        current_state["mtokensClaimed"].update({claimer_address: True}),
    )


def vote_liquidate(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("votedForLiquidation", current_state["votedForLiquidation"])
    if policy_inputs["step"] != "post-exchange":
        return default

    dice_roll = uniform(0.1, 0.9)

    agents = sys_params["agents"]
    i_voter = -1
    for i_agent in range(0, len(agents) - 1):
        agent = agents[i_agent]
        if not current_state["votedForLiquidation"][agent["address"]]:
            i_voter = i_agent
            break

    if i_voter < 0:
        return default

    voter = agents[i_voter]
    agent_opts_to_not_vote = voter["probabilities"]["liquidate"] < dice_roll
    if agent_opts_to_not_vote:
        return default

    voter_address = voter["address"]
    if current_state["deposited"][voter_address] == 0:
        return default

    current_state["totalVotedForLiquidation"] += current_state["deposited"][
        voter_address
    ]

    return (
        "votedForLiquidation",
        current_state["votedForLiquidation"].update({voter_address: True}),
    )


def liquidate(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    if policy_inputs["step"] != "unanimous liquidation vote":
        return ("liquidationTime", current_state["liquidationTime"])

    return ("liquidationTime", datetime.utcnow().replace(microsecond=0).timestamp())


def claim(
    sys_params: dict[str, Any],
    substep: int,
    _,
    current_state: dict[str, Any],
    policy_inputs: dict[str, Any],
):
    default = ("mToken_balance", current_state["mToken_balance"])
    if policy_inputs["step"] != "post-liquidation":
        return default

    dice_roll = uniform(0.1, 0.9)

    agents = sys_params["agents"]
    i_claimer = -1
    for i_agent in range(0, len(agents) - 1):
        if agents[i_agent]["DAO"] == 0:
            i_claimer = -1
            break

    if i_claimer == -1:
        return default

    claimer = agents[i_claimer]
    agent_opts_to_not_claim = claimer["probabilities"]["claim"] < dice_roll
    if agent_opts_to_not_claim:
        return default

    claimer_address = claimer["address"]
    mToken_balance = claimer["mDAO"]
    unclaimed_mToken_balance = (
        0
        if current_state["mTokensClaimed"][claimer_address]
        else current_state["deposited"][claimer_address]
        * 10 ** sys_params["mToken_decimals"][0]
        / sys_params["exchangeRate"][0]
    )

    claimable_balance = mToken_balance + unclaimed_mToken_balance
    if claimable_balance == 0:
        return default

    sys_params["agents"][i_claimer]["mDAO"] = 0
    sys_params["agents"][i_claimer]["DAO"] += claimable_balance

    return (
        "mToken_balance",
        current_state["mToken_balance"] - unclaimed_mToken_balance,
    )

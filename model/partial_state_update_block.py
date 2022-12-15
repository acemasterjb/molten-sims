from .mechanisms import (
    claim,
    claimMTokens_set_claimed,
    claimMTokens_credit_funder,
    deposit_and_deplete_DAI,
    deposit_and_update_total,
    deposit_into_funder_account,
    exchange_charge_dao,
    exchange_receive_deposit_token,
    exchange_send_mTokens,
    exchange_set_exchange_time,
    exchange_transfer_to_dao,
    exchange_transfer_to_molten,
    liquidate,
    refund_and_credit_DAI,
    refund_and_update_total,
    refund_funder_account,
    vote_liquidate,
)

from .policies import (
    claim_policy,
    claimMTokens_policy,
    deposit_policy,
    exchange_policy,
    liquidate_policy,
    refund_policy,
    vote_liquidate_policy,
)

block_step_1 = [
    {
        "policies": {"action": deposit_policy},
        "variables": {
            "deposited": deposit_into_funder_account,
            "agents": deposit_and_deplete_DAI,
            "totalDeposited": deposit_and_update_total,
        },
    }
    for _ in range(0, 9)
]

block_step_2 = [
    {
        "policies": {"action": refund_policy},
        "variables": {
            "deposited": refund_funder_account,
            "agents": refund_and_credit_DAI,
            "totalDeposited": refund_and_update_total,
        },
    }
    for _ in range(0, 9)
]

block_step_3 = [
    {
        "policies": {"action": exchange_policy},
        "variables": {
            "exchangeTime": exchange_set_exchange_time,
            "mToken_balance": exchange_send_mTokens,
            "DAO_treasury": exchange_transfer_to_dao,
            "daoToken_balance": exchange_charge_dao,
            "DAO_treasury": exchange_transfer_to_molten,
            "totalDeposited": exchange_receive_deposit_token,
        },
    }
]

block_step_4 = [
    {
        "policies": {"action": claimMTokens_policy},
        "variables": {
            "mTokensClaimed": claimMTokens_set_claimed,
            "agents": claimMTokens_credit_funder,
        },
    }
    for _ in range(0, 9)
]

block_step_5 = [
    {
        "policies": {
            "vote_liquidate_policicy": vote_liquidate_policy,
            "liquidate_policy": liquidate_policy,
        },
        "variables": {"step_1": vote_liquidate, "step_2": liquidate},
    }
    for _ in range(0, 9)
]

block_step_6 = [
    {
        "policies": {"claim_policy": claim_policy},
        "variables": {"step_1": claim},
    }
    for _ in range(0, 9)
]

block_steps = [
    block_step_1,
    block_step_2,
    block_step_3,
    block_step_4,
    # block_step_5,
    # block_step_6,
]
partial_state_update_block = []

for block_step in block_steps:
    partial_state_update_block.extend(block_step)

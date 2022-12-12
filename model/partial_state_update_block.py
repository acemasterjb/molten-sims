from .mechanisms import (
    claim,
    claimMTokens,
    deposit_and_deplete_DAI,
    deposit_and_update_total,
    deposit_into_funder_account,
    exchange,
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
        "policies": {"deposit_policy": deposit_policy},
        "variables": {
            "deposit_into_funder": deposit_into_funder_account,
            "deposit_deplete_dai": deposit_and_deplete_DAI,
            "deposit_update_total": deposit_and_update_total,
        },
    }
    for _ in range(0, 9)
]

block_step_2 = [
    {
        "policies": {"deposit_policy": refund_policy},
        "variables": {
            "deposit_into_funder": refund_funder_account,
            "deposit_deplete_dai": refund_and_credit_DAI,
            "deposit_update_total": refund_and_update_total,
        },
    }
    for _ in range(0, 9)
]

block_step_3 = [
    {
        "policies": {"exchange_policy": exchange_policy},
        "variables": {"exchange": exchange},
    }
]

block_step_4 = [
    {
        "policies": {"claimMTokens_policy": claimMTokens_policy},
        "variables": {"claimMTokens": claimMTokens},
    }
    for _ in range(0, 9)
]

block_step_5 = [
    {
        "policies": {
            "vote_liquidate_policicy": vote_liquidate_policy,
            "liquidate_policy": liquidate_policy,
        },
        "variables": {"vote_liquidate": vote_liquidate, "liquidate": liquidate},
    }
    for _ in range(0, 9)
]

block_step_6 = [
    {
        "policies": {"claim_policy": claim_policy},
        "variables": {"claim": claim},
    }
    for _ in range(0, 9)
]

block_steps = [
    block_step_1,
    block_step_2,
    block_step_3,
    block_step_4,
    block_step_5,
    block_step_6,
]
partial_state_update_block = []

for block_step in block_steps:
    partial_state_update_block.extend(block_step)

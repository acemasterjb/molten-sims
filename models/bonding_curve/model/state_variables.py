from datetime import datetime
from random import randint, uniform
from typing import Any

deployed_timestamp = datetime.utcnow().replace(microsecond=0).timestamp()
n_agents = 10
init_bool_state = {n.to_bytes(2, "big"): False for n in range(2, n_agents + 2)}

genesis_state = {
    "block_timestamp": deployed_timestamp,
    "deposited": {n.to_bytes(2, "big"): 0 for n in range(2, n_agents + 2)},
    "mTokens_allocation": {n.to_bytes(2, "big"): 0 for n in range(2, n_agents + 2)},
    "totalDeposited": 0,
    "exchangeTime": 0,
    "lockingDuration": 0,
    "mTokensClaimed": init_bool_state.copy(),
    "liquidationTime": 0,
    "votedForLiquidation": init_bool_state.copy(),
    "totalVotedForLiquidation": 0,
    "mToken_balance": 0,
    "daoToken_balance": 0,
    "DAO_treasury": {
        "address": (1).to_bytes(2, "big"),
        "daoToken_balance": 2e9 * 10**18,
        "depositToken_balance": 0,
    },
    "agents": [],
}


def init_state(n_agents: int = 10) -> dict[str, Any]:
    for i_agent in range(n_agents):
        genesis_state["agents"].append(
            {
                "address": (i_agent + 2).to_bytes(2, "big"),
                "DAI": randint(1e21, 9.99e24),
                "mDAO": 0,
                "DAO": 0,
                "probabilities": {
                    "deposit": uniform(0.1, 0.9),
                    "refund": uniform(0.1, 0.2),
                    "liquidate": uniform(0.1, 0.4),
                    "claim": uniform(0.1, 0.9),
                },
            }
        )
    return genesis_state


initial_state = init_state()

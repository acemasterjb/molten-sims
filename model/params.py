from typing import Any
from random import randint, uniform

params = {
    "DAO_treasury": [{
        "address": "0x01",
        "daoToken_balance": 2e9,
        "depositToken_balance": 0,
    }],
    "exchange_rate": [0.2],
    "agents": [],
    "mToken_decimals": [18],
    "daoToken_decimals": [18],
}


def init_params(n_agents: int = 10) -> dict[str, Any]:
    for i_agent in range(0, n_agents - 1):
        params["agents"].append(
            {
                "address": f"0x0{i_agent + 2}",
                "DAI": randint(1e3, 9.99e6),
                "mDAO": 0,
                "DAO": 0,
                "probabilities": {
                    "deposit": uniform(0.1, 0.9),
                    "refund": uniform(0.1, 0.2),
                    "claimMTokens": uniform(0.1, 0.9),
                    "liquidate": uniform(0.1, 0.4),
                    "claim": uniform(0.1, 0.9),
                },
            }
        )
    return params

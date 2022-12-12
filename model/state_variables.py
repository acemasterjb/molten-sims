from datetime import datetime

deployed_timestamp = datetime.utcnow().replace(microsecond=0).timestamp()
n_agents = 10
init_bool_state = {f"0x0{n}": False for n in range(2, n_agents + 1)}

genesis_state = {
    "block_timestamp": deployed_timestamp,
    "deposited": {f"0x0{n}": 0 for n in range(2, n_agents + 1)},
    "totalDeposited": 0,
    "exchangeTime": 0,
    "lockingDuration": 0,
    "mTokensClaimed": init_bool_state.copy(),
    "liquidationTime": 0,
    "votedForLiquidation": init_bool_state.copy(),
    "totalVotedForLiquidation": 0,
    "mToken_balance": 0,
    "depositToken_balance": 0,
    "daoToken_balance": 0
}

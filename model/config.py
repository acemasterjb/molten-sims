from cadCAD import configs
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim

from .params import init_params
from .partial_state_update_block import partial_state_update_block
from .state_variables import genesis_state

del configs[:]

sim_config = config_sim(
    {
        "N": 1,  # no. of sim runs
        "T": range(70),  # no. of timesteps; 14s * 5 blocks
        "M": init_params(),
    }
)

exp = Experiment()
exp.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_state,
    partial_state_update_blocks=partial_state_update_block,
)

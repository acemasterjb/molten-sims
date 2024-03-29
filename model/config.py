from cadCAD import configs
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim

from .params import params
from .partial_state_update_block import partial_state_update_block
from .state_variables import initial_state

del configs[:]

sim_config = config_sim(
    {
        "N": 1,  # no. of sim runs
        "T": range(1),  # no. of times to run through PSUBs
        "M": params,
    }
)

exp = Experiment()
exp.append_model(
    sim_configs=sim_config,
    initial_state=initial_state,
    partial_state_update_blocks=partial_state_update_block,
)

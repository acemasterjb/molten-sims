from cadCAD import configs
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim

from .bonding_curve.model.params import params as bc_params
from .bonding_curve.model.state_variables import initial_state as bc_initial_state
from .bonding_curve.model.partial_state_update_block import partial_state_update_block as bc_psub
from .twap.model.params import params as twap_params
from .twap.model.partial_state_update_block import partial_state_update_block as twap_psub
from .twap.model.state_variables import initial_state as twap_initial_state

del configs[:]

sim_config_twap = config_sim(
    {
        "N": 1,  # no. of sim runs
        "T": range(1),  # no. of times to run through PSUBs
        "M": twap_params,
    }
)

sim_config_bc = config_sim(
    {
        "N": 1,  # no. of sim runs
        "T": range(1),  # no. of times to run through PSUBs
        "M": bc_params,
    }
)

exp = Experiment()

exp.append_model(
    sim_configs=sim_config_twap,
    initial_state=twap_initial_state,
    partial_state_update_blocks=twap_psub,
)
exp.append_model(
    sim_configs=sim_config_bc,
    initial_state=bc_initial_state,
    partial_state_update_blocks=bc_psub,
)

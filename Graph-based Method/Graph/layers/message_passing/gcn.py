"""Graph convolution neural network layer."""
from typing import Dict, List, Any

import tensorflow as tf

from .message_passing import MessagePassing, MessagePassingInput, register_message_passing_implementation
from .gnn_edge_mlp import GNN_Edge_MLP


@register_message_passing_implementation
class GCN(GNN_Edge_MLP):

    @classmethod
    def get_default_hyperparameters(cls):
        these_hypers = {
            "use_target_state_as_input": False,
            "normalize_by_num_incoming": True,
            "num_edge_MLP_hidden_layers": 0,

        }
        mp_hypers = super().get_default_hyperparameters()
        mp_hypers.update(these_hypers)
        return mp_hypers

    def __init__(self, params: Dict[str, Any], **kwargs):
        super(GCN, self).__init__(params, **kwargs)


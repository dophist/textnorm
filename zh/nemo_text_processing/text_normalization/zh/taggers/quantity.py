import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class QuantityFst(GraphFst):
    '''
        kg  千克
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="quantity", kind="classify", deterministic=deterministic)
        quant = pynini.string_file(get_abs_path("data/quantity/quantity.tsv"))
        quantity_graph = pynutil.insert("quantity: \"") + NumberFst().final_graph + quant + pynutil.insert(" \"")
        quantity_graph = self.add_tokens(quantity_graph)
        self.fst = quantity_graph.optimize()
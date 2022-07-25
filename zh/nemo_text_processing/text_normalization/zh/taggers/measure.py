import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst, delete_space
from nemo_text_processing.text_normalization.zh.utils import get_abs_path,load_labels
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class MeasureFst(GraphFst):
    '''
        TODO: the output of following case is not what this tagger actually produces
        also make sure to fix this kind of inconsistency in other places.
        1kg  -> measure { measure: "1kg" }
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="measure", kind="classify", deterministic=deterministic)

        units_en = pynini.string_file(get_abs_path("data/measure/units_en.tsv"))
        units_zh = pynini.string_file(get_abs_path("data/measure/units_zh.tsv"))

        graph_measure = self.add_tokens(
            pynutil.insert("measure: \"") + NumberFst().graph_number + delete_space + (units_en | units_zh) + pynutil.insert("\"")
        )

        self.fst = graph_measure.optimize()

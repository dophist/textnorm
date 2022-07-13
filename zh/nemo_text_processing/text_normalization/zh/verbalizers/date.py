import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, NEMO_NOT_QUOTE ,GraphFst
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class DateFst(GraphFst):
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="date", kind="verbalize", deterministic=deterministic)
        date = pynutil.delete('year: \"') + pynini.closure(NEMO_NOT_QUOTE) + pynutil.delete(' \"') 
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        digit_teen_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit_teen.tsv")))
        zero = pynini.invert(pynini.string_file(get_abs_path("data/number/zero.tsv")))
        zero_graph = pynini.cross("0","")
        year_graph = pynini.closure(digit_graph|zero,2,4)
        STR_TEEN = '十'
        digit_null_graph = digit_graph|zero_graph
        time_number_graph = (
             (digit_teen_graph + pynutil.insert(STR_TEEN) + digit_null_graph)|
            (zero_graph + digit_graph)
        )

        date_type1 = pynutil.delete("year: \"") + year_graph + pynutil.insert("年") + pynutil.delete(" \"") + " "\
                    + pynutil.delete("month: \"") + time_number_graph + pynutil.insert("月") + pynutil.delete(" \"") + " "\
                    + pynutil.delete("day: \"") + time_number_graph + pynutil.insert("日") + pynutil.delete(" \"")

        date_type2 = pynutil.delete("year: \"") + year_graph + pynutil.insert("年") + pynutil.delete(" \"") + " "\
                    + pynutil.delete("month: \"") + time_number_graph + pynutil.insert("月") + pynutil.delete(" \"")

        final_graph = date|date_type1|date_type2
        delete_tokens = self.delete_tokens(final_graph)
        self.fst = delete_tokens.optimize()

import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, GraphFst, insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class TimeFst(GraphFst):
    '''
        1:25
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="time", kind="verbalize", deterministic=deterministic)   
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        digit_teen_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit_teen.tsv")))
        zero_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/zero.tsv")))
        STR_TEEN = '十'
        digit_null_graph = digit_graph|pynini.cross('0','')
        time_number_graph = (
             (digit_teen_graph + pynutil.insert(STR_TEEN) + digit_null_graph)|
            (zero_graph + digit_graph)
        )
        all_zero_graph_none = pynini.cross("0","") + pynini.cross("0","")
        all_zero_graph = pynini.cross("00","零")
        clock_no_sec = pynutil.delete("hour: \"") + (time_number_graph|all_zero_graph|digit_graph) + pynutil.insert("点")+ pynutil.delete("\"") + " "\
                + pynutil.delete("min: \"") + (time_number_graph) + pynutil.insert("分") + pynutil.delete("\"")
        clock_no_min = pynutil.delete("hour: \"") + (time_number_graph|all_zero_graph|digit_graph) + pynutil.insert("点")+ pynutil.delete("\"") + " "\
                + pynutil.delete("min: \"") + (all_zero_graph_none) + pynutil.delete("\"")
        clock_with_sec = pynutil.delete("hour: \"") + (time_number_graph|all_zero_graph|digit_graph) + pynutil.insert("点")+ pynutil.delete("\"") + " "\
                + pynutil.delete("min: \"") + (time_number_graph|all_zero_graph)  + pynutil.insert("分")+ pynutil.delete("\"") + " "\
                + pynutil.delete("sec: \"") + (time_number_graph) + pynutil.insert("秒") + pynutil.delete("\"")
        clock_graph = clock_no_sec|clock_with_sec|clock_no_min


        
        final_graph = clock_graph
        final_graph = self.delete_tokens(final_graph)
        self.fst = final_graph.optimize()
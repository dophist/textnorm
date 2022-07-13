import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import GraphFst,insert_space,NEMO_DIGIT,NEMO_NOT_QUOTE
from nemo_text_processing.text_normalization.zh.taggers.number import NumberFst
from pynini.lib import pynutil
class TimeFst(GraphFst):
    '''
        1:02
        1:02:36
        2002/01/28
    '''
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="time", kind="classify", deterministic=deterministic)
        clock_hour = pynini.closure(NEMO_DIGIT,1) + (pynutil.delete(':')|pynutil.delete('-'))
        clock_min = pynini.closure(NEMO_DIGIT,2,2)
        clock_min_with_sec = pynini.closure(NEMO_DIGIT,2,2) +  (pynutil.delete(':')|pynutil.delete('-'))
        clock_second = pynini.closure(NEMO_DIGIT,1,2)
        clock_no_sec_graph = pynutil.insert("hour: \"") + clock_hour + pynutil.insert("\"")\
        + insert_space + pynutil.insert("min: \"") + clock_min + pynutil.insert("\"")
        clock_with_sec_graph = pynutil.insert("hour: \"") + clock_hour + pynutil.insert("\"")\
        + insert_space + pynutil.insert("min: \"") + clock_min_with_sec + pynutil.insert("\"")\
        + insert_space + pynutil.insert("sec: \"") + clock_second + pynutil.insert("\"")
        clock_graph = clock_no_sec_graph|clock_with_sec_graph

        time_graph = clock_graph
        time_graph = self.add_tokens(time_graph)
        self.fst = time_graph.optimize()
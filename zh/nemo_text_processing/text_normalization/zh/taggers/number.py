#!/usr/bin/env python3
# coding=utf-8
import pynini
from nemo_text_processing.text_normalization.zh.graph_utils import NEMO_SIGMA, NEMO_DIGIT, GraphFst, insert_space, NEMO_CHAR
from nemo_text_processing.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil
class NumberFst(GraphFst):
    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="number", kind="classify", deterministic=deterministic)
        STR_TEEN = '十'
        STR_HUND = '百'
        STR_THOU = '千'
        STR_WAN = '万'
        STR_YI = '亿'
        non_num = (NEMO_CHAR - NEMO_DIGIT) | pynini.accep(' ') 
        digit_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit.tsv")))
        zero_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/zero.tsv")))
        digit_teen_graph = pynini.invert(pynini.string_file(get_abs_path("data/number/digit_teen.tsv")))

        digit_z_graph = digit_graph|zero_graph
        digit_null_graph = digit_graph|pynini.cross('0','')
        digit_teen_graph = digit_teen_graph 
        u_teen_num_graph = (
            (digit_graph + pynutil.insert(STR_TEEN) + digit_null_graph)|
            (zero_graph + digit_graph)
        )
        teen_num_graph = (
            (digit_teen_graph + pynutil.insert(STR_TEEN) + digit_null_graph)|
            (zero_graph + digit_graph)
        )
        hund_num_graph = (
            (digit_graph + pynutil.insert(STR_HUND) + u_teen_num_graph)|
            (digit_graph + pynutil.insert(STR_HUND) + pynini.cross('0','')**2)
        )
        thou_num_graph = (
            ((digit_graph + pynutil.insert(STR_THOU) + hund_num_graph)|
            (digit_graph + pynutil.insert(STR_THOU) + zero_graph + digit_graph + pynutil.insert(STR_TEEN) + digit_null_graph)|
            (digit_graph + pynutil.insert(STR_THOU) + zero_graph + pynini.cross('0','') + digit_graph)|
            (digit_graph + pynutil.insert(STR_THOU) + pynini.cross('0','')**3))
        )
        wan_num_graph = (
            (thou_num_graph|hund_num_graph|teen_num_graph|digit_null_graph) + pynutil.insert(STR_WAN) + (thou_num_graph|
            (pynini.cross('0','') + pynutil.insert('零') + hund_num_graph)|(pynini.cross('0','')**2 + pynutil.insert('零') + (digit_graph + pynutil.insert(STR_TEEN) + digit_null_graph))|
            (pynini.cross('0','')**3 + pynutil.insert('零') + digit_graph))
        )
        long_num_graph = (
            pynini.closure(digit_z_graph,9)
        )
        graph = hund_num_graph | thou_num_graph | teen_num_graph | digit_z_graph | wan_num_graph | long_num_graph
        self.fst = non_num + graph + non_num
        self.fst = self.fst.optimize()
        
        
        





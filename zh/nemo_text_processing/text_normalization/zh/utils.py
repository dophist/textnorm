# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import os
import pynini
from pynini.lib import utf8

def get_abs_path(rel_path):
    """
    Get absolute path

    Args:
        rel_path: relative path to this file
        
    Returns absolute path
    """
    return os.path.dirname(os.path.abspath(__file__)) + '/' + rel_path


def load_labels(abs_path):
    """
    loads relative path file as dictionary

    Args:
        abs_path: absolute path

    Returns dictionary of mappings
    """
    label_tsv = open(abs_path, encoding="utf-8")
    labels = list(csv.reader(label_tsv, delimiter="\t"))
    return labels


def augment_labels_with_punct_at_end(labels):
    """
    augments labels: if key ends on a punctuation that value does not have, add a new label 
    where the value maintains the punctuation

    Args:
        labels : input labels
    Returns:
        additional labels
    """
    res = []
    for label in labels:
        if len(label) > 1:
            if label[0][-1] == "." and label[1][-1] != ".":
                res.append([label[0], label[1] + "."] + label[2:])
    return res


def chr_sep(line):
    m = '' 
    for i,chr in enumerate(line):
        if '\u4e00' <= chr <= '\u9fa5' or '\uff01' <= chr <= '\uff5e':
            if i+1 < len(line) and ('\u4e00' <= line[i+1] <= '\u9fa5' or '\uff01' <= line[i+1] <= '\uff5e'):
                m+=' ' + chr
            else:
                m+=' ' + chr + ' '
            
        else:
            m+=chr
    m = ' ' + m + ' '
    return m
    
def pre_process(line):
    money_list = ['￥','$','USD','€','EUR','￡','J￥','JPY￥','HK$','HKD','AUD','A$','SUR','DEM','DM','FRF','CAD','CAD$','FRF']
    res = ''
    for word in line.split():
        if word[0] in money_list:
            word = word[1:] + word[0]
        if '/' in word:
            items = word.split('/')
            word = items[1] + '/' + items[0]
        res += word + ' '
    return res
    
def normalize(line,fst):
    line = chr_sep(line)
    line = ' ' + pre_process(line)
    res = (line @ fst).string()
    return res.replace(' ','')

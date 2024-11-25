#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-fish_blocks author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class vector_sink(gr.sync_block):
    """
    ur a nerd
    """
    def __init__(self, vector_len=1024, in_num=4):
        gr.sync_block.__init__(self,
            name="Vector Sink",
            in_sig=[(np.complex64, vector_len)] * in_num,
            out_sig=None
        )
        
        self.vector_len = vector_len
        self.in_num = in_num
        self.list = []


    def work(self, input_items, output_items):
        inputs = np.stack([input_items[i][0] for i in range(self.in_num)], axis=0).astype(np.complex64)  
        self.list = inputs
            
        return len(input_items[0])
    
    
    def get_data(self):
        return self.list


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Fish.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from collections import deque
import threading

class vector_sink(gr.sync_block):
    """
    ur a nerd
    """
    def __init__(self, vector_len=1024, in_num=4, in_type='complex', buff=False, buff_count=10):
        if in_type=='complex':
            in_t=np.complex64
        elif in_type=='float':
            in_t=np.float32
        elif in_type=='int':
            in_t=np.int32
        else:
            raise ValueError(f"Unsupported in_type: {in_type}")

        gr.sync_block.__init__(self,
            name="Vector Sink",
            in_sig=[(in_t, vector_len)] * in_num,
            out_sig=None
        )
        
        self.vector_len = vector_len
        self.in_num = in_num
        self.in_type = in_t
        self.buff = buff
        self.buff_count = buff_count

        self.list = []
        self.lock = threading.Lock()
        
        if self.buff:
            self.buffer = deque(maxlen=self.buff_count)
            self.buff_len = 0  
        else:
            self.buff_len = 1  


    def work(self, input_items, output_items):
        inputs = np.stack([input_items[i][0] for i in range(self.in_num)], axis=0).astype(self.in_type)
        
        with self.lock:
            if self.buff:
                self.buffer.append(inputs)
                self.buff_len = len(self.buffer)
            else:
                self.list = inputs
                self.buff_len = 1

            return len(input_items[0])

    
    def get_data(self, clear_buffer):
        if self.buff:
            data = list(self.buffer)
            if clear_buffer:
                self.buffer.clear()
                self.buff_len = 0
            return data
        else:
            return self.list




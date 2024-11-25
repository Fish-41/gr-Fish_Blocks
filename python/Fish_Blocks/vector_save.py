#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-fish_blocks author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class vector_save(gr.sync_block):
    """
    kinda cringe
    """
    def __init__(self, vector_len=1024, in_num=4, file_location='/folder/your_file.npz', data_size=1000, collect_data=True, save_data=True):
        gr.sync_block.__init__(self,
            name="Vector Save",
            in_sig=[(np.complex64, vector_len)] * in_num,
            out_sig=None
        )
        
        self.vector_len = vector_len
        self.in_num = in_num
        self.data_size = data_size
        self.collect_data = collect_data
        self.save_data = save_data
        self.file_location = file_location
        
        self.collected_data = False
        
        self.list = []
        self.data = np.zeros((self.data_size, self.in_num, self.vector_len), dtype=np.complex64)



    def work(self, input_items, output_items):
        inputs = np.stack([input_items[i][0] for i in range(self.in_num)], axis=0).astype(np.complex64)  
        self.list = inputs
        
        if self.collect_data:
            if len(self.data) == 0:
                print('\nCollecting Data')
            
            if len(self.data) == self.data_size:
                self.collect_data = False
                self.collected_data = True
                print('\nCollected Data')
                
            else:
                self.data[len(self.data)] = inputs
        
        elif self.collected_data and self.save_data:
            np.savez(self.file_location, self.data)
            self.save_data = False
            print('\nData Saved')
                
        return len(input_items[0])
    
    def set_collect_data(self, collect_data):
        self.collect_data = collect_data
    
    def set_save_data(self, save_data):
        self.save_data = save_data
        
    def get_data(self):
        return self.data


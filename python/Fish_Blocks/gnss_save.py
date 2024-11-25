#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 gr-fish_blocks author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class gnss_save(gr.sync_block):
    """
    weirdo
    """
    def __init__(self, vector_len=1024, in_num=4, file_location='/folder/your_file.npz', data_size=1000, collect_data=True):
        gr.sync_block.__init__(self,
            name="GNSS Save",
            in_sig=[(np.complex64, vector_len)] * in_num,
            out_sig=None
        )
        
        self.vector_len = vector_len
        self.in_num = in_num
        self.data_size = data_size
        self.collect_data = collect_data
        self.file_location = file_location
        
        self.collected_data = False
        self.save_data = True  # Controls whether to save after collection
        
        self.current_index = 0
        # Initialize data storage with complex64 to match incoming data
        self.data = np.zeros((self.data_size, self.in_num, self.vector_len), dtype=np.complex64)
        
        # Open the file in write-binary mode
        try:
            self.file = open(self.file_location, 'wb')
            print(f"Opened file for writing: {self.file_location}")
        except IOError as e:
            print(f"Failed to open file {self.file_location}: {e}")
            self.collect_data = False  # Prevent data collection if file can't be opened

    def work(self, input_items, output_items):
        # Stack inputs: shape becomes (in_num, vector_len)
        inputs = np.stack([input_items[i][0] for i in range(self.in_num)], axis=0).astype(np.complex64)
        
        if self.collect_data:
            if self.current_index == 0:
                print('\nCollecting Data')
            
            # Store the input data
            self.data[self.current_index] = inputs
            self.current_index += 1
            
            # Check if we've collected enough data
            if self.current_index >= self.data_size:
                self.collect_data = False
                self.collected_data = True
                print('\nCollected Data')
                
        if self.collected_data and self.save_data:
            print('\nSaving Data')
            # Flatten the data to a 1D array: shape becomes (data_size * in_num * vector_len,)
            data_flat = self.data.reshape(-1)
            scale = 32767  # Max value for int16
            
            # Scale and convert to int16
            real_int16 = (np.real(data_flat) * scale).astype(np.int16)
            imag_int16 = (np.imag(data_flat) * scale).astype(np.int16)
            
            # Interleave I and Q samples
            interleaved = np.empty((real_int16.size + imag_int16.size,), dtype=np.int16)
            interleaved[0::2] = real_int16
            interleaved[1::2] = imag_int16
            
            # Write the interleaved data to the file
            try:
                interleaved.tofile(self.file)
                print('\nData Saved')
            except IOError as e:
                print(f"Failed to write data to file: {e}")
            
            self.save_data = False  # Ensure data is saved only once
                
        return len(input_items[0])
    
    def set_collect_data(self, collect_data):
        self.collect_data = collect_data
        

    def stop(self):
        # Close the file when the flowgraph stops
        try:
            self.file.close()
            print(f"Closed file: {self.file_location}")
        except AttributeError:
            # self.file might not have been created if file opening failed
            pass
        return gr.sync_block.stop(self)


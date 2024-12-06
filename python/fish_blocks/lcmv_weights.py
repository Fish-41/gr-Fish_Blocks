#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Fish.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import threading

class lcmv_weights(gr.sync_block):
    """
    ur kinda weird
    """
    def __init__(self, nr=4, beam_val = 1, spacing=0.5, nulls=False, beam_pos=[], null_pos=[]):
        gr.sync_block.__init__(self,
            name="Vector Sink",
            in_sig=None,
            out_sig=None
        )
        
        self.nr = nr
        self.beam_val = beam_val
        self.nulls = nulls
        self.null_pos = null_pos
        self.beam_pos = beam_pos
        self.spacing = spacing
        
        self.epsilon = 1e-12
        
        self.Nr = self.nr

        self.array_indices = np.arange(self.Nr).reshape(-1, 1)
        self.beam_list = []
        self.null_list = []
        self.f_list = []
        
        self.update_steer()


    def work(self, input_items, output_items):
        with self.lock:
            if self.up_flag:
                self.update_steer()

        return len(input_items[0])
    


    def set_beam_pos(self, beam_pos):
        self.beam_pos = beam_pos
        self.update_steer()
        
    def set_null_pos(self, null_pos):
        self.null_pos = null_pos
        self.update_steer()
        
    def update_steer(self):
        self.beam_list = []
        self.null_list = []
        self.f_list = []
        
        for ang in self.beam_pos:
            self.beam_list.append(np.exp(-2j * np.pi * self.spacing * self.array_indices * np.sin(np.radians(ang))).reshape(-1,1))
            self.f_list.append(self.beam_val)
        
        if self.nulls:
            for ang in self.null_pos:
                self.null_list.append(np.exp(-2j * np.pi * self.spacing * self.array_indices * np.sin(np.radians(ang))).reshape(-1,1))
                self.f_list.append(0)
            self.beam_list.extend(self.null_list)
        self.f = np.array(self.f_list)
        self.s = np.hstack(self.beam_list)
        

    def get_weights(self):
        Xn = np.random.rand(self.Nr, 1024) + 1j*np.random.rand(self.Nr, 1024)
        Rn = np.cov(Xn)
        R_inv = np.linalg.pinv(Rn)
        
        w = R_inv @ self.s @ np.linalg.pinv(self.s.conj().T @ R_inv @ self.s) @ self.f
        w = w.squeeze()
        w = np.conj(w) 
        w_mag = np.absolute(w)
        w_ph = np.rad2deg(np.angle(w))
        print(w_mag, w_ph)
        return w_mag, w_ph


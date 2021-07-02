#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-electrosense author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
import pmt
from gnuradio import gr

class variable_updater(gr.basic_block):
    """
    docstring for block variable_updater
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="variable_updater",
            in_sig=[<+numpy.float32+>, ],
            out_sig=[<+numpy.float32+>, ])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.commdict = {"freq": lambda x: self.lserv.set_cfreq(float(x)),
                         "alpha": lambda x: self.lserv.set_alpha(float(x)),
                         "ppm": lambda x: self.lserv.set_ppm(float(x)),
                         "rfgain": lambda x: self.lserv.set_rfgain(int(x)),
                         "tune_delay": lambda x: self.lserv.set_tune_delay(float(x)),
                        }

    def register_instance(self,tb):
        self.lserv = tb

    def handle_msg(self, msg_pmt):
        msg = pmt.to_python(msg_pmt)
        if self.commdict.has_key(msg[0]):
            try:
                self.commdict[msg[0]](msg[1])
                print("Updating: ", msg)
            except:
                print("Updating failed: ", msg)

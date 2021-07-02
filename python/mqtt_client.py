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
import paho.mqtt.client as mqtt

class mqtt_client(gr.basic_block):
    """
    docstring for block mqtt_client
    """
    def __init__(self, server, port, channel, ca_cert=None, certfile=None, keyfile=None):
        gr.basic_block.__init__(self,
            name="mqtt_client",
            in_sig=[<+numpy.float32+>, ],
            out_sig=[<+numpy.float32+>, ])

        # Register the message port
        self.message_port_register_out(pmt.intern('out'))
        self.server = server
        self.port   = port
        self.channel = channel
        self.ca_cert = ca_cert
        self.certfile = certfile 
        self.keyfile = keyfile 

        self.connect()

    def connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        if self.ca_cert:
            self.client.tls_set(self.ca_cert, certfile=self.certfile, keyfile=self.keyfile)
        self.client.on_message = self.on_message
        self.client.connect(self.server, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.channel+"/#")

    def on_message(self, client, userdata, msg):
        data = msg.payload.split(",")
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.intern(data[0]), pmt.intern(data[1])))


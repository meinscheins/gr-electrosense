#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
import pmt
import avro.schema
import avro.io
from gnuradio import gr
import paho.mqtt.client as mqtt

class mqtt_client(gr.basic_block):
    """
    docstring for block mqtt_client
    """
    def __init__(self, server, port, senid, avrofile, ca_cert=None, certfile=None, keyfile=None):
        gr.basic_block.__init__(self,
            name="mqtt_client",
            in_sig=[],
            out_sig=[])

        # Register the message port
        self.message_port_register_out(pmt.intern('out'))
        self.server = server
        self.port   = port
        self.ca_cert = ca_cert
        self.certfile = certfile
        self.keyfile = keyfile
        self.senid = senid
        self.avrofile = avrofile

        self.schema = avro.schema.Parse(open(avrofile).read())
        self.reader = DatumReader(schema)

        self.connect()

    def connect(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("sensor", "sensor")
        self.client.on_connect = self.on_connect
        if self.ca_cert:
            self.client.tls_set(self.ca_cert, certfile=self.certfile, keyfile=self.keyfile, tls_version=2)
        self.client.on_message = self.on_message

        # INSECURE !!!
        self.client.tls_insecure_set(True)
        # INSECURE !!!
        
        self.client.connect(self.server, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        topics = [("control/sensor/all", 0), ("control/sensor/id/" + str(self.senid), 0)]
        self.client.subscribe(topics)

    def on_message(self, client, userdata, msg):
        print(decode_message(msg.payload))
        variable_name = ""
        variable_content = ""
        #self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.intern(variable_name), pmt.intern(variable_content)))

    def decode_message(self, message):
        message_bytes = io.BytesIO(message)
        decoder = BinaryDecoder(message_bytes)
        event_dict = reader.read(decoder)
        return event_dict
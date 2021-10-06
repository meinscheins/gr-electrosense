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

import datetime
import time
import psutil
import numpy
import pmt
import avro.schema
import avro.io
import io
import paho.mqtt.client as mqtt
from gnuradio import gr

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
        self.status = "IDLE"
        self.status_info = {}

        self.schema = avro.schema.Parse(open(avrofile).read())
        self.reader = avro.io.DatumReader(self.schema)

        self.connect()

    def _handle_status_request(self, msg):
        # type = SENSORSTATUS
        if msg["Type"] == "SENSORSTATUS":
            msg = {"SerialNumber": self.serial_number,
                "Timestamp": current_timestamp(),
               "Uptime": int(time.mktime(datetime.datetime.now().timetuple()) - psutil.boot_time()),
               "Status": self.status,
               "StatusInfo": self.status_info}
            self.send_message("SensorStatus", msg, "sensor/status/{}".format(self.senid))
            

    def connect(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("sensor", "sensor")
        self.client.on_connect = self.on_connect
        if self.ca_cert:
            self.client.tls_set(self.ca_cert, certfile=self.certfile, keyfile=self.keyfile, tls_version=2)
        self.client.on_message = self.on_message

        self.client.connect(self.server, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        topics = [("control/sensor/all", 0), ("control/sensor/id/" + str(self.senid), 0)]
        self.client.subscribe(topics)

    def on_message(self, client, userdata, msg):
        decoded_message = self.decode_message(msg.payload)

        # Type = StatusRequest
        if decoded_message["Type"] == "StatusRequest":
            self._handle_status_request(decoded_message["Message"])


        # Connector to GNURadio
        variable_name = ""
        variable_content = ""
        #self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.intern(variable_name), pmt.intern(variable_content)))

    def send_message(self, msg_type, data, topic):
        print(data)
        msg = self.parser.encode_message(msg_type, data)
        print(msg)
        #self.client.publish(topic, msg, 0)

    def decode_message(self, message):
        message_bytes = io.BytesIO(message)
        decoder = avro.io.BinaryDecoder(message_bytes)
        event_dict = self.reader.read(decoder)
        return event_dict

    def encode_message(self, message_type, data):
        """Create an Avro record with fields type = messageType and message = data
        Encapsulation ensures that the decoder can infer the schema based on the `type` field
        """
        buf = io.BytesIO()
        encoder = BinaryEncoder(buf)
        writer = DatumWriter(self.schema)
        writer.write({"Type": message_type, "Message": data}, encoder)
        msg = bytearray(buf.getvalue())
        buf.close()
        return msg

    def current_timestamp():
        return int(time.mktime(datetime.datetime.now().timetuple()))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-electrosense author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import time
import datetime
import psutil

class message_handler:
    def __init__(self, send_message_function, update_variable_function, senid):
        self.send_message = send_message_function
        self.update_variable = update_variable_function
        self.senid = senid
        self.status = "IDLE"
        self.status_info = {}

    def handle_status_request(self, msg):
        # type = SENSORSTATUS
        if msg["Type"] == "SENSORSTATUS":
            msg = {"SerialNumber": self.senid,
                "Timestamp": self.current_timestamp(),
               "Uptime": int(time.mktime(datetime.datetime.now().timetuple()) - psutil.boot_time()),
               "Status": self.status,
               "StatusInfo": self.status_info}
            self.send_message("SensorStatus", msg, "sensor/status/{}".format(self.senid))

    def handle_measurement_command(self, msg):
        # type = SENSORSTATUS
        if msg["Command"] == "START":
            self.status = "BUSY"
            params = msg["SensingParams"]
            # updating parameter
            for parameter in params:
                self.update_variable(parameter, params[parameter])
            
            # command running with updated parameters
            self.status = "SENSING"
        elif msg["Command"] == "STOP":
            self.status = "IDLE"


    def current_timestamp(self):
        return int(time.mktime(datetime.datetime.now().timetuple()))
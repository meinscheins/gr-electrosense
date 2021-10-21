#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-electrosense author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

class sensor_manager:
    def __init__(self):
        self.status = "IDLE"
        self.status_info = {}

    def _handle_status_request(self, msg):
        # type = SENSORSTATUS
        if msg["Type"] == "SENSORSTATUS":
            msg = {"SerialNumber": self.senid,
                "Timestamp": self.current_timestamp(),
               "Uptime": int(time.mktime(datetime.datetime.now().timetuple()) - psutil.boot_time()),
               "Status": self.status,
               "StatusInfo": self.status_info}
            self.send_message("SensorStatus", msg, "sensor/status/{}".format(self.senid))

    def current_timestamp(self):
        return int(time.mktime(datetime.datetime.now().timetuple()))
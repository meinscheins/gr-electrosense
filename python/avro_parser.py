#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-electrosense author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import avro.schema
import avro.io
import io

class avro_parser:
    def __init__(self, avrofile):
        self.avrofile = avrofile

        self.schema = avro.schema.Parse(open(avrofile).read())
        self.reader = avro.io.DatumReader(self.schema)
        self.writer = avro.io.DatumWriter(self.schema)

    def decode_message(self, message):
        message_bytes = io.BytesIO(message)
        decoder = avro.io.BinaryDecoder(message_bytes)
        message_dict = self.reader.read(decoder)

        return message_dict

    def encode_message(self, message_type, data):
        buf = io.BytesIO()
        encoder = avro.io.BinaryEncoder(buf)
        self.writer.write({"Type": message_type, "Message": data}, encoder)
        encoded_message = bytearray(buf.getvalue())
        buf.close()

        return encoded_message
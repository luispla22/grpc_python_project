# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gps_1403.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0egps_1403.proto\x12\x08gps_1403\x1a\x1fgoogle/protobuf/timestamp.proto\"I\n\x07\x44\x61taGPS\x12\x0f\n\x07payload\x18\x01 \x01(\t\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x07\n\x05\x45mpty2E\n\x0e\x44\x61taGPSService\x12\x33\n\x0bSendGPSData\x12\x11.gps_1403.DataGPS\x1a\x11.gps_1403.DataGPSb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gps_1403_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DATAGPS']._serialized_start=61
  _globals['_DATAGPS']._serialized_end=134
  _globals['_EMPTY']._serialized_start=136
  _globals['_EMPTY']._serialized_end=143
  _globals['_DATAGPSSERVICE']._serialized_start=145
  _globals['_DATAGPSSERVICE']._serialized_end=214
# @@protoc_insertion_point(module_scope)

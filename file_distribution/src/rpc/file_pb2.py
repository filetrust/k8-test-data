# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="file.proto",
    package="",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\nfile.proto"(\n\x05Input\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x11\n\tnum_files\x18\x02 \x01(\x05"\x18\n\x08Response\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x32,\n\x04\x46ile\x12$\n\rMaliciousFile\x12\x06.Input\x1a\t.Response"\x00\x62\x06proto3',
)


_INPUT = _descriptor.Descriptor(
    name="Input",
    full_name="Input",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="type",
            full_name="Input.type",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="num_files",
            full_name="Input.num_files",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=14,
    serialized_end=54,
)


_RESPONSE = _descriptor.Descriptor(
    name="Response",
    full_name="Response",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="data",
            full_name="Response.data",
            index=0,
            number=2,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=56,
    serialized_end=80,
)

DESCRIPTOR.message_types_by_name["Input"] = _INPUT
DESCRIPTOR.message_types_by_name["Response"] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Input = _reflection.GeneratedProtocolMessageType(
    "Input",
    (_message.Message,),
    {
        "DESCRIPTOR": _INPUT,
        "__module__": "file_pb2"
        # @@protoc_insertion_point(class_scope:Input)
    },
)
_sym_db.RegisterMessage(Input)

Response = _reflection.GeneratedProtocolMessageType(
    "Response",
    (_message.Message,),
    {
        "DESCRIPTOR": _RESPONSE,
        "__module__": "file_pb2"
        # @@protoc_insertion_point(class_scope:Response)
    },
)
_sym_db.RegisterMessage(Response)


_FILE = _descriptor.ServiceDescriptor(
    name="File",
    full_name="File",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=82,
    serialized_end=126,
    methods=[
        _descriptor.MethodDescriptor(
            name="MaliciousFile",
            full_name="File.MaliciousFile",
            index=0,
            containing_service=None,
            input_type=_INPUT,
            output_type=_RESPONSE,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_FILE)

DESCRIPTOR.services_by_name["File"] = _FILE

# @@protoc_insertion_point(module_scope)

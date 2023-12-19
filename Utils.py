import sys

def little_to_big_endian_16(value):
    return ((value << 8) & 0xFF00) | ((value >> 8) & 0xFF)

def little_to_big_endian_32(value):
    return ((value << 24) & 0xFF000000) | ((value << 8) & 0x00FF0000) | ((value >> 8) & 0x0000FF00) | ((value >> 24) & 0x000000FF)

def is_little_endian():
    test_value = 0x12345678
    return sys.byteorder == 'little'
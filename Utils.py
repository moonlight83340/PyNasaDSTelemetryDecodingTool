import sys

## value in little endian to big endian
#  @param value a uint16_t value to convert in big endian
def little_to_big_endian_16(value):
    return ((value << 8) & 0xFF00) | ((value >> 8) & 0xFF)
    
## value in little endian to big endian
#  @param value a uint32_t value to convert in big endian
def little_to_big_endian_32(value):
    return ((value << 24) & 0xFF000000) | ((value << 8) & 0x00FF0000) | ((value >> 8) & 0x0000FF00) | ((value >> 24) & 0x000000FF)
    
## check if PC is in little endian or big endian
def is_little_endian():
    test_value = 0x12345678
    return sys.byteorder == 'little'
    
## convert a bytes array to decimal
#  @param bytes a bytes array of size 2 to convert in a uint16_t
def convert_to_decimal(bytes):
    return (bytes[0] << 8) | bytes[1]
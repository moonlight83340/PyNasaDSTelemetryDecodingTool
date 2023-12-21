import struct
import ctypes
import datetime
import Utils
import argparse

#Maximum length for an absolute path name
OS_MAX_PATH_LEN = 32

## HK CCSDS_PrimaryHeader_t struct
class CCSDS_PrimaryHeader_t(ctypes.Structure):
    _fields_ = [
        ('StreamId', ctypes.c_uint8 * 2),  # packet identifier word (stream ID)
        ('Sequence', ctypes.c_uint8 * 2),  # packet sequence word
        ('Length', ctypes.c_uint8 * 2)     # packet length word
    ]

## HK CFE_MSG_TelemetrySecondaryHeader_t struct
class CFE_MSG_TelemetrySecondaryHeader_t(ctypes.Structure):
    _fields_ = [
        ('Time', ctypes.c_uint8 * 6)  # Time, big endian: 4 byte seconds, 2 byte subseconds
    ]
 
## HK DS_HkTlm_Payload_t struct 
class DS_HkTlm_Payload_t(ctypes.Structure):
    _fields_ = [
        ('CmdAcceptedCounter', ctypes.c_uint8),
        ('CmdRejectedCounter', ctypes.c_uint8),
        ('DestTblLoadCounter', ctypes.c_uint8),
        ('DestTblErrCounter', ctypes.c_uint8),
        ('FilterTblLoadCounter', ctypes.c_uint8),
        ('FilterTblErrCounter', ctypes.c_uint8),
        ('AppEnableState', ctypes.c_uint8),
        ('Spare8', ctypes.c_uint8),
        ('FileWriteCounter', ctypes.c_uint16),
        ('FileWriteErrCounter', ctypes.c_uint16),
        ('FileUpdateCounter', ctypes.c_uint16),
        ('FileUpdateErrCounter', ctypes.c_uint16),
        ('DisabledPktCounter', ctypes.c_uint32),
        ('IgnoredPktCounter', ctypes.c_uint32),
        ('FilteredPktCounter', ctypes.c_uint32),
        ('PassedPktCounter', ctypes.c_uint32),
        ('FilterTblFilename', ctypes.c_char * OS_MAX_PATH_LEN)
    ]

## HK TelemetrySecondaryHeaderTime struct 
class TelemetrySecondaryHeaderTime:
    def __init__(self, seconds=0, sub_seconds=0):
        self.seconds = seconds
        self.sub_seconds = sub_seconds

## DS HK
def get_telemetry_secondary_header_time(secondary_header):
    time = TelemetrySecondaryHeaderTime()
    time.seconds = 0
    for i in range(4):
        time.seconds |= secondary_header.Time[i] << ((3 - i) * 8)
    time.sub_seconds = (secondary_header.Time[4] << 8) | secondary_header.Time[5]
    return time

## get the utc time from J2000 point
def get_packet_datestamp_in_utc_time_from_j2000_time(seconds, sub_seconds):
    # J2000.0 in UTC
    j2000_time = datetime.datetime(2000, 1, 1, 11, 58, 55)

    # Add milliseconds to J2000.0 date
    j2000_time += datetime.timedelta(milliseconds=816)

    # Calculate the date with seconds and subseconds
    new_time = j2000_time + datetime.timedelta(seconds=seconds, milliseconds=sub_seconds)

    return new_time

## DS HK Telemetry decoder class
class DSHKTelemetryDecoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.packets = []
    ## Process the binary file to read the HK telemetry
    def process_binary_file(self):
        with open(self.file_path, 'rb') as file:
            buffer = file.read()
            file_cursor = 0

            while file_cursor < len(buffer):
                current_packet = {}

                primary_header_size = ctypes.sizeof(CCSDS_PrimaryHeader_t)
                primary_header = CCSDS_PrimaryHeader_t.from_buffer_copy(buffer[file_cursor:file_cursor + primary_header_size])
                current_packet['primary_header'] = primary_header
                file_cursor += primary_header_size

                secondary_header_present = primary_header.StreamId[1] & 0x20
                if secondary_header_present:
                    secondary_header_size = ctypes.sizeof(CFE_MSG_TelemetrySecondaryHeader_t)
                    secondary_header = CFE_MSG_TelemetrySecondaryHeader_t.from_buffer_copy(buffer[file_cursor:file_cursor + secondary_header_size])
                    file_cursor += secondary_header_size
                    current_packet['secondary_header'] = secondary_header

                payload_size = ctypes.sizeof(DS_HkTlm_Payload_t)
                payload = DS_HkTlm_Payload_t.from_buffer_copy(buffer[file_cursor:file_cursor + payload_size])
                file_cursor += payload_size
                
                # Assuming the data is in little-endian, performing conversion to big-endian
                if Utils.is_little_endian():
                    payload.FileWriteCounter = Utils.little_to_big_endian_16(payload.FileWriteCounter)
                    payload.FileWriteErrCounter = Utils.little_to_big_endian_16(payload.FileWriteErrCounter)
                    payload.FileUpdateCounter = Utils.little_to_big_endian_16(payload.FileUpdateCounter)
                    payload.FileUpdateErrCounter = Utils.little_to_big_endian_16(payload.FileUpdateErrCounter)
                    payload.DisabledPktCounter = Utils.little_to_big_endian_32(payload.DisabledPktCounter)
                    payload.IgnoredPktCounter = Utils.little_to_big_endian_32(payload.IgnoredPktCounter)
                    payload.FilteredPktCounter = Utils.little_to_big_endian_32(payload.FilteredPktCounter)
                    payload.PassedPktCounter = Utils.little_to_big_endian_32(payload.PassedPktCounter)
                
                current_packet['payload'] = payload

                self.packets.append(current_packet)
                
    ## show the packets value
    def show_packets(self):
        for packet in self.packets:
            print("Packet:")
            primary_header = packet['primary_header']
            stream_id = Utils.convert_to_decimal(primary_header.StreamId)
            sequence = Utils.convert_to_decimal(primary_header.Sequence)
            length = Utils.convert_to_decimal(primary_header.Length)
            
            applicationID = stream_id & 0x07FF
            secondaryHeaderPresent = (stream_id & 0x0800) >> 11
            packetType = (stream_id & 0x1000) >> 12
            ccsdsVersion = (stream_id & 0xE000) >> 13

            sequenceCount = sequence & 0x3FFF
            segmentationFlags = (sequence & 0xC000) >> 14

            print(f"Application ID: {applicationID}")
            print(f"Secondary Header: {secondaryHeaderPresent}")
            print(f"Packet Type: {packetType}")
            print(f"CCSDS Version: {ccsdsVersion}")
            print(f"sequence Count: {sequenceCount}")
            print(f"segmentation Flags: {segmentationFlags}")
            print(f"length: {length}")
            
            if 'secondary_header' in packet:
                telemetry_time = get_telemetry_secondary_header_time(packet['secondary_header'])
                print("Seconds:", telemetry_time.seconds)
                print("Subseconds:", telemetry_time.sub_seconds)
                utc_date_time = get_packet_datestamp_in_utc_time_from_j2000_time(telemetry_time.seconds, telemetry_time.sub_seconds)
                    # Display the new date in UTC format
                utc_time = utc_date_time.strftime("%Y-%m-%d %H:%M:%S")
                milliseconds = (utc_date_time.microsecond // 1000) % 1000
                print(f"Date/Time: {utc_time}.{milliseconds} UTC")
            payload = packet['payload']
            print("CmdAcceptedCounter:", payload.CmdAcceptedCounter)
            print("CmdRejectedCounter:", payload.CmdRejectedCounter)
            print("DestTblLoadCounter:", payload.DestTblLoadCounter)
            print("DestTblErrCounter:", payload.DestTblErrCounter)
            print("FilterTblLoadCounter:", payload.FilterTblLoadCounter)
            print("FilterTblErrCounter:", payload.FilterTblErrCounter)
            print("AppEnableState:", payload.AppEnableState)
            print("FileWriteCounter:", payload.FileWriteCounter)
            print("FileWriteErrCounter:", payload.FileWriteErrCounter)
            print("FileUpdateCounter:", payload.FileUpdateCounter)
            print("FileUpdateErrCounter:", payload.FileUpdateErrCounter)
            print("DisabledPktCounter:", payload.DisabledPktCounter)
            print("IgnoredPktCounter:", payload.IgnoredPktCounter)
            print("FilteredPktCounter:", payload.FilteredPktCounter)
            print("PassedPktCounter:", payload.PassedPktCounter)
            print("FilterTblFilename:", payload.FilterTblFilename)

def main():
    if Utils.is_little_endian():
        print("The machine is little endian")
    else:
        print("The machine is big endian")
    parser = argparse.ArgumentParser(description='DS-HK Telemetry decoder python version')
    parser.add_argument('command', choices=['run'], help='Command to execute')
    parser.add_argument('file_path', type=str, help='Path to the file')
    args = parser.parse_args()
    if args.command == 'run':
        decoder = DSHKTelemetryDecoder(args.file_path)
        decoder.process_binary_file()
        decoder.show_packets()
    else:
        print('Unknown command')

if __name__ == "__main__":
    main()

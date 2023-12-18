import struct
from datetime import datetime, timedelta

class DSHKTelemetryDecoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.packets = []

    def process_binary_file(self):
        with open(self.file_path, 'rb') as file:
            buffer = file.read()

            file_cursor = 0
            while file_cursor < len(buffer):
                current_packet = {}

                primary_header_size = struct.calcsize('!HBBB')
                primary_header = struct.unpack('!HBBB', buffer[file_cursor:file_cursor + primary_header_size])
                file_cursor += primary_header_size
                secondary_header_present = primary_header[1] & 0x20

                if secondary_header_present:
                    secondary_header_size = struct.calcsize('!4B2H')
                    secondary_header = struct.unpack('!4B2H', buffer[file_cursor:file_cursor + secondary_header_size])
                    file_cursor += secondary_header_size
                    current_packet['secondary_header'] = secondary_header

                payload_size = struct.calcsize('!10I')
                payload = struct.unpack('!10I', buffer[file_cursor:file_cursor + payload_size])
                file_cursor += payload_size
                current_packet['payload'] = payload

                self.packets.append(current_packet)

    def show_packets(self):
        for packet in self.packets:
            print("Packet:")
            if 'secondary_header' in packet:
                print("Secondary Header:", packet['secondary_header'])
            print("Payload:", packet['payload'])

    @staticmethod
    def get_packet_datestamp_in_utc_time_from_j2000_time(seconds, sub_seconds):
        j2000_epoch = datetime(year=2000, month=1, day=1, hour=11, minute=58, second=55)
        j2000_time = j2000_epoch + timedelta(seconds=seconds, milliseconds=sub_seconds)
        utc_time = j2000_time.strftime('%Y-%m-%d %H:%M:%S.%f') + " UTC"
        return utc_time

# Example usage
file_path = "C:/Users/perrotg/Documents/GitHub/NasaDSTelemetryDecodingTool/TestFile/ds_tlm.bin"
decoder = DSHKTelemetryDecoder(file_path)
decoder.process_binary_file()
decoder.show_packets()

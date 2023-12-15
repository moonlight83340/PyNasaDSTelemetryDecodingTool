import struct

# Maximum length for an absolute path name
OS_MAX_PATH_LEN = 32

class DS_HkTlm_Payload_t:
    def __init__(self):
        self.CmdAcceptedCounter = 0
        self.CmdRejectedCounter = 0
        self.DestTblLoadCounter = 0
        self.DestTblErrCounter = 0
        self.FilterTblLoadCounter = 0
        self.FilterTblErrCounter = 0
        self.AppEnableState = 0
        self.Spare8 = 0
        self.FileWriteCounter = 0
        self.FileWriteErrCounter = 0
        self.FileUpdateCounter = 0
        self.FileUpdateErrCounter = 0
        self.DisabledPktCounter = 0
        self.IgnoredPktCounter = 0
        self.FilteredPktCounter = 0
        self.PassedPktCounter = 0
        self.FilterTblFilename = b''

class CCSDS_PrimaryHeader_t:
    def __init__(self):
        self.StreamId = [0, 0]
        self.Sequence = [0, 0]
        self.Length = [0, 0]

class CFE_MSG_TelemetrySecondaryHeader_t:
    def __init__(self):
        self.Time = [0, 0, 0, 0, 0, 0]

class CCSDS_SpacePacket_t:
    def __init__(self):
        self.Pri = CCSDS_PrimaryHeader_t()

class CFE_MSG_Message_t:
    def __init__(self):
        self.CCSDS = CCSDS_SpacePacket_t()
        self.Byte = bytearray()

class CFE_MSG_TelemetryHeader_t:
    def __init__(self):
        self.Msg = CFE_MSG_Message_t()
        self.Sec = CFE_MSG_TelemetrySecondaryHeader_t()

class DS_HkPacket_t:
    def __init__(self):
        self.TelemetryHeader = CFE_MSG_TelemetryHeader_t()
        self.Payload = DS_HkTlm_Payload_t()

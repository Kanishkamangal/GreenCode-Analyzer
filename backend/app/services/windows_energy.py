"""
Native Windows Energy Metering Interface (EMI).

Purpose
-------
Reads hardware-reported accumulated energy from Windows EMI.

This implementation:

    - Uses native Windows SetupAPI
    - Uses native DeviceIoControl
    - Supports EMI V1 and EMI V2
    - Dynamically parses EMI V2 channels
    - Selects RAPL_Package0_PKG by channel name
    - Reads AbsoluteEnergy directly from the hardware energy meter
    - Does NOT estimate energy using Power * Time
    - Does NOT use PowerShell
    - Does NOT use CPU utilization to estimate energy

For EMI, AbsoluteEnergy is reported in picowatt-hours (pWh).
The pWh -> Joule conversion is only a unit conversion.
"""

import ctypes
import struct
import uuid

from ctypes import (
    Structure,
    POINTER,
    byref,
    sizeof,
    c_void_p,
    c_ulong,
    c_ulonglong,
    c_ushort,
    c_size_t,
    create_string_buffer,
    wintypes,
)


# ============================================================
# Windows DLLs
# ============================================================

kernel32 = ctypes.WinDLL(
    "kernel32",
    use_last_error=True,
)

setupapi = ctypes.WinDLL(
    "setupapi",
    use_last_error=True,
)


# ============================================================
# Windows constants
# ============================================================

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

ERROR_NO_MORE_ITEMS = 259

DIGCF_PRESENT = 0x00000002
DIGCF_DEVICEINTERFACE = 0x00000010

OPEN_EXISTING = 3

FILE_ATTRIBUTE_NORMAL = 0x00000080

GENERIC_READ = 0x80000000

FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002

FILE_DEVICE_UNKNOWN = 0x00000022

METHOD_BUFFERED = 0

FILE_READ_ACCESS = 0x0001


# ============================================================
# EMI device GUID
# ============================================================

GUID_DEVICE_ENERGY_METER = (
    "{45BD8344-7ED6-49CF-A440-C276C933B053}"
)


# ============================================================
# EMI constants
# ============================================================

EMI_VERSION_V1 = 1
EMI_VERSION_V2 = 2

EMI_MEASUREMENT_UNIT_PICOWATT_HOURS = 0

EMI_NAME_MAX = 16

# Structure:
#
# ULONGLONG AbsoluteEnergy
# ULONGLONG AbsoluteTime
#
# = 16 bytes
EMI_MEASUREMENT_DATA_SIZE = 16


# ============================================================
# Correct EMI IOCTL construction
# ============================================================

def ctl_code(
    device_type,
    function,
    method,
    access,
):
    return (
        (device_type << 16)
        | (access << 14)
        | (function << 2)
        | method
    )


# IMPORTANT:
#
# These are:
#
# function 0 -> version
# function 1 -> metadata size
# function 2 -> metadata
# function 3 -> measurement
#
# with FILE_READ_ACCESS.

IOCTL_EMI_GET_VERSION = ctl_code(
    FILE_DEVICE_UNKNOWN,
    0,
    METHOD_BUFFERED,
    FILE_READ_ACCESS,
)

IOCTL_EMI_GET_METADATA_SIZE = ctl_code(
    FILE_DEVICE_UNKNOWN,
    1,
    METHOD_BUFFERED,
    FILE_READ_ACCESS,
)

IOCTL_EMI_GET_METADATA = ctl_code(
    FILE_DEVICE_UNKNOWN,
    2,
    METHOD_BUFFERED,
    FILE_READ_ACCESS,
)

IOCTL_EMI_GET_MEASUREMENT = ctl_code(
    FILE_DEVICE_UNKNOWN,
    3,
    METHOD_BUFFERED,
    FILE_READ_ACCESS,
)


# ============================================================
# GUID structure
# ============================================================

class GUID(Structure):

    _fields_ = [
        (
            "Data1",
            wintypes.DWORD,
        ),
        (
            "Data2",
            wintypes.WORD,
        ),
        (
            "Data3",
            wintypes.WORD,
        ),
        (
            "Data4",
            wintypes.BYTE * 8,
        ),
    ]


# ============================================================
# SetupAPI structure
# ============================================================

class SP_DEVICE_INTERFACE_DATA(Structure):

    _fields_ = [
        (
            "cbSize",
            wintypes.DWORD,
        ),
        (
            "InterfaceClassGuid",
            GUID,
        ),
        (
            "Flags",
            wintypes.DWORD,
        ),
        (
            "Reserved",
            c_size_t,
        ),
    ]


# ============================================================
# Windows API prototypes
# ============================================================

setupapi.SetupDiGetClassDevsW.argtypes = [
    POINTER(GUID),
    wintypes.LPCWSTR,
    wintypes.HWND,
    wintypes.DWORD,
]

setupapi.SetupDiGetClassDevsW.restype = (
    wintypes.HANDLE
)


setupapi.SetupDiEnumDeviceInterfaces.argtypes = [
    wintypes.HANDLE,
    c_void_p,
    POINTER(GUID),
    wintypes.DWORD,
    POINTER(SP_DEVICE_INTERFACE_DATA),
]

setupapi.SetupDiEnumDeviceInterfaces.restype = (
    wintypes.BOOL
)


setupapi.SetupDiGetDeviceInterfaceDetailW.argtypes = [
    wintypes.HANDLE,
    POINTER(SP_DEVICE_INTERFACE_DATA),
    c_void_p,
    wintypes.DWORD,
    POINTER(wintypes.DWORD),
    c_void_p,
]

setupapi.SetupDiGetDeviceInterfaceDetailW.restype = (
    wintypes.BOOL
)


setupapi.SetupDiDestroyDeviceInfoList.argtypes = [
    wintypes.HANDLE,
]

setupapi.SetupDiDestroyDeviceInfoList.restype = (
    wintypes.BOOL
)


kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    c_void_p,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE,
]

kernel32.CreateFileW.restype = wintypes.HANDLE


kernel32.DeviceIoControl.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD,
    c_void_p,
    wintypes.DWORD,
    c_void_p,
    wintypes.DWORD,
    POINTER(wintypes.DWORD),
    c_void_p,
]

kernel32.DeviceIoControl.restype = wintypes.BOOL


kernel32.CloseHandle.argtypes = [
    wintypes.HANDLE,
]

kernel32.CloseHandle.restype = wintypes.BOOL


# ============================================================
# Data classes
# ============================================================

from dataclasses import dataclass


@dataclass
class EnergyMeasurement:

    absolute_energy_pwh: int
    absolute_time: int


@dataclass
class EMIChannel:

    name: str
    measurement_unit: int


# ============================================================
# Helper functions
# ============================================================

def raise_windows_error(message: str):

    error = ctypes.get_last_error()

    if error == 0:
        raise OSError(
            f"{message} (Windows error unavailable)"
        )

    raise OSError(
        error,
        f"{message} "
        f"(Windows error {error})",
    )


def guid_from_string(
    guid_string: str,
) -> GUID:

    value = uuid.UUID(
        guid_string
    )

    data = value.bytes_le

    result = GUID()

    result.Data1 = int.from_bytes(
        data[0:4],
        "little",
    )

    result.Data2 = int.from_bytes(
        data[4:6],
        "little",
    )

    result.Data3 = int.from_bytes(
        data[6:8],
        "little",
    )

    for index in range(8):

        result.Data4[index] = (
            data[8 + index]
        )

    return result


# ============================================================
# Windows Energy Meter
# ============================================================

class WindowsEnergyMeter:

    def __init__(
        self,
        target_channel="RAPL_Package0_PKG",
    ):

        self.target_channel = (
            target_channel
        )

        self.handle = None

        self.device_path = None

        self.version = None

        self.channels = []

        self.metadata_buffer = None

        self.selected_channel_index = None

        self.hardware_oem = ""

        self.hardware_model = ""

        self.hardware_revision = 0

        self._open()


    # ========================================================
    # Device discovery
    # ========================================================

    def _discover_device_paths(self):

        guid = guid_from_string(
            GUID_DEVICE_ENERGY_METER
        )

        device_info = (
            setupapi.SetupDiGetClassDevsW(
                byref(guid),
                None,
                None,
                DIGCF_PRESENT
                | DIGCF_DEVICEINTERFACE,
            )
        )

        if (
            device_info
            == INVALID_HANDLE_VALUE
        ):

            raise_windows_error(
                "SetupDiGetClassDevsW failed"
            )

        paths = []

        try:

            index = 0

            while True:

                interface_data = (
                    SP_DEVICE_INTERFACE_DATA()
                )

                interface_data.cbSize = sizeof(
                    SP_DEVICE_INTERFACE_DATA
                )

                success = (
                    setupapi
                    .SetupDiEnumDeviceInterfaces(
                        device_info,
                        None,
                        byref(guid),
                        index,
                        byref(interface_data),
                    )
                )

                if not success:

                    error = ctypes.get_last_error()

                    if (
                        error
                        == ERROR_NO_MORE_ITEMS
                    ):
                        break

                    raise_windows_error(
                        "SetupDiEnumDeviceInterfaces failed"
                    )

                required_size = (
                    wintypes.DWORD()
                )

                setupapi.SetupDiGetDeviceInterfaceDetailW(
                    device_info,
                    byref(interface_data),
                    None,
                    0,
                    byref(required_size),
                    None,
                )

                if required_size.value == 0:

                    index += 1
                    continue

                buffer = create_string_buffer(
                    required_size.value
                )

                # SP_DEVICE_INTERFACE_DETAIL_DATA_W:
                #
                # cbSize is:
                #   8 bytes on 64-bit Windows
                #   6 bytes on 32-bit Windows
                #
                detail_cb_size = (
                    8
                    if ctypes.sizeof(
                        ctypes.c_void_p
                    ) == 8
                    else 6
                )

                ctypes.memmove(
                    buffer,
                    ctypes.byref(
                        ctypes.c_ulong(
                            detail_cb_size
                        )
                    ),
                    sizeof(
                        ctypes.c_ulong
                    ),
                )

                success = (
                    setupapi
                    .SetupDiGetDeviceInterfaceDetailW(
                        device_info,
                        byref(interface_data),
                        buffer,
                        required_size.value,
                        byref(required_size),
                        None,
                    )
                )

                if not success:

                    raise_windows_error(
                        "SetupDiGetDeviceInterfaceDetailW failed"
                    )

                # Device path begins immediately
                # after cbSize.
                # SP_DEVICE_INTERFACE_DETAIL_DATA_W contains:
                #
                #   DWORD cbSize
                #   WCHAR DevicePath[]
                #
                # On Windows, the WCHAR DevicePath starts at the
                # structure's WCHAR-aligned offset.
                #
                # Read it directly from the returned byte buffer.

                device_path_offset = 4

                device_path = ctypes.wstring_at(
                    ctypes.addressof(buffer)
                    + device_path_offset
                )

                # Windows device interface paths must begin with \\?\
                if not device_path.startswith("\\\\?\\"):

                    raise RuntimeError(
                        "Invalid Windows EMI device path returned "
                        f"by SetupAPI: {device_path!r}"
                    )

                paths.append(
                    device_path
                )

                index += 1

        finally:

            setupapi.SetupDiDestroyDeviceInfoList(
                device_info
            )

        return paths


    # ========================================================
    # Open device
    # ========================================================

    def _open(self):

        paths = (
            self._discover_device_paths()
        )
        # print("DISCOVERED EMI DEVICE PATHS:")

        # for path in paths:
        #     print(repr(path))

        if not paths:

            raise RuntimeError(
                "No Windows Energy Metering "
                "Interface device was found."
            )

        last_error = None

        for path in paths:

            handle = kernel32.CreateFileW(
                path,
                GENERIC_READ,
                FILE_SHARE_READ
                | FILE_SHARE_WRITE,
                None,
                OPEN_EXISTING,
                FILE_ATTRIBUTE_NORMAL,
                None,
            )

            if (
                handle
                != INVALID_HANDLE_VALUE
            ):

                self.handle = handle
                self.device_path = path

                break

            last_error = ctypes.get_last_error()

        if self.handle is None:

            raise OSError(
                last_error or 0,
                "Unable to open any "
                "Windows EMI device."
            )

        try:

            self._get_version()

            self._get_metadata()

        except Exception:

            self.close()

            raise


    # ========================================================
    # Get EMI version
    # ========================================================

    def _get_version(self):

        # EMI_VERSION contains USHORT EmiVersion.
        buffer = create_string_buffer(
            2
        )

        returned = (
            wintypes.DWORD()
        )

        success = (
            kernel32.DeviceIoControl(
                self.handle,
                IOCTL_EMI_GET_VERSION,
                None,
                0,
                buffer,
                len(buffer),
                byref(returned),
                None,
            )
        )

        if not success:

            raise_windows_error(
                "IOCTL_EMI_GET_VERSION failed"
            )

        self.version = struct.unpack_from(
            "<H",
            buffer.raw,
            0,
        )[0]

        if self.version not in (
            EMI_VERSION_V1,
            EMI_VERSION_V2,
        ):

            raise RuntimeError(
                f"Unsupported EMI version: "
                f"{self.version}"
            )


    # ========================================================
    # Get metadata size
    # ========================================================

    def _get_metadata_size(self):

        buffer = create_string_buffer(
            4
        )

        returned = (
            wintypes.DWORD()
        )

        success = (
            kernel32.DeviceIoControl(
                self.handle,
                IOCTL_EMI_GET_METADATA_SIZE,
                None,
                0,
                buffer,
                len(buffer),
                byref(returned),
                None,
            )
        )

        if not success:

            raise_windows_error(
                "IOCTL_EMI_GET_METADATA_SIZE failed"
            )

        return struct.unpack_from(
            "<I",
            buffer.raw,
            0,
        )[0]


    # ========================================================
    # Get metadata
    # ========================================================

    def _get_metadata(self):

        size = (
            self._get_metadata_size()
        )

        if size <= 0:

            raise RuntimeError(
                "Windows EMI returned "
                "invalid metadata size."
            )

        buffer = create_string_buffer(
            size
        )

        returned = (
            wintypes.DWORD()
        )

        success = (
            kernel32.DeviceIoControl(
                self.handle,
                IOCTL_EMI_GET_METADATA,
                None,
                0,
                buffer,
                size,
                byref(returned),
                None,
            )
        )

        if not success:

            raise_windows_error(
                "IOCTL_EMI_GET_METADATA failed"
            )

        self.metadata_buffer = buffer

        if self.version == EMI_VERSION_V1:

            self._parse_v1_metadata(
                buffer.raw
            )

        elif self.version == EMI_VERSION_V2:

            self._parse_v2_metadata(
                buffer.raw
            )


    # ========================================================
    # Parse V1 metadata
    # ========================================================

    def _parse_v1_metadata(
        self,
        data: bytes,
    ):

        # EMI_METADATA_V1:
        #
        # int32 MeasurementUnit
        # WCHAR HardwareOEM[16]
        # WCHAR HardwareModel[16]
        # USHORT HardwareRevision
        # USHORT MeteredHardwareNameSize
        # WCHAR MeteredHardwareName[]
        #
        # First fixed portion = 4 + 32 + 32 + 2 + 2
        # = 72 bytes.

        if len(data) < 72:

            raise RuntimeError(
                "Invalid EMI V1 metadata."
            )

        measurement_unit = (
            struct.unpack_from(
                "<I",
                data,
                0,
            )[0]
        )

        if (
            measurement_unit
            != EMI_MEASUREMENT_UNIT_PICOWATT_HOURS
        ):

            raise RuntimeError(
                "Unsupported EMI V1 "
                "measurement unit."
            )

        self.hardware_oem = (
            data[
                4:36
            ]
            .decode(
                "utf-16-le",
                errors="ignore",
            )
            .split("\x00", 1)[0]
        )

        self.hardware_model = (
            data[
                36:68
            ]
            .decode(
                "utf-16-le",
                errors="ignore",
            )
            .split("\x00", 1)[0]
        )

        self.hardware_revision = (
            struct.unpack_from(
                "<H",
                data,
                68,
            )[0]
        )

        name_size = (
            struct.unpack_from(
                "<H",
                data,
                70,
            )[0]
        )

        name_bytes = data[
            72:72 + name_size
        ]

        meter_name = (
            name_bytes
            .decode(
                "utf-16-le",
                errors="ignore",
            )
            .split("\x00", 1)[0]
        )

        self.channels = [
            EMIChannel(
                name=meter_name,
                measurement_unit=measurement_unit,
            )
        ]

        # V1 has only one channel.
        self.selected_channel_index = 0


    # ========================================================
    # Parse V2 metadata
    # ========================================================

    def _parse_v2_metadata(
        self,
        data: bytes,
    ):

        # EMI_METADATA_V2:
        #
        # WCHAR HardwareOEM[16]      32 bytes
        # WCHAR HardwareModel[16]    32 bytes
        # USHORT HardwareRevision     2 bytes
        # USHORT ChannelCount         2 bytes
        #
        # Channels begin at offset 68.

        if len(data) < 68:

            raise RuntimeError(
                "Invalid EMI V2 metadata."
            )

        self.hardware_oem = (
            data[
                0:32
            ]
            .decode(
                "utf-16-le",
                errors="ignore",
            )
            .split("\x00", 1)[0]
        )

        self.hardware_model = (
            data[
                32:64
            ]
            .decode(
                "utf-16-le",
                errors="ignore",
            )
            .split("\x00", 1)[0]
        )

        self.hardware_revision = (
            struct.unpack_from(
                "<H",
                data,
                64,
            )[0]
        )

        channel_count = (
            struct.unpack_from(
                "<H",
                data,
                66,
            )[0]
        )

        offset = 68

        channels = []

        for _ in range(channel_count):

            if offset + 6 > len(data):

                raise RuntimeError(
                    "Invalid EMI V2 channel metadata."
                )

            measurement_unit = (
                struct.unpack_from(
                    "<I",
                    data,
                    offset,
                )[0]
            )

            channel_name_size = (
                struct.unpack_from(
                    "<H",
                    data,
                    offset + 4,
                )[0]
            )

            if channel_name_size < 2:

                raise RuntimeError(
                    "Invalid EMI V2 "
                    "channel name size."
                )

            name_start = (
                offset + 6
            )

            name_end = (
                name_start
                + channel_name_size
            )

            if name_end > len(data):

                raise RuntimeError(
                    "EMI V2 channel extends "
                    "beyond metadata buffer."
                )

            name_bytes = data[
                name_start:name_end
            ]

            channel_name = (
                name_bytes
                .decode(
                    "utf-16-le",
                    errors="ignore",
                )
                .split("\x00", 1)[0]
            )

            channels.append(
                EMIChannel(
                    name=channel_name,
                    measurement_unit=measurement_unit,
                )
            )

            # EMI_CHANNEL_V2_NEXT_CHANNEL
            #
            # Move exactly:
            #
            # sizeof(fixed fields) + ChannelNameSize
            #
            offset = name_end

        self.channels = channels

        # ----------------------------------------------------
        # Find requested channel
        # ----------------------------------------------------

        target = (
            self.target_channel
            .strip()
            .lower()
        )

        for index, channel in enumerate(
            self.channels
        ):

            if (
                channel.name
                .strip()
                .lower()
                == target
            ):

                self.selected_channel_index = (
                    index
                )

                break

        if (
            self.selected_channel_index
            is None
        ):

            available = ", ".join(
                channel.name
                for channel in self.channels
            )

            raise RuntimeError(
                "Requested Windows EMI "
                f"channel '{self.target_channel}' "
                "was not found.\n"
                f"Available channels: {available}"
            )

        selected = self.channels[
            self.selected_channel_index
        ]

        if (
            selected.measurement_unit
            != EMI_MEASUREMENT_UNIT_PICOWATT_HOURS
        ):

            raise RuntimeError(
                "Selected EMI channel does not "
                "report energy in picowatt-hours."
            )


    # ========================================================
    # Read measurements
    # ========================================================

    def read_all(
        self,
    ):

        if self.handle is None:

            raise RuntimeError(
                "Windows EMI device is closed."
            )

        if self.version == EMI_VERSION_V1:

            channel_count = 1

        else:

            channel_count = len(
                self.channels
            )

        output_size = (
            channel_count
            * EMI_MEASUREMENT_DATA_SIZE
        )

        buffer = create_string_buffer(
            output_size
        )

        returned = (
            wintypes.DWORD()
        )

        success = (
            kernel32.DeviceIoControl(
                self.handle,
                IOCTL_EMI_GET_MEASUREMENT,
                None,
                0,
                buffer,
                output_size,
                byref(returned),
                None,
            )
        )

        if not success:

            raise_windows_error(
                "IOCTL_EMI_GET_MEASUREMENT failed"
            )

        measurements = []

        for index in range(
            channel_count
        ):

            offset = (
                index
                * EMI_MEASUREMENT_DATA_SIZE
            )

            absolute_energy = (
                struct.unpack_from(
                    "<Q",
                    buffer.raw,
                    offset,
                )[0]
            )

            absolute_time = (
                struct.unpack_from(
                    "<Q",
                    buffer.raw,
                    offset + 8,
                )[0]
            )

            measurements.append(
                EnergyMeasurement(
                    absolute_energy_pwh=(
                        absolute_energy
                    ),
                    absolute_time=(
                        absolute_time
                    ),
                )
            )

        return measurements


    # ========================================================
    # Read selected package energy
    # ========================================================

    def read_package_energy(
        self,
    ) -> EnergyMeasurement:

        measurements = (
            self.read_all()
        )

        index = (
            self.selected_channel_index
        )

        if index is None:

            raise RuntimeError(
                "No EMI channel has been selected."
            )

        if index >= len(
            measurements
        ):

            raise RuntimeError(
                "EMI measurement did not return "
                "the selected channel."
            )

        return measurements[
            index
        ]


    # ========================================================
    # Convert a measured interval to Joules
    # ========================================================

    @staticmethod
    def energy_delta_joules(
        before: EnergyMeasurement,
        after: EnergyMeasurement,
    ) -> float:

        if (
            after.absolute_energy_pwh
            < before.absolute_energy_pwh
        ):

            raise RuntimeError(
                "EMI energy counter moved "
                "backwards. The device may have "
                "reset or wrapped."
            )

        delta_pwh = (
            after.absolute_energy_pwh
            - before.absolute_energy_pwh
        )

        # This is ONLY unit conversion:
        #
        # 1 Wh = 3600 J
        # 1 pWh = 10^-12 Wh
        #
        # therefore:
        #
        # 1 pWh = 3.6e-9 J

        return (
            delta_pwh
            * 3.6e-9
        )


    # ========================================================
    # Diagnostics
    # ========================================================

    def get_info(self):

        return {
            "device_path": self.device_path,
            "emi_version": self.version,
            "hardware_oem": self.hardware_oem,
            "hardware_model": self.hardware_model,
            "hardware_revision": self.hardware_revision,
            "target_channel": self.target_channel,
            "selected_channel_index": (
                self.selected_channel_index
            ),
            "channels": [
                {
                    "name": channel.name,
                    "measurement_unit": (
                        channel.measurement_unit
                    ),
                }
                for channel in self.channels
            ],
        }


    # ========================================================
    # Close
    # ========================================================

    def close(self):

        if self.handle is not None:

            kernel32.CloseHandle(
                self.handle
            )

            self.handle = None


    def __enter__(self):

        return self


    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        self.close()


# ============================================================
# Convenience function
# ============================================================

def create_energy_meter(
    target_channel="RAPL_Package0_PKG",
):

    return WindowsEnergyMeter(
        target_channel=target_channel
    )
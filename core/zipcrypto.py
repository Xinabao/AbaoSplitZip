"""
Minimal Traditional PKWARE ZipCrypto writer for pyzipper.

pyzipper can read traditional ZipCrypto archives, but its public writer only
implements WinZip AES. This module plugs into pyzipper's encrypter hook so the
app can still produce Windows Explorer-compatible encrypted ZIP files.
"""

import os

from pyzipper import ZipFile

ZIP_CRYPTO = "ZIP_CRYPTO"
_MASK_USE_DATA_DESCRIPTOR = 0x08
_CRC_POLY = 0xEDB88320


def _gen_crc(value: int) -> int:
    for _ in range(8):
        if value & 1:
            value = (value >> 1) ^ _CRC_POLY
        else:
            value >>= 1
    return value


_CRC_TABLE = [_gen_crc(i) for i in range(256)]


class ZipCryptoEncrypter:
    def __init__(self, pwd: bytes):
        if not pwd:
            raise RuntimeError("ZipCrypto encryption requires a password")
        self._pwd = pwd
        self._zinfo = None
        self._key0 = 305419896
        self._key1 = 591751049
        self._key2 = 878082192
        for byte in pwd:
            self._update_keys(byte)

    def _crc32_byte(self, byte: int, crc: int) -> int:
        return (crc >> 8) ^ _CRC_TABLE[(crc ^ byte) & 0xFF]

    def _update_keys(self, byte: int):
        self._key0 = self._crc32_byte(byte, self._key0)
        self._key1 = (self._key1 + (self._key0 & 0xFF)) & 0xFFFFFFFF
        self._key1 = (self._key1 * 134775813 + 1) & 0xFFFFFFFF
        self._key2 = self._crc32_byte(self._key1 >> 24, self._key2)

    def _crypt_byte(self) -> int:
        key = self._key2 | 2
        return ((key * (key ^ 1)) >> 8) & 0xFF

    def update_zipinfo(self, zinfo):
        self._zinfo = zinfo
        zinfo.flag_bits |= _MASK_USE_DATA_DESCRIPTOR
        zinfo.extract_version = max(zinfo.extract_version, 20)
        zinfo.create_version = max(zinfo.create_version, 20)
        if not hasattr(zinfo, "_raw_time"):
            zinfo._raw_time = zinfo.get_dostime()

    def encryption_header(self) -> bytes:
        check_byte = (self._zinfo._raw_time >> 8) & 0xFF
        return self.encrypt(os.urandom(11) + bytes([check_byte]))

    def encrypt(self, data: bytes) -> bytes:
        result = bytearray()
        append = result.append
        for byte in data:
            encrypted = byte ^ self._crypt_byte()
            self._update_keys(byte)
            append(encrypted)
        return bytes(result)

    def flush(self) -> bytes:
        return b""


class ZipCryptoZipFile(ZipFile):
    def get_encrypter(self):
        if self.encryption == ZIP_CRYPTO:
            return ZipCryptoEncrypter(self.pwd)
        return super().get_encrypter()

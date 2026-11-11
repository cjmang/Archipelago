from __future__ import annotations

import settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin

CHECKSUM_GSTLA = '8efe8b2aaed97149e897570cd123ff6e'


class GSTLAPatchError(Exception):
    pass


def apply_ups(rom: bytes, patch_data: bytes) -> bytes:
    """
    Patches a rom from a GBA UPS File. Shamelessly modeled after the GS TLA Rando code
    """
    target = bytearray(rom)
    data = patch_data[4:-12]
    patch_offset = 0

    def read_offset() -> int:
        nonlocal patch_offset
        local_offset = 0
        shift = 1
        while True:
            byte = data[patch_offset]
            patch_offset += 1
            local_offset += (byte & 0x7F) * shift
            if (byte & 0x80) > 0:
                break
            shift <<= 7
            local_offset += shift

        return local_offset

    source_len = read_offset()
    target_len = read_offset()
    if target_len > source_len:
        target.extend(bytearray(target_len - source_len))

    byte_offset = 0
    data_len = len(data)
    while patch_offset < data_len:
        offset = read_offset()
        byte_offset += offset
        while True:
            datum = data[patch_offset]
            patch_offset += 1
            target[byte_offset] ^= datum
            byte_offset += 1
            if datum == 0:
                break
    return bytes(target)


class GSTLADeltaPatch(APProcedurePatch, APTokenMixin):
    hash = CHECKSUM_GSTLA
    game = 'Golden Sun The Lost Age'
    patch_file_ending = '.apgstla'
    result_file_ending = '.gba'
    procedure = [
        ('apply_gstla_rando', ['ap_settings.gstlarando']),
        ('apply_tokens', ['token_data.bin']),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        # gotta read the options to get AP to check the md5s
        with open(settings.get_settings().gstla_options.rom_file, 'rb') as rom_file:
            return rom_file.read()

    def add_settings(self, data: bytes, debug_data: bytes | None):
        self.files['ap_settings.gstlarando'] = data
        if debug_data:
            self.files['ap_settings.debug.txt'] = debug_data


class GSTLAPatchExtension(APPatchExtension):
    game = 'Golden Sun The Lost Age'

    @staticmethod
    def apply_gstla_rando(caller: GSTLADeltaPatch, rom: bytes, patch_file: str) -> bytes:
        import requests

        ap_settings = caller.get_file(patch_file)
        try:
            # response = requests.post("http://localhost:3000/import_ap_ajax",
            response = requests.post(
                'https://gs2randomiser.com/import_ap_ajax',
                data=ap_settings,
                allow_redirects=False,
                timeout=(10, 120),
                headers={
                    # Rando expects XHR
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/octet-stream',
                },
            )
        except requests.RequestException as error:
            raise GSTLAPatchError(f'Could not reach the GS TLA Randomizer Website: {error}') from error
        if response.status_code != 200:
            raise GSTLAPatchError(
                f'Failed to patch ROM using GS TLA Randomizer Website; http code: {response.status_code}'
            )
        data = response.json()
        if not isinstance(data, dict) or not data.get('success'):
            raise GSTLAPatchError(f'Failed to patch ROM using GS TLA Randomizer Website; response: {data}')

        try:
            patch = bytes(data['patch'])
        except (KeyError, TypeError, ValueError) as error:
            raise GSTLAPatchError('The GS TLA Randomizer Website did not supply a usable patch') from error
        return apply_ups(rom, patch)

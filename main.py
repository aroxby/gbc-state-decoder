#!/usr/bin/env python3
import gzip
import struct


class Save:
    def __init__(self, save_bytes):
        self.bytes = save_bytes

    @property
    def player_name(self):
        NAME_OFFSET = 0x2598
        MAX_NAME = 11
        TEXT_TERMINATOR = 0x50
        name_bytes = self.bytes[NAME_OFFSET:NAME_OFFSET + MAX_NAME]
        length = name_bytes.index(TEXT_TERMINATOR)
        return decode_game_text(name_bytes[:length])

    @property
    def pokedex_owned(self):
        OWNED_OFFSET = 0x25A3
        OWNED_SIZE = 13
        owned_bytes = self.bytes[OWNED_OFFSET:OWNED_OFFSET + OWNED_SIZE]
        owned_byte_vals = struct.unpack('13B', owned_bytes)
        owned_count = sum(bin(byte_val).count('1') for byte_val in owned_byte_vals)
        return owned_count

    @property
    def pokedex_seen(self):
        SEEN_OFFSET = 0x25B6
        SEEN_SIZE = 13
        seen_bytes = self.bytes[SEEN_OFFSET:SEEN_OFFSET + SEEN_SIZE]
        seen_byte_vals = struct.unpack('13B', seen_bytes)
        seen_count = sum(bin(byte_val).count('1') for byte_val in seen_byte_vals)
        return seen_count

    @property
    def rival_name(self):
        NAME_OFFSET = 0x25F6
        MAX_NAME = 11
        TEXT_TERMINATOR = 0x50
        name_bytes = self.bytes[NAME_OFFSET:NAME_OFFSET + MAX_NAME]
        length = name_bytes.index(TEXT_TERMINATOR)
        return decode_game_text(name_bytes[:length])

    @property
    def player_id(self):
        ID_OFFSET = 0x2605
        ID_SIZE = 2
        id_bytes = self.bytes[ID_OFFSET:ID_OFFSET + ID_SIZE]
        id_val = struct.unpack('>H', id_bytes)[0]
        return id_val


def decode_game_text(byte_string):
    decode80toBF = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "(", ")", " :", " ;", "[", "]",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "é", "'d", "'l", "'s", "'t", "'v",
    ]
    decodeE0toFF = [
        "'", "Pk", "Mn", "-", "'r", "'m", " ?", " !", ".", "ァ", "ゥ", "ェ", "▷", "▶", "▼", "♂",
        "$", "×", ".", "/", ",", "♀", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ]
    output_string = ""
    for byte in byte_string:
        if byte >= 0x80 and byte <= 0xBF:
            output_string += decode80toBF[byte - 0x80]
        elif byte >= 0xE0 and byte <= 0xFF:
            output_string += decodeE0toFF[byte - 0xE0]
        else:
            output_string += '?'
    return output_string


def load_save(save_file):
    SAVE_LENGTH = 32768
    save_bytes = save_file.read(SAVE_LENGTH)
    assert len(save_bytes) == SAVE_LENGTH
    return save_bytes


def load_save_from_file(path):
    with open(path, 'rb') as save_file:
        return load_save(save_file)


def load_save_from_bgb_state(path):
    with gzip.open(path, 'rb') as state_file:
        state_file.seek(0x837C)
        return load_save(state_file)


def load_save_from_mob_state(path):
    with gzip.open(path, 'rb') as state_file:
        state_file.seek(0x8044)
        return load_save(state_file)


def load_save_from_vba_state(path):
    with gzip.open(path, 'rb') as state_file:
        state_file.seek(0xFCE6)
        return load_save(state_file)


def main():
    # save_bytes = load_save_from_file('red.sav')
    # save_bytes = load_save_from_bgb_state('red.sgm')
    # save_bytes = load_save_from_mob_state('red.st1')
    save_bytes = load_save_from_vba_state('red.sg1')
    save = Save(save_bytes)
    print('Player:', save.player_name, f'IDNo/{save.player_id}')
    print('Rival:', save.rival_name)
    print('Pokedex seen: ', save.pokedex_seen)
    print('Pokedex owned: ', save.pokedex_owned)


if __name__ == '__main__':
    main()

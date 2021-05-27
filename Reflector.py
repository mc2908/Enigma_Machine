from enum import Enum


class Reflector:

    def __init__(self, etype, wiring):
        self.wiring = wiring
        self.wiring_type = WiringType.Std
        self.eType = etype

    def encode(self, char_in):
        char_in = char_in.upper()
        right_char_list = [right_char for _, right_char in self.wiring]
        char_idx = right_char_list.index(char_in)
        out_contact, in_contact = self.wiring[char_idx]
        return out_contact

    def swap_wiring(self, new_wiring):
        self.wiring = new_wiring
        self.wiring_type = WiringType.Mod

    def reset_std_wiring(self):
        self.wiring = get_wiring_by_ReflectorType(self.eType)
        self.wiring_type = WiringType.Std



class ReflectorType(Enum):
    ND = 0
    A = 1
    B = 2
    C = 3

class WiringType(Enum):
    ND = 0
    Std = 1
    Mod = 2

def reflectorType_from_name(rotor_name):
    if rotor_name == "A":
        reflector_type = ReflectorType.A

    elif rotor_name == "B":
        reflector_type = ReflectorType.B

    else:  # must be C
        reflector_type = ReflectorType.C
    return reflector_type


def reflector_from_name(rotor_name):
    reflector_type = reflectorType_from_name(rotor_name)
    wiring = get_wiring_by_ReflectorType(reflector_type)
    reflector = Reflector(reflector_type, wiring)
    return reflector


def get_wiring_by_ReflectorType(rotor_type):
    base_contact = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    wiring_matrix = [
                   ["E", "J", "M", "Z", "A", "L", "Y", "X", "V", "B", "W", "F", "C", "R", "Q", "U", "O", "N", "T", "S", "P", "I", "K", "H", "G", "D"],  # A
                   ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T'],  # B
                   ['F', 'V', 'P', 'J', 'I', 'A', 'O', 'Y', 'E', 'D', 'R', 'Z', 'X', 'W', 'G', 'C', 'T', 'K', 'U', 'Q', 'S', 'B', 'N', 'M', 'H', 'L']]  # C

    wiring = list(zip(wiring_matrix[rotor_type.value - 1], base_contact))
    return wiring

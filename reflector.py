from enum import Enum
import utility


class Reflector:

    def __init__(self, etype, wiring):
        self.wiring = dict(wiring)
        self.wiring_type = WiringType.Std
        self.eType = etype

    def encode(self, char_in):
        if char_in not in self.wiring:
            raise ValueError()
        out_contact = self.wiring[char_in]
        return out_contact

    def swap_wiring(self, new_wiring):
        new_wiring_dict = dict(new_wiring)
        if self.wiring != new_wiring_dict:
            self.wiring = new_wiring_dict
            self.wiring_type = WiringType.Mod

    def reset_std_wiring(self):
        self.wiring = dict(get_wiring_by_ReflectorType(self.eType))
        self.wiring_type = WiringType.Std

    # find the swapped pairs in the reflector with respect to the standard wiring
    def find_wiring_changes(self):
        if self.wiring_type == WiringType.Std:
            # no changes, return an empty list
            return []
        std_wiring = get_wiring_by_ReflectorType(self.wiring_type)
        mod_wiring = self.wiring.items()
        # find the connections which were modified
        mod_pairs = [x for x in mod_wiring if x not in std_wiring]
        # removed complementary pairs
        for x, y in mod_pairs:
            if (y, x) in mod_pairs:
                idx = mod_pairs.index((y, x))
                mod_pairs.pop(idx)
        mod_pairs = [x+y for x, y in mod_pairs]
        return mod_pairs

    # two reflector are equal if they are of the same type
    def __eq__(self, other):
        return self.eType == other.eType

# # Enumerator class to identify reflector
class ReflectorType(Enum):
    ND = 0
    A = 1
    B = 2
    C = 3

# Enumerator class to identify if a reflector's wiring has been manually modified or not
class WiringType(Enum):
    ND = 0
    Std = 1
    Mod = 2


def reflectorType_from_name(reflector_name):
    if reflector_name == "A":
        reflector_type = ReflectorType.A
    elif reflector_name == "B":
        reflector_type = ReflectorType.B
    elif reflector_name == "C":  # must be C
        reflector_type = ReflectorType.C
    else:
        raise ValueError(f"Reflector {reflector_name} does not exist")
    return reflector_type


def reflector_from_name(reflector_name):
    reflector_type = reflectorType_from_name(reflector_name)
    wiring = get_wiring_by_ReflectorType(reflector_type)
    reflector = Reflector(reflector_type, wiring)
    return reflector


def get_wiring_by_ReflectorType(reflector_type):
    base_contact = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    wiring_matrix = [
                   ["E", "J", "M", "Z", "A", "L", "Y", "X", "V", "B", "W", "F", "C", "R", "Q", "U", "O", "N", "T", "S", "P", "I", "K", "H", "G", "D"],  # A
                   ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T'],  # B
                   ['F', 'V', 'P', 'J', 'I', 'A', 'O', 'Y', 'E', 'D', 'R', 'Z', 'X', 'W', 'G', 'C', 'T', 'K', 'U', 'Q', 'S', 'B', 'N', 'M', 'H', 'L']]  # C

    wiring = list(zip(wiring_matrix[reflector_type.value - 1], base_contact))
    return wiring


if __name__ == "__main__":
    reflector = reflector_from_name("A")
    assert(reflector.encode("A") == "E")
    assert(reflector.encode("E") == "A")
from enum import Enum


class Rotor:

    def __init__(self, etype, wiring, notch):
        self.location = 0                           # Rotor location in the Rotorcase 0 = rightmost rotor
        self.pos = 0                                # Rotor current position
        self.default_pos = 0                        # Rotor default position (set when the rotor is first added)
        self.ringSet = 0                            # Rotor ring setting
        self.eType = etype                          # Rotor Type
        self.wiring = wiring                        # Rotor wiring  <tuple(<string>,<string>)>
        self.s_Notch = notch                        # Rortor notch  <string>
        self.num_Notch = Rotor.char2num(notch)      # Rotor notch <integer>
        self.left_rotor = None                      # Rotor on the left side
        self.right_rotor = None                     # Rotor on the right side
        self.has_rotated = False                    # Flag to indicate whether or not the rotor has rotated for a given keyboard press

    def set_initial_position(self, s_pos):
        s_pos = s_pos.upper()
        if s_pos > "Z" or s_pos < "A":
            return
        self.pos = Rotor.char2num(s_pos)
        self.default_pos = Rotor.char2num(s_pos)

    def reset_to_default(self):
        self.pos = self.default_pos

    def set_ring_setting(self, val):
        if type(val) == str:
            val = Rotor.char2num(val) + 1
        self.ringSet = val - 1

    def rotate(self):
        if self.is_fourth_rotor():  # the fourth rotor never rotates
            return
        # If this rotor isn't the last one and it is at the notch position, then rotate the next rotor on the left first
        if not self.is_leftmost_rotor() and self.is_at_notch():
            self.left_rotor.rotate()
        self.pos = (self.pos + 1) % 26  # increase position by 1
        self.has_rotated = True
        return True

    def is_leftmost_rotor(self):
        return self.left_rotor is None

    def is_rightmost_rotor(self):
        return self.right_rotor is None

    def is_fourth_rotor(self):
        return self.location == 3

    def encode_right_to_left(self, char_in):
        char_in = char_in.upper()
        # get the list of right contacts
        right_contacts = [right_char for _, right_char in self.wiring]
        # get the correct right contact alignment considering position and ring setting
        _, right_contact = self.adjust_rotor_contact_right_to_left(char_in)
        # get the
        wire_map_idx = right_contacts.index(right_contact)
        left_contact, _ = self.wiring[wire_map_idx]
        if self.is_leftmost_rotor():
            # the last rotor needs to pass adjusted contact information to the reflector because the reflector does not
            # know anything about the position of the rotors
            left_contact = Rotor.num2Char((Rotor.char2num(left_contact) - self.pos + self.ringSet) % 26)
        return left_contact

    def encode_left_to_right(self, char_in):
        char_in = char_in.upper()
        left_contacts = [left_char for left_char, _ in self.wiring]
        # get the list of right contacts
        _, left_contact = self.adjust_rotor_contact_left_to_right(char_in)
        wire_map_idx = left_contacts.index(left_contact)
        _, right_contact = self.wiring[wire_map_idx]
        if self.is_rightmost_rotor():
            right_contact = Rotor.num2Char((Rotor.char2num(right_contact) - self.pos + self.ringSet) % 26)
        return right_contact

    def adjust_rotor_contact_right_to_left(self, char_in):
        right_rotor_pos = 0
        right_rotor_ring_set = 0
        if not self.is_rightmost_rotor():
            right_rotor_pos = self.right_rotor.pos
            right_rotor_ring_set = self.right_rotor.ringSet
        contact_idx = (Rotor.char2num(char_in) + self.pos - self.ringSet - right_rotor_pos + right_rotor_ring_set) % 26
        contact = Rotor.num2Char(contact_idx)
        return contact_idx, contact

    def adjust_rotor_contact_left_to_right(self, char_in):
        pos_left_rotor = 0
        ringSet_left_rotor = 0
        if not self.is_leftmost_rotor():
            pos_left_rotor = self.left_rotor.pos
            ringSet_left_rotor = self.left_rotor.ringSet
        contact_idx = (Rotor.char2num(char_in) + self.pos - self.ringSet - pos_left_rotor + ringSet_left_rotor) % 26
        contact = Rotor.num2Char(contact_idx)
        return contact_idx, contact

    def set_next_rotor(self, rotor):
        self.nextRotor = rotor

    def set_previous_rotor(self, rotor):
        self.nextRotor = rotor

    def is_at_notch(self):
        return self.num_Notch == self.pos

    @ staticmethod
    def char2num(char):
        return ord(char) - ord("A")

    @staticmethod
    def num2Char(num):
        return chr(num + ord("A"))


class RotorType(Enum):
    ND = 0
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5
    Beta = 6
    Gamma = 7


def rotor_from_name(rotor_name):
    rotor_type = Rotor_type_from_name(rotor_name)
    wiring = get_wiring_by_rotorType(rotor_type)
    notch = get_notch_by_RotorType(rotor_type)
    rotor = Rotor(rotor_type, wiring, notch)
    return rotor



def Rotor_type_from_name(rotor_name):
    if rotor_name == "I":
        rotor_type = RotorType.I

    elif rotor_name == "II":
        rotor_type = RotorType.II

    elif rotor_name == "III":
        rotor_type = RotorType.III

    elif rotor_name == "IV":
        rotor_type = RotorType.IV

    elif rotor_name == "V":
        rotor_type = RotorType.V

    elif rotor_name == "Beta":
        rotor_type = RotorType.Beta

    else:  # must be Gamma
        rotor_type = RotorType.Gamma
    return rotor_type



def get_wiring_by_rotorType(rotor_type):
    base_contact = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    wiring_matrix = [
                   ["E", "K", "M", "F", "L", "G", "D", "Q", "V", "Z", "N", "T", "O", "W", "Y", "H", "X", "U", "S", "P", "A", "I", "B", "R", "C", "J"],  # I
                   ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E'],  # II
                   ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O'],  # III
                   ['E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R', 'H', 'X', 'L', 'N', 'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B'],  # IV
                   ['V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N', 'H', 'L', 'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K'],  # V
                   ['L', 'E', 'Y', 'J', 'V', 'C', 'N', 'I', 'X', 'W', 'P', 'B', 'Q', 'M', 'D', 'R', 'T', 'A', 'K', 'Z', 'G', 'F', 'U', 'H', 'O', 'S'],  # Beta
                   ['F', 'S', 'O', 'K', 'A', 'N', 'U', 'E', 'R', 'H', 'M', 'B', 'T', 'I', 'Y', 'C', 'W', 'L', 'Q', 'P', 'Z', 'X', 'V', 'G', 'J', 'D']]  # Gamma

    wiring = list(zip(wiring_matrix[rotor_type.value - 1], base_contact))
    return wiring


def get_notch_by_RotorType(rotor_type):
    notchList = ["Q", "E", "V", "J", "Z", " ", " "]
    notch = notchList[rotor_type.value-1]
    return notch


if __name__ == '__main__':
    rot = rotor_from_name("III")
    rot.set_intial_position("B")
    print(rot.wiring)
    outChar = rot.encode_right_to_left("A")
    print(outChar)
    print(rot.encode_left_to_right(outChar))

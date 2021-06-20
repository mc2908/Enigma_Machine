from enum import Enum


class Rotor:

    def __init__(self, etype, wiring, notch):
        self.location = 0                                       # Rotor location in the Rotorcase 0 = rightmost rotor
        self.pos = 0                                            # Rotor current position
        self.default_pos = 0                                    # Rotor default position (set when the rotor is first added)
        self.ringSet = 0                                        # Rotor ring setting
        self.eType = etype                                      # Rotor Type
        self.wiring = [dict([(t[1], t[0]) for t in wiring])]    # Rotor wiring right to left
        self.wiring.append(dict(wiring))                        # Rotor wiring  left to right
        self.s_Notch = notch                                    # Rotor notch string
        self.num_Notch = Rotor.char2num_static(notch)           # Rotor notch integer (base 26)
        self.left_rotor = None                                  # Rotor object on the left side
        self.right_rotor = None                                 # Rotor object on the right side
        self.has_rotated = False                                # Flag to indicate whether or not the rotor has rotated for a given keyboard press
        self.char2num_dict = dict([(chr(x), x-65) for x in range(65, 91)])
        self.num2char_dict = dict([(x-65, chr(x)) for x in range(65, 91)])

    # set rotor initial position
    def set_initial_position(self, s_pos):
        if s_pos not in self.wiring[0].keys():
            raise ValueError(f"Rotor initial position {s_pos} does not exist. Please select a letter between A - Z")
        self.pos = self.char2num(s_pos)
        self.default_pos = self.char2num(s_pos)

    # reset the current rotor position to the initial default value
    def reset_to_default(self):
        self.pos = self.default_pos

    # set the rotor ring setting. it can either be defined as integer {1-26} or string {A-Z}
    def set_ring_setting(self, val):
        if type(val) is str:
            self.set_ring_setting_str(val)
        elif type(val) is int:
            self.set_ring_setting_int(val)
        else:
            raise TypeError("Ring setting can only be defined as integer or string")

    # set the rotor ring setting from a str input
    def set_ring_setting_str(self, val):
        if val in self.wiring[0].keys():
            self.ringSet = self.char2num(val - 1)
        else:
            raise ValueError(f"Ring setting {val} does not exist. Please enter either a number between 1- 26 or a character between A - Z")

    # set the rotor ring setting from an integer input
    def set_ring_setting_int(self, val):
        if 1 <= val <= 26:
            self.ringSet = val - 1
        else:
            raise ValueError(f"Ring setting {val} does not exist. Please enter either a number between 1- 26 or a character between A - Z")

    # method to make the rotor rotate of one position
    def rotate(self):
        if self.is_fourth_rotor():
            # the fourth rotor never rotates
            return
        # If this rotor isn't the last one and it is at the notch position, then first rotate the next rotor on the left
        if not self.is_leftmost_rotor() and self.is_at_notch():
            self.left_rotor.rotate()
        # increase rotor position by 1
        self.pos = (self.pos + 1) % 26
        # this rotor has rotate for this key stroke
        self.has_rotated = True

    # if this rotor is the leftmost one return True
    def is_leftmost_rotor(self):
        return self.left_rotor is None

    # if this rotor is the rightmost one return True
    def is_rightmost_rotor(self):
        return self.right_rotor is None

    # if this rotor is fourth and leftmost rotor return True
    def is_fourth_rotor(self):
        return self.location == 3

    # encode a letter in the forward direction (right to left). Char_in is the input coming for the previous element(rotor/ reflector/plugboard)
    def encode_right_to_left(self, char_in):
        # input validation
        wiring = self.wiring[0]
        if char_in not in wiring.keys():
            raise ValueError()
        # get the correct rotor right contact after adjusting rotor alignment for position and ring setting
        right_contact = self.adjust_rotor_contact_right_to_left(char_in)
        left_contact = wiring[right_contact]
        if self.is_leftmost_rotor():
            # the last rotor needs to pass adjusted contact information to the reflector because the reflector does not
            # know anything about the position of the rotors
            left_contact = self.num2char((self.char2num(left_contact) - self.pos + self.ringSet) % 26)
        return left_contact

    # encode a letter in the backward direction (left to right). Char_in is the input coming for the previous element(rotor/ reflector/plugboard)
    def encode_left_to_right(self, char_in: str):
        # input validation
        wiring = self.wiring[1]
        if char_in not in wiring.keys():
            raise ValueError()
        # get the correct rotor left contact after adjusting rotor alignment for position and ring setting
        left_contact = self.adjust_rotor_contact_left_to_right(char_in)
        # fetch the rotor right contact wired to the left one
        right_contact = wiring[left_contact]
        if self.is_rightmost_rotor():
            # The last rotor needs to pass the adjusted contact information to the reflector because the reflector does not
            # know anything about the position of the rotors
            right_contact = self.num2char((self.char2num(right_contact) - self.pos + self.ringSet) % 26)
        return right_contact

    # Get the right alignment between this rotor and the previous element on the right.
    def adjust_rotor_contact_right_to_left(self, char_in):
        right_rotor_pos = 0
        right_rotor_ring_set = 0
        # If this rotor is not the rightmost one, take into account the position and ring setting of the previous rotor
        # on the right to get the correct alignment between the two
        if not self.is_rightmost_rotor():
            right_rotor_pos = self.right_rotor.pos
            right_rotor_ring_set = self.right_rotor.ringSet
        contact_idx = (self.char2num(char_in) + self.pos - self.ringSet - right_rotor_pos + right_rotor_ring_set) % 26
        contact = self.num2char(contact_idx)
        return contact

    # method to get the right alignment between this rotor and the previous element on the left (i.e. rotor/ reflector/ plugboard)
    def adjust_rotor_contact_left_to_right(self, char_in):
        left_rotor_pos = 0
        left_rotor_ring_set = 0
        # If this rotor is not the leftmost one, take into account the position and ring setting of the previous rotor
        # on the left to get the correct alignment between the two
        if not self.is_leftmost_rotor():
            left_rotor_pos = self.left_rotor.pos
            left_rotor_ring_set = self.left_rotor.ringSet
        contact_idx = (self.char2num(char_in) + self.pos - self.ringSet - left_rotor_pos + left_rotor_ring_set) % 26
        contact = self.num2char(contact_idx)
        return contact

    # checking if this rotor is at the notch position
    def is_at_notch(self):
        return self.num_Notch == self.pos

    # map chars A - Z to ints 0 - 25
    def char2num(self, char):
        return self.char2num_dict[char]

    # map ints 0 - 25 to chars A - Z
    def num2char(self, num):
        return self.num2char_dict[num]

    # Overwriting the __eq__ inbuilt method: two rotors are considered equal if of the same type
    def __eq__(self, other):
        return self.eType == other.eType

    @ staticmethod
    def char2num_static(char):
        return ord(char) - ord("A")

    @staticmethod
    def num2Char_static(num):
        return chr(num + ord("A"))


# Enumerator class to uniquely identify the rotors
class RotorType(Enum):
    ND = 0
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5
    Beta = 6
    Gamma = 7


# Instantiate a rotor object from name
def rotor_from_name(rotor_name):
    rotor_type = rotor_type_from_name(rotor_name)
    wiring = get_wiring_by_rotorType(rotor_type)
    notch = get_notch_by_RotorType(rotor_type)
    this_rotor = Rotor(rotor_type, wiring, notch)
    return this_rotor


def rotor_type_from_name(rotor_name):
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
    elif rotor_name == "Gamma":  # must be Gamma
        rotor_type = RotorType.Gamma
    else:
        raise ValueError(f"Rotor {rotor_name} does not exist.")
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
    notch_list = ["Q", "E", "V", "J", "Z", " ", " "]
    notch = notch_list[rotor_type.value-1]
    return notch


if __name__ == '__main__':

    # test correct encoding
    rotor = rotor_from_name("I")
    assert (rotor.encode_right_to_left("A") == "E")
    assert (rotor.encode_left_to_right("A") == "U")


    # test worng inputs
    try:
        Rotor = rotor_from_name("HELLO")
        print("Test failed")
    except ValueError:
        print("Test passed")

    try:
        Rotor = rotor_from_name([])
        print("Test failed")
    except ValueError:
        print("Test passed")

    try:
        Rotor = rotor_from_name(342534)
        print("Test failed")
    except ValueError:
        print("Test passed")
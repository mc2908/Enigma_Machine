from Rotor import *
from Plugboard import *
from PlugLead import *
from Rotorscase import *
from Reflector import *


class EnigmaMachine:

    def __init__(self):
        self.plugboard = Plugboard()
        self.rotorcase = Rotorscase()
        self.reflector = None
        self.num_reflectors = 0

    def insert_plugleads(self, mapping):
        for pairs in mapping:
            self.plugboard.add(PlugLead(pairs))

    def remove_plugleads(self):
        self.plugboard.clear()


    def add_rotors(self, names):
        names.reverse()
        for name in names:
            rotor = rotor_from_name(name)
            self.rotorcase.add(rotor)

    def set_rotor_initial_pos(self, initialPositions):
        self.rotorcase.set_rotor_initial_positions(initialPositions)

    def set_rotor_ring_setting(self, ring_settings):
        self.rotorcase.set_rotor_initial_ring_setting(ring_settings)

    def remove_rotors(self):
        self.rotorcase.remove_all_rotors()

    def replace_rotors(self, rotor_names):
        # this function needs to be finished
        rotor_names.reverse()
        for idx, name in enumerate(rotor_names):
            if name == "" or Rotor_type_from_name(name) == self.rotorcase.rotors[idx].eType:
                continue
        self.rotorcase.rotors[idx] = rotor_from_name(name)

    def reset_default_rotor_position(self):
        self.rotorcase.reset_to_default_position()

    def add_reflector(self, name):
        if self.num_reflectors > 1:
            return
        self.reflector = reflector_from_name(name)
        self.num_reflectors += 1

    def replace_reflector(self, name, *args):
        self.reflector = reflector_from_name(name)
        if len(args) == 1:
            self.reflector.wiring = args[0]



    def encode(self, in_string):
        if not self.check_machine_components():
            print("Machine not setup properly")
            return
        out_string = ""
        for char in in_string:
            self.rotorcase.rotate()
            char_out = self.plugboard.encode(char)
            char_out = self.rotorcase.encode_right_to_left(char_out)
            char_out = self.reflector.encode(char_out)
            char_out = self.rotorcase.encode_left_to_right(char_out)
            char_out = self.plugboard.encode(char_out)
            out_string += char_out
        return out_string

    def check_machine_components(self):
        reflector_ok = self.reflector is not None
        rotors_ok = self.rotorcase.min_rotors <= self.rotorcase.num_rotors <= self.rotorcase.max_rotors
        plugboard_ok = True
        return reflector_ok and rotors_ok and plugboard_ok


if __name__ == '__main__':
    """
    em0 = EnigmaMachine()
    em0.add_rotor("IV",   "Z",   19)
    em0.add_rotor("III",  "V",   15)
    em0.add_rotor("II",   "E",   11)
    em0.add_rotor("I",    "Q",   7)
    em0.add_reflector("C")
    encoded_string = em0.encode("Z")
    print(encoded_string)
    """
    """
    em1 = EnigmaMachine()
    #em.add_rotor("IV",   "Z",   19)
    em1.add_rotor("III",  "Z",   1)
    em1.add_rotor("II",   "A",   1)
    em1.add_rotor("I",    "A",   1)
    em1.add_reflector("B")
    em1.insert_plugleads(["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])
    encoded_string = em1.encode("HELLOWORLD")
    #encoded_string = em1.encode("IVQYPNWYBCEXPOXCIPIUSHCZBNGBYS")
    print(encoded_string)
    """
    """
    em = EnigmaMachine()
    em.add_rotor("IV", "Z", 19)
    em.add_rotor("III", "V", 15)
    em.add_rotor("II", "E", 11)
    em.add_rotor("I", "Q", 7)
    em.add_reflector("C")
    encoded_string = em.encode("Z")
    print(encoded_string)

    em1 = EnigmaMachine()
    em1.add_rotor("IV", "Z", 19)
    em1.add_rotor("III", "V", 15)
    em1.add_rotor("II", "E", 11)
    em1.add_rotor("I", "Q", 7)
    em1.add_reflector("C")
    encoded_string = em1.encode("Z")
    print(encoded_string)


    
    em2 = EnigmaMachine()
    em2.add_rotor("I",    "P", 5)
    em2.add_rotor("Beta", "G", 3)
    em2.add_rotor("V",    "Z", 24)
    em2.add_rotor("IV",   "E", 18)
    em2.add_reflector("A")
    em2.insert_plugleads(["PC", "XZ", "FM", "QA", "ST", "NB", "HY", "OR", "EV", "IU"])
    encoded_string = em2.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(encoded_string)
    """

    """
    em3 = EnigmaMachine()
    em3.add_rotors(["IV", "V", "Beta", "I"])
    em3.set_rotor_initial_pos(["E", "Z", "G", "P"])
    em3.set_rotor_ring_setting([18, 24, 3, 5])
    em3.add_reflector("A")
    em3.insert_plugleads(["PC", "XZ", "FM", "QA", "ST", "NB", "HY", "OR", "EV", "IU"])
    encoded_string = em3.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(encoded_string)
    """

    em3 = EnigmaMachine()
    em3.add_rotors(["IV", "V", "Beta", "I"])
    em3.set_rotor_initial_pos(["E", "Z", "G", "P"])
    em3.set_rotor_ring_setting([18, 24, 3, 5])
    em3.add_reflector("A")
    em3.reflector.swap_wiring([('Y', 'A'), ('R', 'B'), ('U', 'C'), ('H', 'D'), ('Q', 'E'), ('S', 'F'), ('L', 'G'), ('D', 'H'), ('P', 'I'), ('X', 'J'), ('N', 'K'), ('G', 'L'), ('O', 'M'), ('K', 'N'), ('M', 'O'), ('I', 'P'), ('E', 'Q'), ('B', 'R'), ('F', 'S'), ('Z', 'T'), ('C', 'U'), ('W', 'V'), ('V', 'W'), ('J', 'X'), ('A', 'Y'), ('T', 'Z')])
    em3.insert_plugleads(["PC", "XZ", "FM", "QA", "ST", "NB", "HY", "OR", "EV", "IU"])
    encoded_string = em3.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(em3.reflector.wiring_type)
    print(encoded_string)

    em3.reflector.reset_std_wiring()
    em3.reset_default_rotor_position()
    encoded_string = em3.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(em3.reflector.wiring_type)
    print(encoded_string)

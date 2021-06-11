from rotor import *
from plugboard import *
from pluglead import *
from rotorscase import *
from reflector import *
import utility


class EnigmaMachine:

    def __init__(self):
        self.plugboard = Plugboard()        # Plugboard object is a container of Pluglead objects
        self.rotorcase = Rotorscase()       # Rotorcase object is a container of Rotor objects
        self.reflector = None               # Reflector object

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

    def set_rotor_initial_pos(self, initial_positions):
        self.rotorcase.set_rotor_initial_positions(initial_positions)

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
        if self.reflector is not None:
            raise ValueError(f"One reflector has already been added, to swap reflector use: replace_reflector(name) instead")
        self.reflector = reflector_from_name(name)

    def replace_reflector(self, name, *args):
        self.reflector = reflector_from_name(name)
        if len(args) == 1:
            self.reflector.wiring = args[0]

    def encode(self, message_in):
        if not self.check_machine_components():
            raise SystemError("Enigma Machine is not property set up. Check your inputs")
        message_in = utility.check_input_message_formatting(message_in)
        message_out = ""
        for char_in in message_in:
            self.rotorcase.rotate()
            char_out = self.plugboard.encode(char_in)
            char_out = self.rotorcase.encode_right_to_left(char_out)
            char_out = self.reflector.encode(char_out)
            char_out = self.rotorcase.encode_left_to_right(char_out)
            char_out = self.plugboard.encode(char_out)
            message_out += char_out
        return message_out

    def check_machine_components(self):
        reflector_ok = self.reflector is not None
        if not reflector_ok:
            print(f"Reflector has not been added. Please add a reflector")
        rotors_ok = self.rotorcase.min_rotors <= self.rotorcase.num_rotors <= self.rotorcase.max_rotors
        if not rotors_ok:
            print(f"Number of added rotors is less than the minimum required (3)")

        plugboard_ok = True
        return reflector_ok and rotors_ok and plugboard_ok

    @staticmethod
    def check_message_formatting(message: str):
        if type(message) is not str:
            raise TypeError("Encode method only accepts strings as input")
        message = message.upper()
        message = [x for x in message if 65 <= ord(x) <= 90]
        message = "".join(message)
        return message


if __name__ == '__main__':
    em0 = EnigmaMachine()
    em0.add_rotors(["I", "II", "III", "IV"])
    em0.set_rotor_initial_pos(["A", "A", "Z"])
    em0.set_rotor_ring_setting([1, 1, 1])
    em0.add_reflector("B")
    em0.insert_plugleads(["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])




    em0 = EnigmaMachine()
    em0.add_rotors(["I", "II", "III"])
    em0.set_rotor_initial_pos(["A", "A", "Z"])
    em0.set_rotor_ring_setting([1, 1, 1])
    em0.add_reflector("B")
    encoded_string = em0.encode("A")
    print(encoded_string)


    em1 = EnigmaMachine()
    em1.add_rotors(["I", "II", "III"])
    em1.set_rotor_initial_pos(["A", "A", "A"])
    em1.set_rotor_ring_setting([1, 1, 1])
    em1.add_reflector("B")
    encoded_string = em1.encode("A")
    print(encoded_string)


    em2 = EnigmaMachine()
    em2.add_rotors(["I", "II", "III"])
    em2.set_rotor_initial_pos(["Q", "E", "V"])
    em2.set_rotor_ring_setting([1, 1, 1])
    em2.add_reflector("B")
    encoded_string = em2.encode("A")
    print(encoded_string)


    em3 = EnigmaMachine()
    em3.add_rotors(["IV", "V", "Beta"])
    em3.set_rotor_initial_pos(["A", "A", "A"])
    em3.set_rotor_ring_setting([14, 9, 24])
    em3.add_reflector("B")
    encoded_string = em3.encode("H")
    print(encoded_string)

    em4 = EnigmaMachine()
    em4.add_rotors(["I", "II", "III", "IV"])
    em4.set_rotor_initial_pos(["Q", "E", "V", "Z"])
    em4.set_rotor_ring_setting([7, 11, 15, 19])
    em4.add_reflector("C")
    encoded_string = em4.encode("Z")
    print(encoded_string)



    em5 = EnigmaMachine()
    em5.add_rotors(["I", "II", "III"])
    em5.set_rotor_initial_pos(["A", "A", "Z"])
    em5.set_rotor_ring_setting([1, 1, 1])
    em5.add_reflector("B")
    em5.insert_plugleads(["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])
    encoded_string = em5.encode("HELLOWORLD")
    print(encoded_string)


    em6 = EnigmaMachine()
    em6.add_rotors(["IV", "V", "Beta", "I"])
    em6.set_rotor_initial_pos(["E", "Z", "G", "P"])
    em6.set_rotor_ring_setting([18, 24, 3, 5])
    em6.add_reflector("A")
    em6.insert_plugleads(["PC", "XZ", "FM", "QA", "ST", "NB", "HY", "OR", "EV", "IU"])
    encoded_string = em6.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(encoded_string)



    em3.reflector.reset_std_wiring()
    em3.reset_default_rotor_position()
    encoded_string = em3.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(em3.reflector.wiring_type)
    print(encoded_string)


    em7 = EnigmaMachine()
    em7.add_rotors(["I", "II", "III", "IV"])
    em7.set_rotor_initial_pos(["A", "A", "Z"])
    em7.set_rotor_ring_setting([1, 1, 1])
    em7.add_reflector("B")
    em7.insert_plugleads(["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])
    encoded_string = em7.encode("sdf**3494dfsa")
    print(encoded_string)
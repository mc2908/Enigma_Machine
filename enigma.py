from rotor import *
from plugboard import *
from pluglead import *
from rotorscase import *
from reflector import *
import utility
import time
import random
import matplotlib.pyplot as plt
import numpy as np

class EnigmaMachine:

    def __init__(self):
        self.plugboard = Plugboard()        # Plugboard object is a container of Pluglead objects
        self.rotorcase = Rotorscase()       # Rotorcase object is a container of Rotor objects
        self.reflector = None               # Reflector object

    # Insert plug leads
    #mapping = ["AB", "CF", "JD"....]
    def insert_plugleads(self, mapping):
        if type(mapping) != list:
            raise TypeError(" Plug lads mapping must be specified os list of strings e.g. ['AB', 'CF', 'JD',....]")
        for pairs in mapping:
            self.plugboard.add(PlugLead(pairs))

    def remove_plugleads(self):
        self.plugboard.clear()

    # Insert rotors
    def add_rotors(self, names):
        if type(names) != list:
            raise TypeError("Rotor names must be specified by a list of names e.g. ['I', 'II', 'III']")
        # Reversing the list because the names list exactly represent the rotor location.
        # The last element in the list is the rightmost rotor which  in turns needs to be added as the first one
        names.reverse()
        for name in names:
            # creating the rotor object
            rotor = rotor_from_name(name)
            self.rotorcase.add(rotor)

    def set_rotors_initial_pos(self, initial_positions):
        if type(initial_positions) != list:
            raise TypeError("Rotor initial positions must be specified by a list of upper case character"
                            " e.g. ['A', 'B', 'C']")
        self.rotorcase.set_rotors_initial_positions(initial_positions)

    def set_rotor_ring_setting(self, ring_settings):
        if type(ring_settings) != list:
            raise TypeError("Rotor initial positions must be specified by a list of integers or upper case character"
                            " e.g. [6, 1, 4] or [F, A, D]")
        self.rotorcase.set_rotor_initial_ring_setting(ring_settings)

    def remove_all_rotors(self):
        self.rotorcase.remove_all_rotors()

    def reset_default_rotor_position(self):
        self.rotorcase.reset_to_default_position()

    def add_reflector(self, name):
        if self.reflector is not None:
            raise ValueError(f"One reflector has already been added, to swap reflector use: replace_reflector(name) instead")
        self.reflector = reflector_from_name(name)

    # Replace existing reflector with a new one. Optionally a custom wiring can also be specified.
    def replace_reflector(self, name, *args):
        self.reflector = reflector_from_name(name)
        if len(args) == 1:
            self.reflector.wiring = args[0]

    def encode(self, message_in):
        if not self.check_machine_components():
            raise SystemError("Enigma Machine is not property set up. Check your inputs")
        # check that all components of the enigma machine are properly set up
        message_in = utility.check_input_message_formatting(message_in)
        message_out = ""
        # iteratively loop over the input message and encode one letter at the time
        for char_in in message_in:
            # rotate the rotors first
            self.rotorcase.rotate()
            # encode the input char
            char_out = self.plugboard.encode(char_in)
            char_out = self.rotorcase.encode_right_to_left(char_out)
            char_out = self.reflector.encode(char_out)
            char_out = self.rotorcase.encode_left_to_right(char_out)
            char_out = self.plugboard.encode(char_out)
            # append the encoded char to the end of the output string
            message_out += char_out
        return message_out

    def check_machine_components(self):
        # there must be one reflector
        reflector_ok = self.reflector is not None
        if not reflector_ok:
            print(f"Reflector has not been added. Please add a reflector")
        # make sure that rotors have been added to the rotorcase
        rotors_ok = self.rotorcase.min_rotors <= self.rotorcase.num_rotors <= self.rotorcase.max_rotors
        if not rotors_ok:
            print(f"Number of added rotors is less than the minimum required (3)")
        return reflector_ok and rotors_ok


    # method to plot Enigma machine time complexity from input size varying from  1 to n
    @staticmethod
    def time_complexity(n):
        em0 = EnigmaMachine()
        em0.add_rotors(["I", "II", "III", "IV"])
        em0.set_rotors_initial_pos(["A", "A", "Z", "A"])
        em0.set_rotor_ring_setting([1, 1, 1, 1])
        em0.add_reflector("B")
        string = ""
        nchar_arr = np.zeros(n // 10)
        time_arr = np.zeros(n // 10)
        for i in range(0, n//10, 1):
            string = string + "".join([Rotor.num2Char_static(random.randint(0, 25)) for _ in range(10)])
            em0.reset_default_rotor_position()
            t_start = time.time()
            encoded_string = em0.encode(string)
            t_elapsed = time.time() - t_start
            time_arr[i] = t_elapsed * 10**3  # time in ms
            nchar_arr[i] = 10 * (i+1)
        fig, ax = plt.subplots()  # Create a figure and an axes.
        ax.plot(nchar_arr, time_arr,)  # Plot some data on the axes.
        ax.set_xlabel('Input string length [num of letters]')  # Add an x-label to the axes.
        ax.set_ylabel('Time [ms]')  # Add a y-label to the axes.
        ax.set_title("Enigma Machine Time complexity")  # Add a title to the axes.
        ax.legend()  # Add a legend.
        plt.show()




if __name__ == '__main__':

    EnigmaMachine.time_complexity(1000)


    em0 = EnigmaMachine()
    em0.add_rotors(["I", "II", "III"])
    em0.set_rotors_initial_pos(["A", "A", "Z"])
    em0.set_rotor_ring_setting([1, 1, 1])
    em0.add_reflector("B")
    encoded_string = em0.encode("A")
    print(encoded_string)


    em1 = EnigmaMachine()
    em1.add_rotors(["I", "II", "III"])
    em1.set_rotors_initial_pos(["A", "A", "A"])
    em1.set_rotor_ring_setting([1, 1, 1])
    em1.add_reflector("B")
    encoded_string = em1.encode("A")
    print(encoded_string)


    em2 = EnigmaMachine()
    em2.add_rotors(["I", "II", "III"])
    em2.set_rotors_initial_pos(["Q", "E", "V"])
    em2.set_rotor_ring_setting([1, 1, 1])
    em2.add_reflector("B")
    encoded_string = em2.encode("A")
    print(encoded_string)


    em3 = EnigmaMachine()
    em3.add_rotors(["IV", "V", "Beta"])
    em3.set_rotors_initial_pos(["A", "A", "A"])
    em3.set_rotor_ring_setting([14, 9, 24])
    em3.add_reflector("B")
    encoded_string = em3.encode("H")
    print(encoded_string)

    em4 = EnigmaMachine()
    em4.add_rotors(["I", "II", "III", "IV"])
    em4.set_rotors_initial_pos(["Q", "E", "V", "Z"])
    em4.set_rotor_ring_setting([7, 11, 15, 19])
    em4.add_reflector("C")
    encoded_string = em4.encode("Z")
    print(encoded_string)



    em5 = EnigmaMachine()
    em5.add_rotors(["I", "II", "III"])
    em5.set_rotors_initial_pos(["A", "A", "Z"])
    em5.set_rotor_ring_setting([1, 1, 1])
    em5.add_reflector("B")
    em5.insert_plugleads(["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])
    encoded_string = em5.encode("HELLOWORLD")
    print(encoded_string)


    em6 = EnigmaMachine()
    em6.add_rotors(["IV", "V", "Beta", "I"])
    em6.set_rotors_initial_pos(["E", "Z", "G", "P"])
    em6.set_rotor_ring_setting([18, 24, 3, 5])
    em6.add_reflector("A")
    em6.insert_plugleads(["PC", "XZ", "FM", "QA", "ST", "NB", "HY", "OR", "EV", "IU"])
    encoded_string = em6.encode("BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI")
    print(encoded_string)


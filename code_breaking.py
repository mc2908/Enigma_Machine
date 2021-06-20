from enigma import *
import itertools
from frozen_class import *
import time
import math
import utility


class CodeBreaking(FrozenClass):
    def __init__(self):
        self.__available_rotors = ["I", "II", "III", "IV", "V", "Beta", "Gamma"]
        self.__available_ring_setting = list(range(1, 27))
        self.__available_rotor_pos = [chr(x) for x in range(65, 65 + 26)]
        self.__available_plugs = [chr(x) for x in range(65, 65 + 26)]
        self.__available_reflectors = ["A", "B", "C"]
        self.__em = EnigmaMachine()
        self.__rotors_name = []
        self.__rotors_positions = []
        self.__rotors_ring_setting = []
        self.__rotor_num = 3
        self.set_number_of_rotors(3)
        self.__reflector_name = self.__available_reflectors
        self.__plugboard_connection = ["??", "??"]
        self.__rotor_name_comb = []
        self.__rotor_pos_comb = []
        self.__rotor_ring_setting_comb = []
        self.__plugboard_connection_comb = []
        self.__reflectors_comb = []
        self.__reflector_wiring_comb = []
        self.allow_reflector_modifications = False
        self.reflector_pairs_to_swap = 0
        # Words DB taken from the github repository shown below:
        # https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-no-swears.txt
        self.__common_words_DB = []
        self.load_common_words_DB("google-10000-english-no-swears.txt")
        self.decoded_string_DB = {}
        self.settings_DB = {}
        self._freeze()

    def set_number_of_rotors(self, n):
        self.__rotor_num = n
        self.__rotors_name = [self.__available_rotors for _ in range(0, n)]
        self.__rotors_positions = [self.__available_rotor_pos for _ in range(0, n)]
        self.__rotors_ring_setting = [self.__available_ring_setting for _ in range(0, n)]

    # Set known rotor constraints:
    def set_rotors(self, rotors):
        if type(rotors) is not list:
            raise TypeError("Rotors constraints must be a list: e.g [['Gamma', 'II'], ['II', 'IV'] ['III', 'V']]")
        if len(rotors) != self.__rotor_num:
            raise ValueError("The number of rotor constraints must match the number of rotors")
        for rotor_elm in rotors:
            if type(rotor_elm) is not list:
                raise TypeError("Each rotor constraint must be a list: e.g [['Gamma', 'II'], ['II', 'IV'] ['III', 'V']]")
            for r in rotor_elm:
                if type(r) is not str:
                    raise TypeError("Each element of each rotor constrait must be a string: e.g [['Gamma', 'II'], ['II', 'IV'] ['III', 'V']]")
                if r not in self.__available_rotors:
                    raise ValueError(f"rotor name {r} is not valid constraint")
        self.__rotors_name = rotors

    # set known rotor position constraints:
    def set_rotor_positions(self, positions):
        if type(positions) is not list:
            raise TypeError("Rotors positions constraint must be a list: e.g [['A', 'B'], ['Z'] ['A', 'B', 'C',...,'Z']]")
        if len(positions) != self.__rotor_num:
            raise ValueError("The number of rotor position constraints must match the number of rotors")
        for position_elm in positions:
            if type(position_elm) is not list:
                raise TypeError("Each rotor position constraint must be a list: e.g [['A', 'B'], ['Z'] ['A', 'B', 'C',...,'Z']]")
            for pos in position_elm:
                if type(pos) is not str:
                    raise TypeError("Each element of each rotor position constraint must be a string: e.g [['A', 'B'], ['Z'] ['A', 'B', 'C',...,'Z']]")
                if pos not in self.__available_rotor_pos:
                    raise ValueError(f"rotor position {pos} is not valid constraint")
        self.__rotors_positions = positions

    # Set known ring settings constraints:
    def set_ring_settings(self, ring_settings):
        if type(ring_settings) is not list:
            raise TypeError("Ring setting constraints must be a list: e.g [[1, 2], [25] [1, 2, 3,...,25]]")
        if len(ring_settings) != self.__rotor_num:
            raise ValueError("The number of ring setting constraints must match the number of rotors")
        for ring_set_elm in ring_settings:
            if type(ring_set_elm) is not list:
                raise TypeError("Each rotor ring settings constraint must be a list: e.g [[1, 2], [25] [1, 2, 3,...,25]] ")
            for ring in ring_set_elm:
                if type(ring) is not int:
                    raise TypeError("Each element of each rotor ring settings constraint must be an integer:  e.g [[1, 2], [25] [1, 2, 3,...,25]]")
                if ring not in self.__available_ring_setting:
                    raise ValueError(f"ring setting {ring} is not valid constraint")
        self.__rotors_ring_setting = ring_settings

    # Set known plugboard constraints:
    def set_plugboard_connections(self, connections):
        if type(connections) is not list:
            raise TypeError("Plug board constraints must be a list: e.g. ['AB', 'C?','??','F?']")
        if len(connections) > 13:
            raise ValueError("The number constraint cannot be higher than 13 as the Plug Board only accepts 13 plug leads")
        for plug_lead in connections:
            if type(plug_lead) is not str:
                raise TypeError("Each plug lead pair must be a string:  e.g. ['AB', 'C?','??','F?']")
            if len(plug_lead) != 2:
                raise ValueError("Each plug lead pair must have length 2:  e.g. ['AB', 'C?','??','F?']")
            for contact in plug_lead:
                if contact not in self.__available_plugs + ["?"]:
                    raise ValueError(f"contact {contact} is not a valid plug board contact")
        self.__plugboard_connection = connections

    # Set known reflector constraints:
    def set_reflectors(self, reflectors):
        if type(reflectors) is not list:
            raise TypeError("Reflector constraints must be a list:  e.g. ['A','B','C']")
        for this_reflector in reflectors:
            if type(this_reflector) is not str:
                raise TypeError("Each known Reflector Name constraint must be a string:  e.g. ['A','B','C']")
            if this_reflector not in self.__available_reflectors:
                raise ValueError(f"reflector {this_reflector} is not a valid reflector name")
        self.__reflector_name = reflectors

    # Helper method to load the common words Data base.
    def load_common_words_DB(self, file_path):
        with open(file_path, 'r') as file:
            DB = file.readlines()
        words_DB = map(lambda s: s.strip("\n"), DB)
        words_BB = map(lambda s: s.upper(), words_DB)
        self.__common_words_DB = list(words_BB)

    def generate_combination(self):
        # Calculate possible combinations for Rotor Position
        all_comb = itertools.product(*[self.__available_rotor_pos for _ in range(self.__rotor_num)])
        # Filter the Rotor position Combination to only keep those ones which satisfy the constraints
        self.__rotor_pos_comb = CodeBreaking.filter_combinations(self.__rotors_positions, all_comb)

        # Calculate possible combination for Rotor Ring Setting
        all_comb = itertools.product(*[self.__available_ring_setting for _ in range(self.__rotor_num)])
        # Filter the Rotor Ring Setting Combination to only keep those ones which satisfy the constraints
        self.__rotor_ring_setting_comb = CodeBreaking.filter_combinations(self.__rotors_ring_setting, all_comb)

        # Calculate possible combination for Rotors nName
        comb = list(itertools.permutations(self.__available_rotors, self.__rotor_num))
        # Filter the Rotor combination to only keep those ones which satisfy the constraints
        self.__rotor_name_comb = CodeBreaking.filter_combinations(self.__rotors_name, comb)

        # Calculate possible combination for Reflector
        comb = list(itertools.combinations(self.__available_reflectors, 1))
        comb_list = [x for x, in comb if x in self.__reflector_name]
        self.__reflectors_comb = comb_list

    # Method to compute the total number of comination possible for any given input settings
    def calculate_combinations_number(self):
        comb_num_rotors = len(self.__rotor_name_comb)
        comb_num_rotor_pos = len(self.__rotor_pos_comb)
        comb_num_ring_set = len(self.__rotor_ring_setting_comb)
        comb_num_reflector = len(self.__reflectors_comb)
        comb_num_plugboard = self.calc_plugboard_comb_num()
        if self.allow_reflector_modifications:
            n = self.reflector_pairs_to_swap
            comb_reflector_wire = int(math.factorial(13) / math.factorial(13 - n) / math.factorial(n) * utility.doubleFactorial(n-1))
        else:
            comb_reflector_wire = 1
        tot_comb_num = comb_num_rotors * comb_num_rotor_pos * comb_num_ring_set * comb_num_reflector * comb_num_plugboard * comb_reflector_wire
        return tot_comb_num

    def calc_plugboard_comb_num(self):
        plugboard_connections = self.__plugboard_connection
        letters = "".join(plugboard_connections)
        num_missing_letter = letters.count("?")
        num_full_pairs = plugboard_connections.count("??")
        num_half_pairs = num_missing_letter - num_full_pairs * 2
        known_letters = letters.replace("?", "")
        num_know_letters = len(known_letters)
        letters_rem = 26 - num_know_letters
        if num_full_pairs == 0:
            ncomb_full_pair = 1
        else:
            ncomb_full_pair = math.factorial(letters_rem) / (math.factorial(letters_rem - num_full_pairs * 2) * 2 ** num_full_pairs * math.factorial(num_full_pairs))
        letters_rem = letters_rem - num_full_pairs * 2
        ncomb_half_pairs = math.factorial(letters_rem) / math.factorial(letters_rem - num_half_pairs)
        ncomb_tot = int(ncomb_full_pair * ncomb_half_pairs)
        return ncomb_tot

    # Apply all possible combinations to the enigma machina to decode the "encoded_sting".
    # If the string contains one or more words specified in crib_list, the decoded message gets stored and scored based
    # on how many common words it contains.
    # The function returns the decoded message with the highest score plus the enigma machine settings.
    def break_code(self, encoded_string, crib_list):
        # Calculate the possible combinations for the enigma machine settings
        self.generate_combination()
        self.decoded_string_DB = {}
        self.settings_DB = {}
        comb_num = self.calculate_combinations_number()
        if not self.allow_reflector_modifications:
            self.reflector_pairs_to_swap = 0
        no_crib_given = False
        if len(crib_list) == 0:
            crib_list = ["A"]
            no_crib_given = True
        crib_list = list(map(lambda l: utility.check_input_message_formatting(l, "Crib Word"), crib_list))
        print(f"The number of total possible combinations is {comb_num}")
        for plug_setting in plugboard_combinations_gen(self.__plugboard_connection, self.__available_plugs):
            # Remove the previously applied plug leads
            self.__em.remove_plugleads()
            # Insert new ones
            self.__em.insert_plugleads(plug_setting)
            for this_reflector in self.__reflectors_comb:
                # Replace reflector
                self.__em.replace_reflector(this_reflector)
                # Generate all allowed reflector wiring combination, if reflector_pairs_to_swap = 0 it generates the
                # standard configuration based on the reflector name
                reflector_wiring_comb = reflector_wiring_comb_gen(get_wiring_by_ReflectorType(reflectorType_from_name(this_reflector)), self.reflector_pairs_to_swap)
                for reflector_wiring in reflector_wiring_comb:
                    # Apply reflector wiring combination
                    self.__em.reflector.swap_wiring(reflector_wiring)
                    for rotors in self.__rotor_name_comb:
                        # Add the new rotors combination
                        self.__em.add_rotors(list(rotors))
                        for pos in self.__rotor_pos_comb:
                            # Apply new rotor initial position
                            self.__em.set_rotors_initial_pos(list(pos))
                            for setting in self.__rotor_ring_setting_comb:
                                # Apply new ring settings
                                self.__em.set_rotors_ring_setting(list(setting))
                                # Before decoding the string reset the rotors to their default initial position
                                self.__em.reset_default_rotor_position()
                                decoded_string = self.__em.encode(encoded_string)
                                for crib in crib_list:
                                    if crib in decoded_string or no_crib_given:
                                        # Score the decoded string based on its common word content
                                        string_score = self.common_words_analysis(decoded_string)
                                        self.decoded_string_DB[decoded_string] = string_score
                                        # Report only the differences between the standard and the modified reflector configurations
                                        wiring_diff = self.__em.reflector.find_wiring_changes()
                                        self.settings_DB[decoded_string] = [rotors, pos, setting, plug_setting,
                                                                            this_reflector, wiring_diff]
        # Find the decoded message with the highest score.
        if len(self.decoded_string_DB.keys()) == 0:
            bretval = False
            out_string = ""
            best_score = []
            settings = [[] for _ in range(6)]
        else:
            bretval = True
            best_score, out_string = max([(v, k) for k, v in self.decoded_string_DB.items()])
            # Retrieve the Enigma Machine setting which generated the decoded message.
            settings = self.settings_DB[out_string]
        return bretval, out_string, best_score, settings

    # Method to score an input string based on how many common words it contains. longer words are given higher score.
    # Standard common_words_DB contains the most common 10000 words in english language excluding swear words
    def common_words_analysis(self, phrase):
        score = 0
        for word in self.__common_words_DB:
            # Do not score words with length less than 3 e.g. IS, TO, AT, IN, etc...
            # they are more likely to be found in a randomly generated string
            if word in phrase and len(word) > 2:
                score += len(word)
        return score

    # Helper methods which filters out the elements in all_comb if the ith sub-element of the element
    # is not present in the i(ith) element of constraints
    @staticmethod
    def filter_combinations(constraints, all_comb):
        if len(constraints) == 3:
            filtered_comb = [(x, y, z) for x, y, z in all_comb if
                             x in constraints[0] and y in constraints[1] and z in constraints[2]]
        elif len(constraints) == 4:
            filtered_comb = [(x, y, z, w) for x, y, z, w in all_comb if
                             x in constraints[0] and y in constraints[1] and z in constraints[2] and w in
                             constraints[3]]
        else:
            raise ValueError(f"constraints has wrong length ({len(constraints)}), Expected 3 or 4")
        return filtered_comb

    @staticmethod
    def code1():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["Beta"], ["Gamma"], ["V"]])
        cb.set_rotor_positions([["M"], ["J"], ["M"]])
        cb.set_ring_settings([[4], [2], [14]])
        cb.set_plugboard_connections(["KI", "NX", "FL"])
        print("Decrypting Code1 with Crib info....")
        solution = cb.break_code("DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ", ["SECRETS"])
        t_elapsed_code_1 = time.time() - t_start
        print_results(solution, t_elapsed_code_1, 1)

    @staticmethod
    def code1noCrib():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["Beta"], ["Gamma"], ["V"]])
        cb.set_rotor_positions([["M"], ["J"], ["M"]])
        cb.set_ring_settings([[4], [2], [14]])
        cb.set_plugboard_connections(["KI", "NX", "FL"])
        print("Decrypting Code1 with no Crib info....")
        solution = cb.break_code("DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ", [])
        t_elapsed_code_1 = time.time() - t_start
        print_results(solution, t_elapsed_code_1, 1)

    @staticmethod
    def code2():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["Beta"], ["I"], ["III"]])
        cb.set_ring_settings([[23], [2], [10]])
        cb.set_reflectors(["B"])
        cb.set_plugboard_connections(["VH", "PT", "ZG", "BJ", "EY", "FS"])
        print("Decrypting Code2 with Crib info....")
        solution = cb.break_code("CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH", ["UNIVERSITY"])
        t_elapsed_code_2 = time.time() - t_start
        print_results(solution, t_elapsed_code_2, 2)

    @staticmethod
    def code2noCrib():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["Beta"], ["I"], ["III"]])
        cb.set_ring_settings([[23], [2], [10]])
        cb.set_reflectors(["B"])
        cb.set_plugboard_connections(["VH", "PT", "ZG", "BJ", "EY", "FS"])
        print("Decrypting Code2 with no Crib info....")
        solution = cb.break_code("CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH", [])
        t_elapsed_code_2 = time.time() - t_start
        print_results(solution, t_elapsed_code_2, 2)

    @staticmethod
    def code3():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["Beta", "Gamma", "IV", "II"], ["Beta", "Gamma", "IV", "II"], ["Beta", "Gamma", "IV", "II"]])
        cb.set_ring_settings([[x for x in range(1, 27) if x % 2 == 0 and (x < 10 or x > 19)] for _ in range(3)])
        cb.set_rotor_positions([["E"], ["M"], ["Y"]])
        cb.set_plugboard_connections(["FH", "TS", "BE", "UQ", "KD", "AL"])
        print("Decrypting Code3 with Crib info....")
        solution = cb.break_code("ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY", ["THOUSANDS"])
        t_elapsed_code_3 = time.time() - t_start
        print_results(solution, t_elapsed_code_3, 3)

    @staticmethod
    def code3noCrib():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["Beta", "Gamma", "IV", "II"], ["Beta", "Gamma", "IV", "II"], ["Beta", "Gamma", "IV", "II"]])
        cb.set_ring_settings([[x for x in range(1, 27) if x % 2 == 0 and (x < 10 or x > 19)] for _ in range(3)])
        cb.set_rotor_positions([["E"], ["M"], ["Y"]])
        cb.set_plugboard_connections(["FH", "TS", "BE", "UQ", "KD", "AL"])
        print("Decrypting Code3 with no Crib info....")
        solution = cb.break_code("ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY", [])
        t_elapsed_code_3 = time.time() - t_start
        print_results(solution, t_elapsed_code_3, 3)

    @staticmethod
    def code4():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["V"], ["III"], ["IV"]])
        cb.set_ring_settings([[24], [12], [10]])
        cb.set_rotor_positions([["S"], ["W"], ["U"]])
        cb.set_plugboard_connections(["WP", "RJ", "A?", "VF", "I?", "HN", "CG", "BS"])
        cb.set_reflectors(["A"])
        print("Decrypting Code4 with Crib info....")
        solution = cb.break_code("SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW", ["TUTOR"])
        t_elapsed_code_4 = time.time() - t_start
        print_results(solution, t_elapsed_code_4, 4)

    @staticmethod
    def code4noCrib():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["V"], ["III"], ["IV"]])
        cb.set_ring_settings([[24], [12], [10]])
        cb.set_rotor_positions([["S"], ["W"], ["U"]])
        cb.set_plugboard_connections(["WP", "RJ", "A?", "VF", "I?", "HN", "CG", "BS"])
        cb.set_reflectors(["A"])
        print("Decrypting Code4 with no Crib info....")
        solution = cb.break_code("SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW", [])
        t_elapsed_code_4 = time.time() - t_start
        print_results(solution, t_elapsed_code_4, 4)

    @staticmethod
    def code5():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["V"], ["II"], ["IV"]])
        cb.set_ring_settings([[6], [18], [7]])
        cb.set_rotor_positions([["A"], ["J"], ["L"]])
        cb.set_plugboard_connections(["UG", "IE", "PO", "NX", "WT"])
        cb.allow_reflector_modifications = True
        cb.reflector_pairs_to_swap = 4
        print("Decrypting Code5 with Crib info....")
        solution = cb.break_code("HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX",
                                                         ["FACEBOOK", "TWITTER", "INSTAGRAM", "LINKEDIN", "YOUTUBE"])
        t_elapsed_code_5 = time.time() - t_start
        print_results(solution, t_elapsed_code_5, 5)

    @staticmethod
    def code5noCrib():
        t_start = time.time()
        cb = CodeBreaking()
        cb.set_rotors([["V"], ["II"], ["IV"]])
        cb.set_ring_settings([[6], [18], [7]])
        cb.set_rotor_positions([["A"], ["J"], ["L"]])
        cb.set_plugboard_connections(["UG", "IE", "PO", "NX", "WT"])
        cb.allow_reflector_modifications = True
        cb.reflector_pairs_to_swap = 4
        print("Decrypting Code5 with no Crib info....")
        solution = cb.break_code("HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX", [])
        t_elapsed_code_5 = time.time() - t_start
        print_results(solution, t_elapsed_code_5, 5)

    @staticmethod
    def all_codes():
        t_start_tot = time.time()
        CodeBreaking.code1()
        CodeBreaking.code2()
        CodeBreaking.code3()
        CodeBreaking.code4()
        CodeBreaking.code5()
        t_elapsed = time.time() - t_start_tot
        print(f"Total execution time: {round(t_elapsed,3)}")

    @staticmethod
    def all_codes_no_crib():
        t_start_tot = time.time()
        CodeBreaking.code1noCrib()
        CodeBreaking.code2noCrib()
        CodeBreaking.code3noCrib()
        CodeBreaking.code4noCrib()
        CodeBreaking.code5noCrib()
        t_elapsed = time.time() - t_start_tot
        print(f"Total execution time: {round(t_elapsed,3)}")


# Generator which creates all possible combinations of plug board connections from given constraints
# plugboard_connection = list which specifies the number of plug_leads and their definition e.g. ["AB", "X?", "??"]
# each pair can be fully defined "AB", partially defined "X?" or not defined "??"
# plugboard_connection = list with all available contacts in the plug board ["A", "B", "C", "D",......, "Z"]
def plugboard_combinations_gen(plugboard_connection, all_available_plugs):
    half_terms = [x for x in plugboard_connection if "?" in x and "??" not in x]
    letters = "".join(plugboard_connection)
    num_missing_letter = letters.count("?")
    num_full_pairs = plugboard_connection.count("??")
    num_half_pairs = num_missing_letter - num_full_pairs * 2
    letters = sorted(letters)
    known_letter_set = set(letters) - {"?"}
    remaining_plugs = set(all_available_plugs) - known_letter_set
    # Generating all combination of contacts to fill in the half defined plug leads
    # e.g.["AB", "C?", "??", "?H"] --> [("D", "E"), ("D", "F"), ("D", "G"), ("D", "H").....("E","Z")....]
    half_pairs = itertools.combinations(remaining_plugs, num_half_pairs)
    for half_pair in half_pairs:
        updated_remaining_letters = remaining_plugs - set(half_pair)
        # Generating all combination of contacts to fill in the undefined plug leads
        # e.g.["AB", "C?", "??", "?H"] --> [("D", "E"), ("D", "F"), ("D", "G"), ("D", "H").....("E","Z")....]
        full_pairs = full_pair_combination_gen(updated_remaining_letters, num_full_pairs)
        for full_pair in full_pairs:
            plug_board_connection_temp = plugboard_connection.copy()
            # filling in the the full pairs e.g. ["AB", "C?", "??", "?H"] --> ["AB", "C?", "DF", "?H"]
            for i in range(len(full_pair)):
                idx = plug_board_connection_temp.index("??")
                plug_board_connection_temp[idx] = "".join(list(full_pair[i]))
            # calculating all permutation of half pairs
            for perm_half_pair in itertools.permutations(half_pair, num_half_pairs):
                out_plug_board_connection = plug_board_connection_temp.copy()
                # substituting the half pairs
                for idx, hlf_term in enumerate(half_terms):
                    idx_term = out_plug_board_connection.index(hlf_term)
                    new_pair = hlf_term.replace("?", perm_half_pair[idx])
                    out_plug_board_connection[idx_term] = new_pair
                yield out_plug_board_connection


# Generator to create n unique plug leads (pair of letter) from a list of available contacts in the plugboard
def full_pair_combination_gen(plug_board_contacts, n):
    # generate all possible n pairs of letters
    all_full_pair_comb = itertools.combinations(itertools.combinations(plug_board_contacts, 2), n)
    # iterate over the possible combination and only yield the ones where no contacts are repeated.
    for pair in all_full_pair_comb:
        if len(set("".join([x + y for x, y in pair]))) == n * 2:
            yield pair


# Generator which yields all possible reflector wiring combinations by swapping n pairs of contacts
def reflector_wiring_comb_gen(std_wiring, n):
    # On the first call return the standard wiring
    yield std_wiring
    all_right_contacts = [x for (_, x) in std_wiring]
    all_left_contacts = [y for (y, _) in std_wiring]
    all_right_contacts_unique = []
    all_left_contacts_unique = []
    for idx, rc in enumerate(all_right_contacts):
        lc = all_left_contacts[idx]
        if lc in all_right_contacts_unique:
            continue
        # List that contains the reflector contacts which receive the input char
        all_right_contacts_unique.append(rc)
        # List that contains the respective contacts the input char is mapped to by the reflector
        all_left_contacts_unique.append(lc)
    # Generate all possible combination of right contact to swap
    right_contact_to_swap_comb = itertools.combinations(all_right_contacts_unique, n)
    for right_contacts_list in right_contact_to_swap_comb:
        # Only swap wires in pairs
        if n % 2 == 1:
            raise ValueError("Pairs of contacts to swap must be an even number")
        right_contacts_pairs_comb = full_pair_combination_gen(right_contacts_list, n // 2)
        for right_contact_pairs in right_contacts_pairs_comb:
            # Pre create a copy of the input wiring which will be later on modified with the new contact pairs
            new_wiring = std_wiring.copy()
            new_left_contact_pairs = []
            # Iterate over the possible right pairs
            for a_right_contact_pair in right_contact_pairs:
                # Find the correspondent left contact
                this_wire_pair_left_contact = [y for (y, x) in std_wiring if x in a_right_contact_pair]
                # Swap the left contacts
                new_left_contact_pairs.append((this_wire_pair_left_contact[1], this_wire_pair_left_contact[0]))
            # Merge the right contact pairs with the swapped left contact pairs
            new_connections = list(zip(join_iterable_2_tuple(new_left_contact_pairs), join_iterable_2_tuple(right_contact_pairs)))
            # Replace old connections with new ones in new_wiring
            for conn in new_connections:
                left_cont, right_cont = conn
                idx = Rotor.char2num_static(right_cont)
                assert (right_cont != new_wiring[idx][0])
                new_wiring[idx] = conn
                idx_complementary = Rotor.char2num_static(left_cont)
                new_wiring[idx_complementary] = conn[1], conn[0]
            # From the second call onwards return the modified wiring
            yield new_wiring


def join_iterable_2_tuple(iterable):
    out = ()
    for x, y in iterable:
        out = out + (x,) + (y,)
    return out


# Helper function which prints the results
def print_results(solution, t_elapsed, n):
    bfound, crakedstring, score, settings = solution
    if bfound:
        print(f"The decoded messages is {crakedstring} with a score of {score}")
        print(f"The Enigma Machine settings are:\n"
              f" Rotors: {settings[0]}\n"
              f" Rotor positions: {settings[1]}\n"
              f" Rotor settings: {settings[2]}\n"
              f" Plugboard connections: {settings[3]}\n"
              f" Reflector: {settings[4]}\n"
              f" Not standard Reflector connections: {settings[5]}")
    else:
        print(f"No solutions has been found which match the given crib(s)")
    print(f"Code {n} execution time: {round(t_elapsed, 3)} seconds\n")


if __name__ == '__main__':

    CodeBreaking.all_codes()

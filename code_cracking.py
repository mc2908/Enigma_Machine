from enigma import *
import itertools


class CodeCraking:
    def __init__(self):
        self.available_rotors = ["I", "II", "III", "IV", "V", "Beta", "Gamma"]
        self.available_ring_setting = list(range(1, 27))
        self.available_rotor_pos = [chr(x) for x in range(65, 65 + 26)]
        self.available_plugs = [chr(x) for x in range(65, 65 + 26)]
        self.available_reflectors = ["A", "B", "C"]
        self.em = EnigmaMachine()
        self.rotors_name = [self.available_rotors for _ in range(0, 3)]
        self.rotors_positions = [self.available_rotor_pos for _ in range(0, 3)]
        self.rotors_ring_setting = [self.available_ring_setting for _ in range(0, 3)]
        self.reflector_name = self.available_reflectors
        self.plugboard_connection = ["??", "??"]
        self.rotor_name_comb = []
        self.rotor_pos_comb = []
        self.rotor_ring_setting_comb = []
        self.plugboard_connection_comb = []
        self.reflectors_comb = []
        self.reflector_wiring_comb = []
        self.allow_reflector_modifications = False
        self.pairs_to_swap = 0
        self.load_common_words_DB("google-10000-english-no-swears.txt")

    def set_crib_word(self, cribword):
        self.crib = cribword

    def load_common_words_DB(self, file_path):
        with open(file_path, 'r') as file:
            DB = file.readlines()
        words_DB = map(lambda s: s.strip("\n"), DB)
        words_BB = map(lambda s: s.upper(), words_DB)
        self.common_words_DB = list(words_BB)

    def calculate_total_combination(self):
        # calculate combination for Rotor Position
        letter_list_copy = self.available_rotor_pos.copy()
        comb = list(itertools.product(letter_list_copy, letter_list_copy,letter_list_copy))
        comb_list = [(x, y, z) for x, y, z in comb if x in self.rotors_positions[0] and y in self.rotors_positions[1] and z in self.rotors_positions[2]]
        self.rotor_pos_comb = comb_list

        # calculate combination for  rotor ring setting
        rotors_ring_setting_copy = self.available_ring_setting
        comb = list(itertools.product(rotors_ring_setting_copy, rotors_ring_setting_copy, rotors_ring_setting_copy))
        comb_list = [(x, y, z) for x, y, z in comb if x in self.rotors_ring_setting[0] and y in self.rotors_ring_setting[1] and z in self.rotors_ring_setting[2]]
        self.rotor_ring_setting_comb = comb_list

        # calculate combination for rotors name
        rotor_name_copy = self.available_rotors
        comb = list(itertools.permutations(rotor_name_copy, 3))
        comb_list = [(x, y, z) for x, y, z in comb if x in self.rotors_name[0] and y in self.rotors_name[1] and z in self.rotors_name[2]]
        self.rotor_name_comb = comb_list

        # calculate combination for reflector
        reflectors_copy = self.available_reflectors.copy()
        comb = list(itertools.combinations(reflectors_copy, 1))
        comb_list = [x for x, in comb if x in self.reflector_name]
        self.reflectors_comb = comb_list
        if self.allow_reflector_modifications:
            self.reflector_wiring_comb = [reflector_wiring_comb_gen(get_wiring_by_ReflectorType(reflectorType_from_name(name)), self.pairs_to_swap) for name in comb_list]
        else:
            self.reflector_wiring_comb = [reflector_wiring_comb_gen(get_wiring_by_ReflectorType(reflectorType_from_name(name)), 0) for name in comb_list]

        # calculate plugboard combination
        self.plugboard_connection_comb = plugboard_combinations_gen(self.plugboard_connection, self.available_plugs)

    def crack_code(self,encoded_string,crib_list):
        decoded_string_DB = {}
        settings_DB = {}
        this_string = encoded_string.upper()
        crib_list = list(map(lambda l: l.upper(), crib_list))
        print(f"number of total possible combination  = {len(self.rotor_name_comb)*len(self.rotor_pos_comb)*len(self.rotor_ring_setting_comb)* len(self.reflectors_comb)}")
        for plug_setting in self.plugboard_connection_comb:
            self.em.remove_plugleads()
            self.em.insert_plugleads(plug_setting)
            for reflector in self.reflectors_comb:
                self.em.replace_reflector(reflector)
                for reflector_wiring in reflector_wiring_comb_gen(get_wiring_by_ReflectorType(reflectorType_from_name(reflector)), self.pairs_to_swap):
                    self.em.reflector.swap_wiring(reflector_wiring)
                    for rotors in self.rotor_name_comb:
                        self.em.remove_rotors()
                        self.em.add_rotors(list(rotors))
                        for pos in self.rotor_pos_comb:
                            self.em.set_rotor_initial_pos(list(pos))
                            for setting in self.rotor_ring_setting_comb:
                                self.em.set_rotor_ring_setting(list(setting))
                                self.em.reset_default_rotor_position()
                                decoded_string = self.em.encode(encoded_string)
                                for crib in crib_list:
                                    if crib in decoded_string:
                                        string_score = self.common_words_analysis(decoded_string)
                                        decoded_string_DB[decoded_string] = string_score
                                        settings_DB[decoded_string] = [rotors, pos, setting,plug_setting, reflector, reflector_wiring]
        best_score, out_string = max([(v, k) for k, v in decoded_string_DB.items()])
        settings = settings_DB[out_string]
        return out_string, best_score,settings

    def common_words_analysis(self,phrase):
        score = 0
        for word in self.common_words_DB:
            if word in phrase and len(word) > 2:
                score += len(word)
        return score


def plugboard_combinations_gen(plugboard_connection, all_available_plugs):
    half_terms = [x for x in plugboard_connection if "?" in x and "??" not in x]
    letters = "".join(plugboard_connection)
    num_missing_letter = letters.count("?")
    num_full_pairs = plugboard_connection.count("??")
    num_half_pairs = num_missing_letter - num_full_pairs*2
    letters = sorted(letters)
    known_letter_set = set(letters) - {"?"}
    remaining_plugs = set(all_available_plugs) - known_letter_set
    half_pairs = itertools.combinations(remaining_plugs, num_half_pairs)
    for half_pair in half_pairs:
        updated_remaining_letters = remaining_plugs - set(half_pair)
        full_pairs = full_pair_combination_gen(updated_remaining_letters, num_full_pairs)
        for full_pair in full_pairs:
            plug_board_connection_temp = plugboard_connection.copy()
            for i in range(len(full_pair)):
                idx = plug_board_connection_temp.index("??")
                plug_board_connection_temp[idx] = "".join(list(full_pair[i]))
            for perm_half_pair in itertools.permutations(half_pair, num_half_pairs):
                out_plug_board_connection = plug_board_connection_temp.copy()
                for idx, hlf_term in enumerate(half_terms):
                    idx_term = out_plug_board_connection.index(hlf_term)
                    new_pair = hlf_term.replace("?", perm_half_pair[idx])
                    out_plug_board_connection[idx_term] = new_pair
                yield out_plug_board_connection


def full_pair_combination_gen(remaining_letters,n):
    POSS2 = itertools.combinations(itertools.combinations(remaining_letters, 2), n)
    bBrake = False
    bOut = False
    for pair in POSS2:
        if len(pair) == 1 or len(pair) == 0:
            yield pair
            continue
        for i in range(len(pair)):
            for j in range(len(pair)):
                if i == j:
                    continue
                if any(x == y for x, y in zip(pair[i], pair[j])) and i != j:
                    bBrake = True
                    break
                new_t = tuple(reversed(pair[j]))
                if any(x == y for x, y in zip(pair[i], new_t)) and i != j:
                    bBrake = True
                    break
                bOut = True
                bBrake = True
            if bBrake:
                bBrake = False
                break
        if bOut:
            bOut = False
            yield pair


def reflector_wiring_comb_gen(std_wiring, n):
    yield std_wiring  # On the first call return the standard wiring
    all_right_contacts = [x for (_, x) in std_wiring]
    all_left_contacts = [y for (y, _) in std_wiring]
    all_right_contacts_unique = []
    all_left_contacts_unique = []
    for idx, rc in enumerate(all_right_contacts):
        lc = all_left_contacts[idx]
        if lc in all_right_contacts_unique:
            continue
        all_right_contacts_unique.append(rc)
        all_left_contacts_unique.append(lc)
    right_contact_to_swap_comb = itertools.combinations(all_right_contacts_unique, n)
    for right_contact in right_contact_to_swap_comb:
        wire_pairs_comb = full_pair_combination_gen(right_contact, 2) #Only swap wires in pairs
        for wire_pairs in wire_pairs_comb:
            new_wiring = std_wiring.copy()
            new_left_contact = []
            for right_contact_pair in wire_pairs:
                this_wire_pair_left_contact = [y for (y, x) in std_wiring if x in right_contact_pair]
                new_left_contact.append((this_wire_pair_left_contact[1], this_wire_pair_left_contact[0]))
            new_conn = list(zip(join_iterable_2_tuple(new_left_contact), join_iterable_2_tuple(wire_pairs)))
            for conn in new_conn:
                left_cont, right_cont = conn
                idx = Rotor.char2num(right_cont)
                assert(right_cont != new_wiring[idx][0])
                new_wiring[idx] = conn
                idx_complemetary = Rotor.char2num(left_cont)
                new_wiring[idx_complemetary] = conn[1], conn[0]

            yield new_wiring   # from the second call onwards return the modified wiring


def join_iterable_2_tuple(iterable):
    out = ()
    for x, y in iterable:
        out = out + (x,) + (y,)
    return out



if __name__ == '__main__':

    CC1 = CodeCraking()
    CC1.rotors_name = [["Beta"], ["Gamma"], ["V"]]
    CC1.rotors_positions = [["M"], ["J"], ["M"]]
    CC1.rotors_ring_setting = [[4], [2], [14]]
    CC1.plugboard_connection = ["KI", "XN", "FL"]
    CC1.calculate_total_combination()
    crakedstring, score, settings = CC1.crack_code("DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ", ["SECRETS"])
    print(f"The decoded messages is {crakedstring} with a score of {score}")
    print(f"The Enigma Machine settings are:"
          f" Rotors: {settings[0]}\n"
          f" Rotor positions: {settings[1]}\n"
          f" Rotor settings: {settings[2]}\n"
          f" Plugboard connections: {settings[3]}\n"
          f" Reflector: {settings[4]}\n"
          f" Reflector Wiring: {settings[5]}")
    print("\n")

    CC2 = CodeCraking()
    CC2.rotors_name = [["Beta"], ["I"], ["III"]]
    CC2.rotors_ring_setting = [[23], [2], [10]]
    CC2.reflector_name = ["B"]
    CC2.plugboard_connection = ["VH", "PT", "ZG", "BJ", "EY", "FS"]
    CC2.calculate_total_combination()
    crakedstring, score, settings = CC2.crack_code("CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH", ["UNIVERSITY"])
    print(f"The decoded messages is {crakedstring} with a score of {score}")
    print(f"The Enigma Machine settings are:"
          f" Rotors: {settings[0]}\n"
          f" Rotor positions: {settings[1]}\n"
          f" Rotor settings: {settings[2]}\n"
          f" Plugboard connections: {settings[3]}\n"
          f" Reflector: {settings[4]}\n"
          f" Reflector Wiring: {settings[5]}")
    print("\n")


    CC3 = CodeCraking()
    CC3.rotors_name = [["Beta", "Gamma", "IV", "II"], ["Beta", "Gamma", "IV", "II"], ["Beta", "Gamma", "IV", "II"]]
    CC3.rotors_ring_setting = [[x for x in range(1, 27) if x % 2 == 0 and (x < 10 or x > 19)] for _ in range(3)]
    CC3.rotors_positions = [["E"], ["M"], ["Y"]]
    CC3.plugboard_connection = ["FH", "TS", "BE", "UQ", "KD", "AL"]
    CC3.calculate_total_combination()
    crakedstring, score, settings = CC3.crack_code("ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY", ["THOUSANDS"])
    print(f"the decoded messages is {crakedstring} with a score of {score}")
    print(f"The Enigma Machine settings are:"
          f" Rotors: {settings[0]}\n"
          f" Rotor positions: {settings[1]}\n"
          f" Rotor settings: {settings[2]}\n"
          f" Plugboard connections: {settings[3]}\n"
          f" Reflector: {settings[4]}\n"
          f" Reflector Wiring: {settings[5]}")
    print("\n")


    CC4 = CodeCraking()
    CC4.rotors_name = [["V"], ["III"], ["IV"]]
    CC4.rotors_ring_setting = [[24], [12], [10]]
    CC4.rotors_positions = [["S"], ["W"], ["U"]]
    CC4.plugboard_connection = ["WP", "RJ", "A?", "VF", "I?", "HN", "CG", "BS"]
    CC4.reflector_name = ["A"]
    CC4.calculate_total_combination()
    crakedstring, score, settings = CC4.crack_code("SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW", ["TUTOR"])
    print(f"the decoded messages is {crakedstring} with a score of {score}")
    print(f"The Enigma Machine settings are:"
          f" Rotors: {settings[0]}\n"
          f" Rotor positions: {settings[1]}\n"
          f" Rotor settings: {settings[2]}\n"
          f" Plugboard connections: {settings[3]}\n"
          f" Reflector: {settings[4]}\n"
          f" Reflector Wiring: {settings[5]}")
    print("\n")


    CC5 = CodeCraking()
    CC5.rotors_name = [["V"], ["II"], ["IV"]]
    CC5.rotors_ring_setting = [[6], [18], [7]]
    CC5.rotors_positions = [["A"], ["J"], ["L"]]
    CC5.plugboard_connection = ["UG", "IE", "PO", "NX", "WT"]
    CC5.allow_reflector_modifications = False
    CC5.pairs_to_swap = 4
    CC5.calculate_total_combination()
    crakedstring, score, settings = CC5.crack_code("HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX", ["FACEBOOK", "TWITTER", "INSTAGRAM", "LINKEDIN", "YOUTUBE"])
    print(f"the decoded messages is {crakedstring} with a score of {score}")
    print(f"The Enigma Machine settings are:"
          f" Rotors: {settings[0]}\n"
          f" Rotor positions: {settings[1]}\n"
          f" Rotor settings: {settings[2]}\n"
          f" Plugboard connections: {settings[3]}\n"
          f" Reflector: {settings[4]}\n"
          f" Reflector Wiring: {settings[5]}")
    print("\n")

    #gen = reflector_wiring_comb_gen([('Y', 'A'), ('R', 'B'), ('U', 'C'), ('H', 'D'), ('Q', 'E'), ('S', 'F'), ('L', 'G'), ('D', 'H'), ('P', 'I'), ('X', 'J'), ('N', 'K'), ('G', 'L'), ('O', 'M'), ('K', 'N'), ('M', 'O'), ('I', 'P'), ('E', 'Q'), ('B', 'R'), ('F', 'S'), ('Z', 'T'), ('C', 'U'), ('W', 'V'), ('V', 'W'), ('J', 'X'), ('A', 'Y'), ('T', 'Z')], 4)

    #for i in gen:
    #   print(i)



class Plugboard:

    def __init__(self):
        self.plugleads = []             # List of plugleads
        self.num_plugleads = 0          # Number of added plugleads
        self.max_num_plugleads = 10     # Maximum number of plug leads allowed (Enigma machine came by default with 10 leads)
        self.__contact = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                          "T", "U", "V", "W", "X", "Y", "Z"}

    def add(self, a_pluglead):
        # Maximum number of plug leads available is 10
        if self.num_plugleads >= self.max_num_plugleads:
            raise ValueError(f"Maximum number of plug leads connections ({self.max_num_plugleads}) has been exceeded")
        # Two or more identical plug leads cannot exist
        if a_pluglead in self.plugleads:
            raise ValueError(" 1 or more pluglead contacts are already in use. Check your inputs")
        self.plugleads.append(a_pluglead)
        self.num_plugleads += 1

    # Remove a specific plug lead by name
    def remove(self, a_pluglead):
        if a_pluglead in self.plugleads:
            self.plugleads.remove(a_pluglead)

    # Remove all plug leads from the plug board
    def clear(self):
        self.plugleads = []
        self.num_plugleads = 0

    # Iterate over all plugleads in the plugboard to encode the input char
    def encode(self, char_in):
        # check that the input is a string
        if not isinstance(char_in, str):
            raise ValueError(f"{char_in} is not a valid input. Input be an UPPERCASE character between A and Z included")
        # check that the input character is valid
        if char_in not in self.__contact:
            raise ValueError(f"{char_in} is not a valid input. Input must be an UPPERCASE character between A to Z included")
        char_out = char_in
        for plug_lead in self.plugleads:
            char_out = plug_lead.encode(char_in)
            # if the input character has been encoded then return the mapped character, if not keep looking
            if char_out != char_in:
                return char_out
        # return an exact copy of the input character if there is no lead that maps it to another char
        return char_out


if __name__ == "__main__":
    from pluglead import *

    # Test correct encoding
    plugboard = Plugboard()
    plugboard.add(PlugLead("SZ"))
    plugboard.add(PlugLead("GT"))
    plugboard.add(PlugLead("DV"))
    plugboard.add(PlugLead("KU"))
    plugboard.add(PlugLead("if"))

    assert (plugboard.encode("K") == "U")
    assert (plugboard.encode("A") == "A")
    assert(plugboard.encode("I") == "F")

    # Test wrong inputs
    pb = Plugboard()
    pb.add(PlugLead("AF"))
    try:
        pb.add(PlugLead("AF"))
        print("Test1 failed")
    except ValueError:
        print("Test1 passed")

    try:
        pb.add(PlugLead("AK"))
        print("Test2 failed")
    except ValueError:
        print("Test2 passed")

    testSet = ["i", "?", 12, [], ""]
    for i, test in enumerate(testSet):
        try:
            pb.encode(test)
            print(f"Test{i} encode failed")
        except ValueError:
            print(f"Test{i} encode passed")









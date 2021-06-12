class Plugboard:

    def __init__(self):
        self.plugleads = []             # list of plug leads
        self.num_plugleads = 0          # number of added plug leads
        self.max_num_plugleads = 10     # maximum number of plug leads allowed ( Enigma machine cam  by default with 10 leads)
        self.__contact = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                          "T", "U", "V", "W", "X", "Y", "Z"}

    def add(self, a_pluglead):
        # Check that the plug lead which is being added had the right number of elements

        # Maximum number of plug leads available is 10
        if self.num_plugleads > self.max_num_plugleads:
            ValueError("Maximum number of pluglead connections has been exceeded")
        # two or more identical plug leads cannot exist
        if a_pluglead in self.plugleads:
            ValueError("Pluglead connections already in use")
        # two or more plugleads cannot have the same keys
        # TODO
        self.plugleads.append(a_pluglead)
        self.num_plugleads += 1

    # remove a specific plug lead by name
    def remove(self, a_pluglead):
        if a_pluglead in self.plugleads:
            self.plugleads.remove(a_pluglead)

    # remove all plug leads from the plug board
    def clear(self):
        self.plugleads = []
        self.num_plugleads = 0

    #
    def encode(self, char_in):
        # check that the input character is a valid one
        if char_in not in self.__contact:
            raise ValueError(f"{char_in} is not a valid contact. Remember to use capital case letters")
        char_out = char_in
        for plug_lead in self.plugleads:
            char_out = plug_lead.encode(char_in)
            # if the input character has been encoded then return the mapped character, if not keep looking
            if char_out != char_in:
                return char_out
        # return an exact copy of the input character if there is no lead that maps it to another char
        return char_out


if __name__ == "__main__":
    import pluglead
    PB = Plugboard()
    pl1 = pluglead.PlugLead("AK")
    pl2 = pluglead.PlugLead("KG")
    pl3 = pluglead.PlugLead("A?")

    PB.add(pl1)
    PB.add(pl1)
    PB.add(pl3)


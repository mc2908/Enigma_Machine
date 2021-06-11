class Plugboard:

    def __init__(self):
        self.plugleads = []
        self.num_plugleads = 0
        self.max_num_plugleads = 10
        self.__contact = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                          "T", "U", "V", "W", "X", "Y", "Z"}

    def add(self, a_pluglead):
        # Maximum number of plugleads available is 10
        if self.num_plugleads > self.max_num_plugleads:
            ValueError("Maximum number of pluglead connections has been exceeded")
        # two or more identical pug leads cannot exist
        # two or more plugleads cannot have the same keys
        if a_pluglead in self.plugleads:
            ValueError("Pluglead connections already in use")

        self.plugleads.append(a_pluglead)
        self.num_plugleads += 1

    def remove(self, a_pluglead):
        if a_pluglead in self.plugleads:
            self.plugleads.remove(a_pluglead)

    def clear(self):
        self.plugleads = []
        self.num_plugleads = 0

    def encode(self, char_in):
        if char_in not in self.__contact:
            raise ValueError()
        char_out = char_in
        for plug_lead in self.plugleads:
            char_out = plug_lead.encode(char_in)
            if char_out != char_in:
                return char_out
        return char_out


if __name__ == "__main__":
    import pluglead
    PB = Plugboard()
    pl1 = pluglead.PlugLead("AK")
    pl2 = pluglead.PlugLead("KG")

    PB.add(pl1)
    PB.add(pl1)


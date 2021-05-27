class Plugboard:

    def __init__(self):
        self.plugleads = []
        self.num_plugleads = 0
        self.max_num_plugleads = 10;

    def add(self, a_pluglead):
        # Maximum number of plugleads available is 10
        if self.num_plugleads > self.max_num_plugleads:
            return
        # two or more identical pug leads cannot be exist
        if a_pluglead in self.plugleads:
            return
        # two or more plugleads cannot have the same keys
        #TO IMPLEMENT
        self.plugleads.append(a_pluglead)
        self.num_plugleads += 1

    def remove(self, a_pluglead):
        if a_pluglead in self.plugleads:
            self.plugleads.remove(a_pluglead)

    def clear(self):
        self.plugleads = []
        self.num_plugleads = 0

    def encode(self, character_in):
        character_out = character_in
        for plgld in self.plugleads:
            character_out = plgld.encode(character_in)
            if character_out != character_in:
                return character_out
        return character_out

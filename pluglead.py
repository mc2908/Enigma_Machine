class PlugLead:

    contacts = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                          "T", "U", "V", "W", "X", "Y", "Z"}

    def __init__(self, mapping):
        # the input mapping must be a string
        if type(mapping) != str:
            raise TypeError("Plug lead must be defined by string")
        # and must have length 2
        if len(mapping) != 2:
            raise ValueError("Each plug lead must be specified by two capital case character from A to Z")
        # Make sure that each element is a valid plug board contact
        if mapping[0] not in self.contacts or mapping[1] not in self.contacts:
            raise ValueError("Specified Plug Lead contacts do not exist")
        from_char = mapping[0]
        to_char = mapping[1]
        # Create a dictionary with back and forth mapping
        self.letter_encode = {from_char: to_char, to_char: from_char}

    def encode(self, character):
        out_character = character
        # if the plug lead connects the input char then map it to the other end of the lead.
        if character in self.letter_encode:
            out_character = self.letter_encode[character]
        return out_character

    def __eq__(self, other):
        return any(x == y for x, y in zip(self.letter_encode.keys(), other.letter_encode.keys())) or\
               any(x == y for x, y in zip(self.letter_encode.keys(), other.letter_encode.values()))
if __name__ == "__main__":
    pass

# You can use this section to write tests and demonstrations of your enigma code.
#   pluglead1 = PlugLead("AS")
#   print(pluglead1.encode("T"))

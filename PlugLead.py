class PlugLead:
    def __init__(self, mapping):
        # implement here some input checking
        mapping = mapping.upper()
        from_char = mapping[0]
        to_char = mapping[1]
        # Create a dictionary with back and forth
        self.letter_encode = {from_char: to_char, to_char: from_char}

    def encode(self, character):
        out_character = character
        if character in self.letter_encode:
            out_character = self.letter_encode[character]
        return out_character


if __name__ == "__main__":
    pass
# You can use this section to write tests and demonstrations of your enigma code.
#   pluglead1 = PlugLead("AS")
#   print(pluglead1.encode("T"))

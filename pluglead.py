class PlugLead:
    # Available contacts: shared between all instances
    contacts = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                          "T", "U", "V", "W", "X", "Y", "Z"}

    def __init__(self, mapping):
        # The input mapping must be a string
        if not isinstance(mapping, str):
            raise TypeError("Plug lead input must be of string type")
        mapping = mapping.upper()
        # And must have length 2
        if len(mapping) != 2:
            raise ValueError("Each plug lead must be specified by two capital case character from A to Z")
        # Make sure that each element is a valid plug board contact
        if mapping[0] not in self.contacts or mapping[1] not in self.contacts:
            raise ValueError(f"Specified Plug Lead contacts ({mapping[0] + mapping[1] }) do not exist")
        from_char = mapping[0]
        to_char = mapping[1]
        # Create a dictionary with back and forth mapping
        self.letter_encode = {from_char: to_char, to_char: from_char}

    def encode(self, char_in):
        # check input
        if not isinstance(char_in,str):
            raise ValueError("Plug lead input must be of string type")
        if char_in not in self.contacts:
            raise ValueError( f"{char_in} is not a valid input. Input must be an UPPERCASE character from A to Z")
        char_out = char_in
        # If the plug lead connects the input char then map it to the other end of the lead.
        if char_in in self.letter_encode:
            char_out = self.letter_encode[char_in]
        return char_out

    def __eq__(self, other):
        return any(x == y for x, y in zip(self.letter_encode.keys(), other.letter_encode.keys())) or\
               any(x == y for x, y in zip(self.letter_encode.keys(), other.letter_encode.values()))


if __name__ == "__main__":

    # Test correct encoding
    lead = PlugLead("AG")
    assert (lead.encode("A") == "G")
    assert (lead.encode("D") == "D")

    lead = PlugLead("DA")
    assert (lead.encode("A") == "D")
    assert (lead.encode("D") == "A")


    lead = PlugLead("aF")
    assert (lead.encode("a") == "F")

    # Test wrong inputs
    try:
        lead = PlugLead(2343)
        print("Test1 failed")
    except TypeError:
        print("Test1 passed")

    try:
        lead = PlugLead("2343")
        print("Test2 failed")
    except ValueError:
        print("Test2 passed")

    try:
        lead = PlugLead("&*")
        print("Test3 failed")
    except ValueError:
        print("Test3 passed")

    lead = PlugLead("AF")
    testSet = ["i", "?", 12, [], ""]
    for i, test in enumerate(testSet):
        try:
            lead.encode(test)
            print(f"Test{i} encode failed")
        except ValueError:
            print(f"Test{i} encode passed")



# You can use this section to write tests and demonstrations of your enigma code.
#   pluglead1 = PlugLead("AS")
#   print(pluglead1.encode("T"))

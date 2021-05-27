



if __name__ == '__main__':
    from PlugLead import PlugLead
    from Plugboard import Plugboard

    plugboard = Plugboard()
    plugboard.add(PlugLead("SZ"))
    plugboard.add(PlugLead("AF"))
    plugboard.add(PlugLead("CR"))

    outChar = plugboard.encode("T")
    print(outChar)

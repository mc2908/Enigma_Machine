from enigma import *

print("Test 1")


message = "sasdfasdfas"

em0 = EnigmaMachine()
em0.add_rotors(["I", "II", "III", "IV"])
em0.set_rotors_initial_pos(["A", "A", "Z"])
em0.set_rotors_ring_setting([1, 1, 1])
em0.add_reflector("C")
em0.insert_plugleads(["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"])
encoded_string = em0.encode(message)


em0.reset_default_rotor_position()
decoded_string = em0.encode(encoded_string)
print(decoded_string)
#assert(decoded_string == message)



r1 = rotor_from_name("I")

try:
    ex1 = r1.encode_left_to_right("A")
    print(ex1)
except ValueError:
    print("Bad")

try:
    ex2 = r1.encode_right_to_left(" ")
    print(ex2)
except ValueError:
    print("Ok")




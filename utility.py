import warnings

def check_input_message_formatting(message: str):
    if type(message) is not str:
        raise TypeError("Encode method only accepts strings as input")
    message_temp = message.upper()
    message_temp = [x for x in message_temp if 65 <= ord(x) <= 90]
    message_formatted = "".join(message_temp)
    if len(message_formatted) != len(message):
        warnings.warn("Input string special characters and/or white spaces have been removed, lowercase characters has been formatted to upper case")
        return message_formatted
    if message_formatted != message:
        warnings.warn("Input string lowercase characters has been formatted to upper case has been formatted to upper case")
    return message_formatted


def check_input_char_formatting(char: str):
    char = char.upper()
    if type(char) is not str:
        raise TypeError("Encode method only accepts strings as input")
    elif len(char) > 1:
        raise ValueError()
    elif len(char) < 1:
        raise ValueError()
    elif ord(char) < 65 or ord(char) > 90:
        raise ValueError()
    return char

import warnings


def check_input_message_formatting(message: str, message_type):
    if type(message) is not str:
        raise TypeError(message_type +" must be a string")
    # make the input string upper case
    message_temp = message.upper()
    # remove all special characters
    message_temp = [x for x in message_temp if 65 <= ord(x) <= 90]
    message_formatted = "".join(message_temp)
    # check if characters have been removed from the input string
    if len(message_formatted) != len(message):
        warnings.warn(message_type + " info: Special characters and/or white spaces have been removed, lowercase characters has been formatted to upper case")
        return message_formatted
    # check if the output sting has been modified respect to the input string
    if message_formatted != message:
        warnings.warn(message_type + "info : Lowercase characters has been formatted to upper case")
    return message_formatted


def doubleFactorial(n):
    if n <= 1:
        return 1
    return n * doubleFactorial(n-2)



if __name__ == '__main__':
    val = doubleFactorial(6)
    print(val)

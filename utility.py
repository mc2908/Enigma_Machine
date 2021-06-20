import warnings

# helper method to check the formatting of a input message
def check_input_message_formatting(message: str, message_type):
    if type(message) is not str:
        raise TypeError(message_type + " must be a string")
    # make the input string upper case
    message_temp = message.upper()
    # remove all special characters
    message_temp = [char for char in message_temp if 65 <= ord(char) <= 90]
    message_formatted = "".join(message_temp)
    # check if characters have been removed from the input string
    if len(message_formatted) != len(message):
        warnings.warn(message_type + " info: Special characters and/or white spaces have been removed, lowercase characters has been formatted to upper case")
        return message_formatted
    # check if the output sting has been modified respect to the input string
    if message_formatted != message:
        warnings.warn(message_type + "info : Lowercase characters has been formatted to upper case")
    return message_formatted


# Helper method to calculate double factorial on a number n, i.e. n * (n-2) * (n-4) * (n-6) * ....
def doubleFactorial(n):
    if n <= 1:
        return 1
    return n * doubleFactorial(n-2)

# Helper method to calculate the moving average on on input list of numbers given a window width ww
def moving_average(in_list, ww):
    out_list = []
    for idx, el in enumerate(in_list):
        if idx < ww:
            s = sum(in_list[0: idx+1])
            avg = s / (idx+1)
        else:
            s = sum(in_list[idx+1-ww: idx+1])
            avg = s / ww
        out_list.append(avg)
    return out_list


if __name__ == '__main__':
    pass

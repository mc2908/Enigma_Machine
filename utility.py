import warnings
import matplotlib.pyplot as plt

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


def moving_avarage(list, window):
    out_list = []
    for idx, el in enumerate(list):
        if idx < window:
            #avg = list[idx]
            s = sum(list[0: idx+1])
            avg = s / (idx+1)
        else:
            s = sum(list[idx+1-window: idx+1])
            avg = s / window
        out_list.append(avg)
    return out_list



if __name__ == '__main__':
    val = doubleFactorial(6)
    print(val)


    x = [x for x in range(100)]
    y = moving_avarage(x,7)
    plt.plot(x, y)
    plt.show()




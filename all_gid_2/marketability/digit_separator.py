def digit_separator(digit):
    str_digit = str(int(digit))
    exit_ = str()
    tail = len(str_digit) % 3
    for i in range(len(str_digit)-3, -1, -3):
        exit_ = " " + str_digit[i:i+3] + exit_

    if tail != 0:
        exit_ = str_digit[:tail] + exit_
        return exit_
    else:
        return exit_[1:]

print(digit_separator(1.788))
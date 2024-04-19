# File for parsing and building the year_forms json

def monthly_to_string(number_list):
    out_string = ""

    for i in range(len(number_list)):
        if i == len(number_list) - 1:
            out_string += str(number_list[i])
            break
        out_string += str(number_list[i]) + ","
    
    return out_string


def string_to_monthly(in_string, as_float=False):
    num_list = []

    string_list = in_string.split(",")

    if as_float:
        for i in string_list:
            num_list.append(float(i))
    else:
        for i in string_list:
            num_list.append(int(i))

    return num_list


def condense_string_list(string_list):
    out_string = ""

    for i in range(len(string_list)):
        if i == len(string_list) - 1:
            out_string += string_list[i]
            break
        out_string += string_list[i] + "~"

    return out_string


def build_string_list(in_string):
    string_list = in_string.split("~")

    return string_list


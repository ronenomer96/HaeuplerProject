def hash_fun(seed, input, len_output):
    if len(input) == 0:
        return "0"*len_output
    len_input = len(input)
    output = ""
    parts_of_seed = [seed[start:start+len_input] for start in range(0, len_output*len_input, len_input)]
    for part in parts_of_seed:
        tmp_list_output = list(bin(int(part, 2) & int(input, 2))[2:])
        num = 0
        for i in tmp_list_output:
            num ^= int(i)
        output += str(num)
    return output
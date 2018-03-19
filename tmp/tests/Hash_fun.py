def hash_fun(seed, input):
    if len(input) == 0:
        return ""
    elif len(seed)%len(input) != 0:
        input=input.zfill(len(input)+len(seed)%len(input))
    len_input = len(input)
    len_seed = len(seed)
    output = ""
    parts_of_seed = [seed[start:start+len_input] for start in range(0, len_seed-1, len_input)]
    for part in parts_of_seed:
        tmp_list_output = list(bin(int(part, 2) & int(input, 2))[2:])
        num = 0
        for i in tmp_list_output:
            num ^= int(i)
        output += str(num)
    return output
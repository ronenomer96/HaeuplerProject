import math
#used as a utility file

def RSEncodeConv(str):
    return bytes(int(str[i : i + 8], 2) for i in range(0, len(str), 8))

def RSDecodeConv(bytearr,desiredLength):
    result=""

    for elem in bytearr:
        numAsString=bin(elem)[2:]
        result+=numAsString.zfill(8)
    if (len(result)>desiredLength and len(result)>8):
        result=result[0:desiredLength]
    return result

def flipBit(str):
    if (str=="1"):
        return "0"
    elif (str=="0"):
        return "1"
    return str

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)



def cal_Symbol_error(err):
    sum = 0
    for i in range(1, 9):
        a = nCr(8, i)
        b= err ** i
        c = (1 - err) ** (8 - i)
        sum += a * b * c
    return sum

def calc_r(k, e):
    E = cal_Symbol_error(e)
    numerator = 2 * k * E + 2
    denominator = 1 - 2 * E
    return math.ceil(numerator/denominator)

def calc_m(transcript, logGap):
    length = len(transcript)
    A = 2 ** logGap
    rem = length % A
    m = (length - rem)/A
    return int(m)
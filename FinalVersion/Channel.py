# -*- coding: utf-8 -*-
import random
import math
import fractions


def Channel(input,errorChance):

    counter = 0
    numerator = fractions.Fraction(errorChance).numerator
    denominator = fractions.Fraction(errorChance).denominator

    if (type(input) is list):
        output=[]
        for string in input:
            tmpOutput=list(string)
            for i in range(0, len(tmpOutput)):
                change = random.randint(1, denominator)
                if (change <= numerator):
                    counter +=1
                    if tmpOutput[i] == "1":
                        tmpOutput[i] = "0"
                    else:
                        tmpOutput[i] = "1"
            output.append(''.join(tmpOutput))
        return [output, counter]

    elif((type(input) is str)):
        output=list(input)
        for i in range(0,len(output)):
            change=random.randint(1,denominator)
            if (change<=numerator):
                counter += 1
                if output[i] == "1":
                    output[i] = "0"
                else:
                    output[i] = "1"
        return [''.join(output), counter]


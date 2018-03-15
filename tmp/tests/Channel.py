# -*- coding: utf-8 -*-
import random
def Channel(input,errorChance):
    output=list(input)
    if (errorChance==0):
        return ''.join(output)
    else:    
        for i in range(0,len(output)):
            change=random.randint(0,(1/errorChance)-1)
            if change==0:
                if output[i]=="1":
                    output[i]="0"
                else:
                    output[i]="1"
        return ''.join(output)       
        

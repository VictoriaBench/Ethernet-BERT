

def findErrors(data, expected):
    count = 0
    errors = 0
    for dB,eB in zip(data, expected):
        for i in range(8):
            db = (dB&0b1<<i)>>i
            eb = (eB&0b1<<i)>>i
            if db is not eb:
                errors+=1
            count+=1
    
    return count, errors
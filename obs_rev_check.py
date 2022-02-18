import itertools as it
obv = list()
rev = list()
both = list()
forb = list()
maxindex = 30

def is_rev(h,k,l):
    if (h - k + l) % 3 == 0:
        return True

def is_obv(h,k,l):
    if (-h + k + l) % 3 == 0:
        return True

#Create Lists with groups of reflections, maxindex in preamble
def create_lists():
    global maxindex, obv, rev, both, forb
    for refl in it.product(range(-1*maxindex,maxindex+1),repeat = 3):
        for index in refl:
            if is_obv(*refl) and is_rev(*refl):
                both.append(refl)
            elif is_obv(*refl):
                obv.append(refl)
            elif is_rev(*refl):
                rev.append(refl)
            else:
                forb.append(refl)  

"""el asterisco (*) antes del argumento es para poder unpackear
la tupla antes de pasarla como un argumento"""
      
#Checks in which list is the (h,k,l) reflection            
def what_is(h,k,l):
    global maxindex, obv, rev, both, forb
    refl = (h,k,l)
    for index in refl:
        if abs(index) > maxindex:
            print("Reflection out of range, increase maximum index range in script preamble")
            return
    if refl in  obv:
        print(refl, "is allowed in Obverse setting")
    elif refl in  rev:
        print(refl, "is allowed in Reverse setting")
    elif refl in  both:
        print(refl, "is allowed in both settings")
    elif refl in  forb:
        print(refl, "is forbidden")
    else:
        print("Something is broke with the code")




#Loop for to allow user input
create_lists()
print('input reflection. e.g. -2 1 0')
while True:
    try:
        usr_input = input()
        if usr_input == '0':
            break
        reflejo = tuple(map(int, usr_input.strip().split()))
        if len(reflejo) != 3:
            print("Input not valid")
            continue
        what_is(*reflejo)
    except ValueError:
        print("Invalid input, try again (Value Error)")

        
    

import re
import os

def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)


def origin(formula):
    tabla = []

    split = re.findall('[A-Z][^A-Z]*', formula) # CH3OH -> [C, H3, O,H]
    for i in split:
        b = re.findall('\d+\.\d*|\d+|\D+', i)
        if len(b) == 1:
            b.append('1')
        tabla.append(b)
        #print(b)
    #print(tabla)    # [C, H3, O,H] -> [[C,1],[H,3],[O,1],[H,1]]

    output = str()
    for i in tabla:
        if i[1] != '1':
            output += i[0]+"\\-("+i[1]+")"
        else:
            output += i[0]     
    return output


#print ("Ejemplo: MasaCompuesto = masa('Bi13Pt3I7')")
print ("Ejemplo: Bi13Pt3I7")
print ("Input '0' para cerrar el programa")

while True:
    comp = input('Formula del compuesto: ')
    if comp == '0':
        exit()
    a = origin(comp)
    print(a)
    addToClipBoard(a)
    print('Copied to the clipboard\n')

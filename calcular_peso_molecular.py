#Calcular pesos moleculares
from tabla_periodica import elementos
import re

def masa(formula):
    tabla = []

    split = re.findall('[A-Z][^A-Z]*', formula) # CH3OH -> [C, H3, O,H]

    for i in split:
        b = re.findall('\d+|\D+', i)
        if len(b) == 1:
            b.append('1')
        tabla.append(b)
        #print(b)
    #print(tabla)    # [C, H3, O,H] -> [[C,1],[H,3],[O,1],[H,1]]


    masa = 0
    for i in tabla:
    # i[0] == Nombre del Elemento; i[1] == Coeficiente estequimetrico.
        peso_molecular = elementos[i[0]] #buscar el peso molecular en el diccionario
        
        print(i[0],"=", peso_molecular)
        masa += peso_molecular*float(i[1])

    print(formula,"=", masa)    
    return masa

#print ("Ejemplo: MasaCompuesto = masa('Bi13Pt3I7')")
print ("Ejemplo: Bi13Pt3I7")
print ("Input '0' para cerrar el programa")

while True:
    comp = input('Formula del compuesto: ')
    if comp == '0':
        try:
            exit()
        except NameError:
            break
    else:
        masa(comp)
        print('\n')


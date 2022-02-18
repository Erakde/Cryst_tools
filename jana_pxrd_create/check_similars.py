# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:55:39 2020

@author: ec
"""

def collect_cif_info(ciffile):
    with open(ciffile) as f:
        for line in f:
            if '_cell_length_a' in line:
                a = line.strip().split()[1]
            if '_cell_length_b' in line:
                b = line.strip().split()[1]            
            if '_cell_length_c' in line:
                c = line.strip().split()[1]                
            if '_symmetry_Int_Tables_number' in line:
                space_group = line.strip().split()[1]
            if '_database_code_ICSD' in line:
                ID = line.strip().split()[1]
            if '_chemical_formula_structural' in line:
                comp_data = line.strip().split() #composition_data
                #print(data)
                formula = ''
                for i in comp_data[1:]:
                    formula += i.strip("'")
        new_data = [ID, formula, space_group, a, b, c]
        return new_data
    
    
def check_database(database, new_data):
    flag = False
    with open(database, 'a+') as f:
        f.seek(0.0)
        for line in f:
            db_data = line.strip().split()
            if db_data[0].startswith('Warning'):
                del db_data[0]
                del db_data[0]
                
            for i,j in enumerate(db_data[-3:]):
                if j.endswith(')'):
                    #print(db_data[i+3])
                    db_data[i+3] = db_data[i+3].split('(')[0]
                    #print(db_data[i+3])
            print(db_data)
            if (float(new_data[3].split('(')[0])*0.9 < float(db_data[3]) < float(new_data[3].split('(')[0])*1.1 and
                float(new_data[4].split('(')[0])*0.9 < float(db_data[4]) < float(new_data[4].split('(')[0])*1.1 and
                float(new_data[5].split('(')[0])*0.9 < float(db_data[5]) < float(new_data[5].split('(')[0])*1.1):  #Si el valor de a b c de la database esta entre el nuevo valor mas menos 10%
                    f.write('Warning: '+ db_data[0])
                    flag = True
        if len(new_data[1]) <= 3:
            new_data[1] += '\t'
        if len(new_data[1]) <= 7:
            new_data[1] += '\t'
            
        if len(new_data[3]) <= 3:
            new_data[3] += '\t'
        if len(new_data[3]) <= 7:
            new_data[3] += '\t'
            
        if len(new_data[4]) <= 3:
            new_data[4] += '\t'
        if len(new_data[4]) <= 7:
            new_data[4] += '\t'
        
        if len(new_data[5]) <= 3:
            new_data[5] += '\t'
        if len(new_data[5]) <= 7:
            new_data[5] += '\t'
        
        if flag:          
            f.write('\t'+'\t\t'.join(new_data)+'\n')
            flag = False
        else:
            f.write('\t\t\t\t'+'\t\t'.join(new_data)+'\n')
        


        
import os, glob      
PATH = 'D:/Python/scripts/jana_pxrd_create/check_iguales'  #define working directory
os.chdir(PATH)
PATH_BAKCIF = PATH+'bak_cifs/'
database = 'D:/Python/scripts/jana_pxrd_create/check_iguales/database.txt'
count = 0 #variable global Para saltarse algunos pasos en pxrd_generate. Siempre tiene que estar antes de llamar a esta funcion
for file in glob.glob("*.cif"): #for all cif files in working directory
    collected_data = collect_cif_info(file)
    check_database(database, collected_data)
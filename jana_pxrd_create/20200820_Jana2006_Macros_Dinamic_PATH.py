# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 12:36:59 2020

@author: ec
Generate csv files containing pxrd simulated data from cif file.

PATH variable should be set to the working directory
Requires Jana2006 open, folder in PATH called csv (/PATH/csv/)
requires ahk: https://www.autohotkey.com/
package name: ahk.
for installation:
    pip install ahk==0.9.0
written in Python3.8
Commands: https://pypi.org/project/ahk/
requires folders named 'bak_cifs' and 'csv'
"""
#ac.send_input('{Backspace}')

from ahk import ActionChain, AHK
from pathlib import Path
import re, shutil


def write_csv(filename,outputname, subheaders = list()): #subheaders is a list of lists containing two values per item, spaced by a comma
    with open(filename) as f:
        global subdir
        filepath = subdir.joinpath('csv', outputname) #define path for .csv file: ./csv/outputname.csv
        print(filepath)
        g = open(filepath, 'w') #create .csv with outputname as name
        flag = False
        #write subheaders in preamble
        for item in subheaders:
            g.write(item[0]+','+item[1]+'\n')
        for line in f:
            if line.startswith('    5.0000'):
                flag = True
            if flag:
                content = line.strip().split()
                g.write(content[0][:-2]+','+content[1]+'\n')
        g.close()                   

#filepath = path of the parent of file as str. filename = filename withou extension as str, pxrd_name = name given to calc. pxrd files as str.
def pxrd_generate(parent_path, filename, pxrd_name): #uses AHK for manipulating Jana2006
    win = ahk.find_window(title=b'Jana2006') #Janna2006 must be open
    win.activate() #activating Janna2006windows
    win.maximize() #maximizing it just to make sure is active
    global count     
#in Jana, open and make new project
    ac.click(27,34) 
    ac.key_press('S')
    ac.key_press('N')

        


#create new file   
    ac.sleep(0.5)
    
    if count == 0: #if a new system is open, change folder
        ac.double_click(800, 745) #click on Path
        ac.type(str(parent_path)) # Paste Path
        
    #ac.click(1100,726) #click down arrow
    ac.double_click(1000, 745) #double click in name field
    ac.type(filename) #write filename as name
    ac.click(1000,810) #click ok
    ac.sleep(1)
    ac.click(833,533) #click  From CIF
    ac.click(1000,810) #click ok
    ac.sleep(0.5)    
    #ac.click(1100,726) #click arrow down button
    #ac.double_click(1000, 745) #double click in name field
    #ac.type(filename+'.cif') #write filename as name
    ac.click(1000,810) #click ok
    ac.sleep(0.8)
    
    
    #do you want to import data from file?
    ac.click(993, 611) #no

#calculate powder diffractogram     
    ac.click(308,31) #click on Tools
    ac.key_press('S') #specials tools
    ac.key_press('p') #powder structure simulation
    
    #INPUT NAME PXRD FILE
    ac.double_click(975,579)
    ac.type(pxrd_name)
    ac.click(990,617) #ok
    
    #INFORMATION A new simulated powder..
    ac.sleep(1.2)
    ac.click(962, 639) #ok
    ac.sleep(0.3)
    

    #Powder Options:
    ac.click(798,379) # Profile
    ac.double_click(943,459) # GU   
    ac.type('10')
    
    ac.double_click(940,487) #GV
    ac.type('-50')
    
    ac.double_click(940,507) #GW
    ac.type('5')
    
    ac.double_click(940,533) #GP
    ac.type('30')
    
    ac.click(992,823) #ok
    ac.click(931,598) #Overwrite? Yes
    ac.sleep(0.8)
    if count == 0:   
        ac.double_click(940,509) #from 5
        ac.type('5')
        
        ac.double_click(940,536) #to 90
        ac.type('90.02')
        
        ac.double_click(940,560) #step 0.02
        ac.type('0.02')
        count = 1
    ac.click(990, 686) #ok
    ac.sleep(1.5)
    
    ac.click(990, 596) #start profile viewer? no
    
    ac.click(27,34) #click File
    ac.key_press('S') #click Structure
    ac.key_press('e') #click close
    ac.sleep(1)
    ac.perform() #execute ac    

def origin(formula): #returns formula in origin legend format
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

def isnumber(n): #returns True or False if n is or not a number
    try:
        int(n)
        return True
    except ValueError:
        return False

def extract_data(ciffile): #returns formula, space_group_number, ID, database (ej: Bi16I4 12 246145 ICSD)
    flag1 = False
    flag2 = False
    flag3 = False
    with open(ciffile) as f:
        for line in f:
            #find the correct line to extract the formula, 
            #_chemi... for ICSD; _sm_phase... for Springer Materials; '_chemical_formula_sum' for cif files from shelx
            if line.startswith('_chemical_formula_structural') or line.startswith('_sm_phase_labels') or line.startswith('_chemical_formula_sum') and not flag1:
                comp_data = line.strip().split() #composition_data
                #print(data)
                formula = ''
                for i in comp_data[1:]:
                    formula += i.strip("'")
                    flag1 = True
                #print(formula)
            #_symm... for SM and ICSD; _space_gr... for shelx cif files
            elif line.startswith('_symmetry_Int_Tables_number') or line.startswith('_space_group_IT_number') and not flag2:
                space_group_num = line.strip().split()[1] #space group data
                if isnumber(space_group_num): #in case there ?
                    flag2 = True
                    #print(space_group_num)
            elif line.startswith('Unique LPF ID Number') and not flag3:
                database = 'SM'
                ID = line.strip().split()[4]
                #print(ID)
                flag3 = True
            elif line.startswith('_database_code_ICSD') and not flag3:
                database = 'ICSD'
                ID = line.strip().split()[1]
                #print(ID)
                flag3 = True
                
            if flag1 and flag2 and flag3:
                return formula, space_group_num, ID, database
        if not flag1:
            print('Formula not found')
        if not flag2:
            print('Space group number not found')
        if not flag3:
            database = ''
            ID = ''
            return formula, space_group_num, ID, database
            
def create_standardized_name(formula, space_group, ID): #returns standarized filename without extension e.g. Bi16I4_(12)_246145
    if ID == '':
        return (formula+'_('+ space_group+')_(calc.)')
    return formula+'_('+ space_group +')_'+ID

def create_originname(formula, ID, database): #returns longname for origin e.g. Bi\-(16)I\-(4) (ICSD: 246145)
    origin_formula = origin(formula)
    if database == '':
        return (origin_formula + ' (calc.)')
    else:
        return (origin_formula + ' ('+database +': ' + ID + ')')


    
ac = ActionChain(executable_path='D:\\AutoHotkey\\AutoHotkey.exe') #specify where AutoHotkey is installed
ahk = AHK(executable_path='D:\\AutoHotkey\\AutoHotkey.exe') #same as above



PATH = 'D:/Python/scripts/jana_pxrd_create/docs/_input'  #define working directory


p = Path(PATH)
for subdir in p.iterdir(): #ceeate csv and bak_cifs folders
    if subdir.is_dir():
        print(subdir)
        subdir.joinpath('csv').mkdir(exist_ok=True)
        subdir.joinpath('bak_cifs').mkdir(exist_ok=True)

           
    PATH_BAKCIF = subdir.joinpath('bak_cifs') # path a bak_cifs directory
    count = 0 #variable global Para saltarse algunos pasos en pxrd_generate. Siempre tiene que estar antes de llamar a esta funcion
    
    for file in subdir.glob("*.cif"): #for all cif files in working directory
        formula, sp_number, ID, database = extract_data(file) #get data from corresponding cif file 
        standard_name = create_standardized_name(formula, sp_number, ID)
    
    
    #Jana macros 
        pxrd_generate(str(subdir), file.stem, standard_name)
        
        
    #Delete trash, keep .cif, .m90, .prf and get data from them
        for trashfile in subdir.glob(file.stem+'*'): #scan all files containing file_stem
            #print(trashfile.suffix)
            if not trashfile.suffix == '.cif':
                trashfile.unlink() #remove all files except for cif,
       
        shutil.copyfile(str(file), str(subdir.joinpath('bak_cifs',file.name)))#make a copy with standarized name in bak_cifs folder
        shutil.move(str(file), subdir.joinpath(standard_name.replace('.', '')+'.cif')) #change name of file that stays in PATH folder, dot is replaced because shutil does not accept it      
        
        for trashfile in subdir.glob(standard_name+'*'): #scan all files containing file_stem
            if not trashfile.suffix in ['.cif', '.m90', '.prf']:
                trashfile.unlink() #remove all files except for m90 and prf
            elif trashfile.suffix == '.m90':  #if .m90 file is found, open
                csv_name = standard_name+'.csv' #get csv_name
                origin_name = create_originname(formula, ID, database)
                subheaders = [['Angle',csv_name[:-4]], ['2Tetha',origin_name]] #creates list of lists containing subheaders for csv file.
                write_csv(trashfile, csv_name, subheaders) #write a csv file named csv_name from trashfile, including subheaders
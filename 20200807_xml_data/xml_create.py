#%%
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:53:41 2020

@author: ec
"""
from lxml import etree
from os import getcwd
import re

class newSample(): 
    def __init__(self):
        pass
        
    def preamble(self, ID):
        self.sampleID = ID.upper().replace(' ', '_')
        print('Sample name:',self.sampleID)
        self.aim =input('Aim: ')                                          
        self.date = input('Synthesis date: ')
        self.procedure = input('Synthesis procedure: ')
        
        self.root = etree.Element('sample',ID=self.sampleID )    #XML:create xml root, name'sample' attribute=self.sampleID
        self.xml_aim = etree.SubElement(self.root,'aim')      #XML: create child named 'aim'
        self.xml_synthesis = etree.SubElement(self.root, 'synthesis') #XML: create child, name 'synthesis'
        self.xml_date = etree.SubElement(self.xml_synthesis, 'date')  #XML: create child, name 'date'
        self.xml_procedure = etree.SubElement(self.xml_synthesis, 'procedure')    #XML: create grandchild, name 'procedure'

        self.xml_aim.text = self.aim                   #XML: fills 'aim' with self.aim
        self.xml_date.text = self.date
        self.xml_procedure.text = self.procedure 
        self.wait_for_input()
        
        
    def wait_for_input(self):
        while True: #loop for input
            print('\n[1] = Add experiments')
            print('[2] = Add others')
            print('[0] = Save '+self.sampleID+'.xml and Exit')
            dummy = input('Enter number: ')
            
            #----save&exit-----
            if dummy == '0':    #0 = exit
                break   
            
            #-----analytics-------  
            elif dummy == '1':  #1 = add experiment
                '''NOTE: ADD LINE TO CHECK WHETHER IT EXIST, OTHERWISE IT WILL ALWAYS CREATE A NEW ONE WHEN THE FILE IS MODIFY IN THE FUTURE'''
                self.xml_analytics = etree.SubElement(self.root, 'analytics')
                self.write_data(Type_='Analytics')
            
            #---------others-------
            elif dummy == '2': #same as adding experiment
                self.xml_others = etree.SubElement(self.root, 'others')
                self.write_data(Type_='Others')
                    
            else:
                print("Woops! I don't understand that number. Try again.")
                
        
        etree.indent(self.root, space="\t")      #change identation of output (default: 2 blankspaces; new: tab)
        pretty = etree.tostring(self.root, encoding='unicode',pretty_print=True) #prepare preety output
        print(pretty)   #print output in console
        tree = etree.ElementTree(self.root)  #get tree
        tree.write(self.sampleID+'.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8') #write tree in sample.ID.xml        
        print(self.sampleID+'.xml saved in '+ getcwd())
                                
#%%                
    
    def addexp(self): # add new experiments
        self.exp_name = self.input_check('Experiment_name (e.g. pxrd, scxrd, sem...): ', InputType_='Experiment')     
        self.exp_ID = (self.input_check(self.exp_name.capitalize() + ' ID: ', InputType_= 'Experiment_ID' ))    # Check if input exists using input_check
        self.exp_date = input(self.exp_name.capitalize() + ' date: ')
        self.exp_desc = input(self.exp_name.capitalize() + ' description: ')
          
    
    def addother(self): #method for adding new 'other' fields
        self.ot_name = self.input_check('Field name? (e.g. Collaborations, Papers): ', InputType_='Other')
        self.ot_desc = input(self.ot_name.capitalize() + ' description: ')

    def writeexp(self): #appends experiment as xml
        self.xml_exp = etree.SubElement(self.xml_analytics, self.exp_name, ID=self.exp_ID)
        etree.SubElement(self.xml_exp, 'date').text = self.exp_date
        etree.SubElement(self.xml_exp, 'description').text = self.exp_desc
    
    def writeother(self):
        etree.SubElement(self.xml_others, self.ot_name).text = self.ot_desc
    
        
    def input_check(self, given_text, InputType_= None): #format input and analyse whether it is a command or text. 
        while True:
            u_input = input(given_text)         
            if InputType_ in ('Experiment', 'Other'):
                if u_input == str():
                    print('This field cannot be left empty. See examples as references.')     
                    continue
                elif not re.match("^[A-Za-z_]*$", u_input):
                    print('Only letters and underscores are accepted as',InputType_.lower(),' names. For further information check conventions.')
                    continue
                else:
                    return u_input.lower()
                
            if InputType_ == 'Experiment_ID':
               attrib_list = []
               for existent_exp in self.root.xpath('/sample/analytics/' + self.exp_name + '[@ID]'): #reads all ID_names for the given experiment
                   attrib_list.append(existent_exp.get('ID')) # and appends them to a list
               #print(attrib_list)
               transformed_u_input = self.transform_ID((u_input).upper().replace(' ', '_')) #variable = transformed ID 
               if transformed_u_input in attrib_list: # if transformed ID exists already
                   print(transformed_u_input, 'already exist as an ID for '+self.exp_name+'. Please try with a different one') #reject, repeat
                   continue
               else:
                   return transformed_u_input #else, accept and return experiment_ID                     
            else:
                return u_input

    def transform_ID(self, test_ID): #Converts ID  if special input is given
        if  test_ID == '':  #if input is empty => test_ID = ID
            return self.sampleID 
        elif test_ID.startswith('*'): #if input is *_something => test_ID = ID_something
            return self.sampleID + test_ID.strip('*')  
        else:
             return test_ID
#%%
                

    def write_data(self, Type_=None, Flag_= True):
        answers = ('N', 'n', 'No', 'no', 'Y', 'y', 'Yes', 'yes',)
        while Flag_:
            if Type_=='Analytics': 
                element = 'experiment'
                self.addexp()
                self.writeexp()
                print(self.exp_ID, 'succesfully added as a(n)', self.exp_name,' experiment.')
                
            elif Type_=='Others':
                element = 'other'
                self.addother()
                self.writeother()
                print(self.ot_name +' succesfully added as others.' )
         
            while True:
                write_data_input = input('Add a new ' + element +'element?: [Y/N]:')
                if write_data_input not in answers:
                    print('Answer was not valid. Try again typing "Y" or "N" without quotes.')
                    continue
                elif write_data_input.lower().startswith('n'):
                    return
                elif write_data_input.lower().startswith('y'):
                    break      
#%%




#file = newSample()
#file.preamble('EC_D01')
#file.ID = 'EC_D01'
#file.wait_for_input()

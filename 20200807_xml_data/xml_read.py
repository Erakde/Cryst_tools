# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 2020

@author: ec
"""

#lxml installation --> pip install lxml (external library). lxml will be used instead of xml.ElementTree
#web_tutorial: https://docs.python.org/3.5/library/xml.etree.elementtree.html
#commands and XPATH syntax https://docs.python.org/3.4/library/xml.etree.elementtree.html
# Commands from source https://lxml.de/api/index.html
# lxml tutorial https://lxml.de/tutorial.html
from lxml import etree
import os
from glob import glob
from xml_create import newSample  


def itersubelement(subnode, identation):
    output = identation #empty identated string to be filled as output
    output += ("<"+subnode.tag+">").upper()+" "
    vainilla = output
    if subnode.attrib != dict() and subnode.values()[0] != '': #print attribs if exist (ONLY FIRST ATTRIBUTE PRINTED!!!!)          
        output += "["+(subnode.keys()[0]).upper()+": "+subnode.values()[0]+"]"
    if subnode.text != None: #print text if exist:
        output += subnode.text.strip()
    if output == vainilla:
        return False #if output doesn't exist => no linebreak
    print(output)
    return True #if exist output => add linebreak


class xml_read(newSample):
    def __init__(self):
        self.onlyID_ = True
        self.positive_results = True   
        
#Parse all files unless a file es specified
    def parse_all(self, xmlfile_= None, printfound_=True, stop_when_found_=False):
        self.file_not_found_error = False
        self.res_found = dict()
        self.res_notfound = dict()
        self.stop_when_found = stop_when_found_
        self.sample_found = False
        
        if xmlfile_!= None:
            self.parse(xmlfile_)
            if self.file_not_found_error:
                return
            
        elif xmlfile_ == None:
            for filename in glob("*.xml"):
                if self.stop_when_found and self.sample_found:
                    return
                self.parse(filename)
        
        if printfound_:
            if self.positive_results:
                if self.res_found == dict():
                    print('No results found.')
                else:
                    for file, text in self.res_found.items():
                        print(text, 'found in', file) 
                        
            elif not self.positive_results:
                if self.res_notfound == dict():
                    print('No results found.')
                else:
                    for file, text in self.res_notfound.items():
                        print('"'+text + '" not found in', file)
            
            
            
    #function only keeps values of the last file that contains self.sampleID
    #OnlyID = False searchs for any matching text (made for find method)
    def parse(self, filename_,): 
        try:
            self.sampleID == None
        except AttributeError:
            if self.user_input != None:
                pass
            else:
                print('Error at parse function, SampleID is missing')
                return
        print('\nREADING',filename_,'...')
        try:
            file = open(os.path.join(os.getcwd(), filename_), 'r')
            if self.onlyID_:
                #if 'ID=' is found in line => parse, store self.root, close file, return
                if 'ID="'+ self.sampleID+'"' in file.read(): 
                    #print(self.ExpID,'found in', file.name)
                    self.xmlfile = filename_
                    parser = etree.XMLParser(remove_blank_text=True)
                    tree = etree.parse(self.xmlfile, parser)
                    root = tree.getroot()
                    #print(root.attrib)
                    self.root = root
                    self.res_found[filename_] = self.sampleID
                    #print('\n',self.sampleID, 'FOUND IN', filename_, '\n')
                    file.close()
                    #pretty = etree.tostring(root, encoding="unicode", pretty_print=True) #https://lxml.de/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output                                              
                    print(self.sampleID, 'found in', filename_, '!!')
                    self.sample_found = True
                    
                    return
                else:
                    self.res_notfound[filename_] = self.sampleID
                    self.sampleID_not_found_error = True
                    print(self.sampleID, 'not found in', filename_)
                    file.close()
                    return
            elif not self.onlyID_:
                if self.user_input in file.read():
                    #print(self.user_input, 'FOUND IN', filename_)
                    self.res_found[filename_] = self.user_input
                    file.close()
                    return
                else:
                    self.res_notfound[filename_] = self.user_input
                    file.close()
                    return
            else:
                print('Not identified error in parse() method')
                file.close
        except FileNotFoundError:
            print(filename_, 'not found.')
            self.file_not_found_error = True
            return
                    
#cat filename.xml samplename. If no filename given => parse all files and cat first match
    def cat(self, sampleID_, filepath_= None): 
        self.sampleID = sampleID_
        self.parse_all(xmlfile_=filepath_)
        try:
            self.root == True
        except AttributeError:
            #if no results found => return
            return
        samplelist = self.root.xpath('//sample[@ID="'+self.sampleID+'"]')
        #print('//sample[@ID="'+self.sampleID+'"]')
        #print(samplelist)
        spacer =('------------------------------o------------------------------').center(60)
        spacer2=('----------------------------     ----------------------------').center(60)
        print(spacer)        
        for element in samplelist:  #iter all sample that matches with the given input
            print((("<"+element.tag+" ID: ").upper()+element.get('ID')+">").center(60)) #print <SAMPLE ID: $sample_id> as title
            print(spacer)
            
            for child in element.iterchildren(): #iterate  over <sample> childrens
                print(("<"+child.tag+">").upper().center(60)) #print title
    
                for grandchild in child.iterchildren(): 
                    flag = itersubelement(grandchild, "") #itersubelement in child; flag adquires boolean value from itersubelement(), corrects linebreaks if there is no content in the elements.
    
                    for grandgrandchild in grandchild.iterchildren():
                        flag = itersubelement(grandgrandchild, "   ") #itersubelement in grandchild
                        for grandgrandgrandchild in grandgrandchild.iterchildren():
                            itersubelement(grandgrandgrandchild, "        ")
                    if flag:
                        print('')
                print('')
                print(spacer2)
            
            """DISCLAIMER: DATA IS ONLY READED UNTIL GRANDGRANDCHILDREN OF <SAMPLE> """
    

    def pretty_print(self, element):
        if element.attrib == {}:
            self.pretty_attrib = 'None'
            return
        try:
            attrib_name = list(element.attrib)[0]
            attrib_val = element.attrib.get(attrib_name)
            self.pretty_attrib = attrib_name +': ' + attrib_val
        except IndexError:
            self.pretty_attrib = 'None'
        print(f"{element.tag:<15}{self.pretty_attrib:>20}")

        
    def locate(self, sampleID_, filepath_=None):
        self.sampleID = sampleID_
        self.parse_all(xmlfile_ = filepath_)
        try:
            self.target = self.root.xpath('//*[@ID="'+self.sampleID+'"]')
        except AttributeError:
            #No results found => return
            return
        spacer = '------------------o------------------'
        print(f"\n{'Elements':<15}{'Attributes':>1}")
        print(spacer)
        for child in self.target:
            self.pretty_print(child)
            for ancestor in child.iterancestors():
                self.pretty_print(ancestor)
        print(spacer)
        
    def find(self, user_input, filepath_= None, positive_results_ = True):
        self.onlyID_ = False
        self.positive_results = positive_results_
        self.user_input = user_input
        self.parse_all(xmlfile_= filepath_)
        
    def sample_append(self, sampleID_, filepath_ = None):
        self.file_not_found_error = False
        self.sampleID_not_found_error = False
        self.sampleID = sampleID_
        self.filepath = filepath_
        self.parse_all(xmlfile_=filepath_, printfound_=False, stop_when_found_=True)
        if not self.file_not_found_error and not self.sampleID_not_found_error:
            self.wait_for_input()

        
        
        
        
    
        
#file = xml_read()

# =============================================================================
# #file.sample_append('EC_D21301')
# #file.sample_append('EC_D01', filepath_= 'EC_D01.xml')
# #file.sample_append('EC_D07981', filepath_= 'EC_D01.xml')
# #file.sample_append('EC_D01', filepath_= 'EC_D01.xmlasdasdsa')
# #file.sample_append('EC_D010987', filepath_= 'EC_D01.xm098709l')
# 
# =============================================================================

#file.find('pxrd')
#file.find('pxrd', filepath_='EC_D01.xml')
#file.find('pxrd', filepath_ = 'EC_A01.xml')
#file.find('pxrd', filepath_ = 'asdsasad.xml')

# =============================================================================
#file.find('pxrd', positive_results_ = False)
# file.find('pxrd', filepath_='EC_D01.xml', positive_results_ = False)
# file.find('pxrd', filepath_ = 'EC_A01.xml', positive_results_ = False)
# file.find('pxrd', filepath_ = 'asdsasad.xml', positive_results_ = False)
# 
# =============================================================================

# =============================================================================
# file.sampleID = 'EC_D01'
# file.parse_all(xmlfile_ = 'EC_D01.xml')
# 
# =============================================================================

# =============================================================================
# file.locate('EC_D01')
# file.locate('EC_D01', filepath_ = 'EC_D01.xml')
# file.locate('EC_D01', filepath_ = 'EC_A01.xml')
# file.locate('EC_D01', filepath_ = 'asdsasad.xml')
# 
# =============================================================================

# =============================================================================
# file.cat('EC_D01')
# file.cat('EC_D01', filepath_ = 'EC_D01.xml')
# file.cat('EC_D01', filepath_ = 'EC_A01.xml')
# file.cat('EC_D01', filepath_='EC_D01.xmlasda')
# file.locate('td_d338')
# 
# =============================================================================

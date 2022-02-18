# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:50:11 2020

@author: ec
"""
import cmd2
from xml_create import newSample
from xml_read import xml_read
import argparse
import os

class UserPromp(cmd2.Cmd):
    
    def __init__(self):
        super().__init__()
        with open('./_PATH/PATH.txt', 'r') as f:   
            print('Getting PATH from PATH.txt file...')
            PATH = f.readline().strip().split('=')[1]
            f.close()
        print('Setting PATH to', PATH)
        try:
            os.chdir(PATH)
        except FileNotFoundError:
            print('Invalid PATH in PATH.txt')
        self.cwd = os.getcwd()
    


    newsample_parser = argparse.ArgumentParser()
    newsample_parser.add_argument('ID', help='Sample ID, e.g. EC_A01')
    @cmd2.with_argparser(newsample_parser)
    def do_newsample(self, args):
        newSample().preamble(args.ID)

        
    modify_parser = argparse.ArgumentParser()
    modify_parser.add_argument('ID', help='Sample ID, e.g. EC_A01')
    modify_parser.add_argument('-f', '--file', help='Search in a specific file. e.g. cat -f EC_readme.xml EC_A01')
    @cmd2.with_argparser(modify_parser) 
    def do_modify(self, args):
        xml_read().sample_append(args.ID, filepath_= args.file)
    
 
    cat_parser = argparse.ArgumentParser()
    cat_parser.add_argument('ID', help='Sample ID, e.g. EC_A01')
    cat_parser.add_argument('-f', '--file', help='Search in a specific file. e.g. cat -f EC_readme.xml EC_A01')
    cat_parser.add_argument('-t', '--text', help='Not only search IDs on Attributes')
    @cmd2.with_argparser(cat_parser)   
    def do_cat(self, args):
        cat_read = xml_read()
        cat_read.cat(args.ID, filepath_= args.file)
        
        
    locate_parser = argparse.ArgumentParser()
    locate_parser.add_argument('Input', help='ID or text that is going to be located')
    locate_parser.add_argument('-f', '--file', help='Search in a specific file. e.g. locate -f EC_A01.xml EC_A01_K2')    
    @cmd2.with_argparser(locate_parser)    
    def do_locate(self, args):
        locate_read = xml_read()
        locate_read.locate(args.Input, filepath_= args.file)



    find_parser = argparse.ArgumentParser()
    find_parser.add_argument('Input', help='ID or text that is going to be located')
    find_parser.add_argument('-f', '--file', help='Search in a specific file. e.g. locate -f EC_A01.xml EC_A01_K2')
    find_parser.add_argument('-i', '--inverse', action='store_false', help='set --inverse to find in which files Input is not found' )    
    @cmd2.with_argparser(find_parser)    
    def do_find(self, args):
        find_read = xml_read()
        find_read.find(args.Input, filepath_=args.file, positive_results_= args.inverse)
    
        
        
#do_cd and do_dir found in https://github.com/python-cmd2/cmd2/blob/master/examples/python_scripting     
    @cmd2.with_argument_list
    def do_cd(self, arglist):
        """Change directory.
    Usage:
        cd <new_dir>
        """
        # Expect 1 argument, the directory to change to
        if not arglist or len(arglist) != 1:
            self.perror("cd requires exactly 1 argument:")
            self.do_help('cd')
            self.last_result = 'Bad arguments'
            return

        # Convert relative paths to absolute paths
        path = os.path.abspath(os.path.expanduser(arglist[0]))

        # Make sure the directory exists, is a directory, and we have read access
        err = None
        data = None
        if not os.path.isdir(path):
            err = f'{path} is not a directory'
        elif not os.access(path, os.R_OK):
            err = f'You do not have read access to {path}'
        else:
            try:
                os.chdir(path)
            except Exception as ex:
                err = f'{ex}'
            else:
                self.poutput(f'Successfully changed directory to {path}')
                data = path
                self.cwd = os.getcwd()

        if err:
            self.perror(err)
        self.last_result = data

    # Enable tab completion for cd command
    def complete_cd(self, text, line, begidx, endidx):
        # Tab complete only directories
        return self.path_complete(text, line, begidx, endidx, path_filter=os.path.isdir)

    dir_parser = argparse.ArgumentParser()
    dir_parser.add_argument('-l', '--long', action='store_true', help="display in long format with one item per line")

    @cmd2.with_argparser(dir_parser, with_unknown_args=True)
    def do_dir(self, args, unknown):
        """List contents of current directory."""
        # No arguments for this command
        if unknown:
            self.perror("dir does not take any positional arguments:")
            self.do_help('dir')
            self.last_result = 'Bad arguments'
            return

        # Get the contents as a list
        contents = os.listdir(self.cwd)

        for f in contents:
            self.poutput(f'{f}')
        self.poutput('')

        self.last_result = contents
            
     
# =============================================================================
#     cd_parser = argparse.ArgumentParser()         
#     cd_parser.add_argument('path', nargs='?', default=None, help='Change directory to path')    
#     
#     complete_cd = cmd2.Cmd.path_complete(path_filter=os.path.isdir)
#     #complete_bar = functools.partialmethod(cmd2.Cmd.path_complete, path_filter=os.path.isdir)
#     #https://cmd2.readthedocs.io/en/latest/features/completion.html
#     @cmd2.with_argparser(cd_parser)   
#     def do_cd(self, args):
#         if args.path == None:
#             print(os.getcwd())
#         else:
#             try:
#                 os.chdir(args.path)
#             except FileNotFoundError:
#                 print(os.path.join(os.getcwd(), args.path),'is not a valid directory')
# =============================================================================
     
    
if __name__ == '__main__':
    import sys
    c = UserPromp()
    sys.exit(c.cmdloop())
    
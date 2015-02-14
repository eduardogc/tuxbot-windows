#!/usr/bin/env python

import os
import cmd
import pyreadline as readline
import aiml # aiml parser/processor
import os # fs operations
import getpass # get user from session
import ruleProcessor # process rules of the robot
import re
import sys

def learnUserName():
    user = getpass.getuser()
    answer = k.respond("My name is " + user)

def doGreet():
    print "\n Hello "+getpass.getuser()+", I'm Tuxbot, your assistant on Linux. \n Please ask me whatever you want. \n Type \"view help\" if you need a manual. \n "


class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        global k
        k = aiml.Kernel()
        tuxbotpath = os.getenv('TUXBOT')
        if tuxbotpath == None:
            print "\nYou have to setup TUXBOT environment variable in order to execute correctly."
            print "Please add the path of tuxbot on your system\'s variables."
            sys.exit(0)
        tuxbotpath = tuxbotpath + '/alice'
        os.chdir(tuxbotpath) # going to dictionary
        list=os.listdir('./');
        for item in list: # load dictionary one by one
            k.learn(item)
        learnUserName()
        doGreet()
        ruleProcessor.startVariablesFromPersist()
        self.prompt = "> "


    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        if (self.prompt is not None and self.prompt != ""):
            answer = k.respond(line)
            ruleProcessor.processAnswer(answer)
        else:
            answer = ""

if __name__ == '__main__':
    try:
        console = Console()
        console.cmdloop()
    except KeyboardInterrupt:
        print '\nbye!'

import re # regex
import os # OS operations
import textToSpeech # robot talks with this

def readDirectoryList(appName):
    # format entry to aproximate it to the most general way possible
    formattedAppName = re.sub(r"[^A-Za-z]", "", appName)
    formattedAppName = formattedAppName.lower()
    tam = len(str(formattedAppName))

    # get file's directory
    cwd = os.getcwd()
    directoriesFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/directories.txt"

    # read the file line by line and mount a list
    with open(directoriesFile, 'r') as f:
        content = f.readlines()

    # scan list searching for the directory
    i=0
    while(i < len(content)):
        if(content[i][:tam] == formattedAppName):
            directory = content[i][tam+1:]
            return directory
        else:
            i += 1
    return 1

def printAndSay(answer):
    print answer
    textToSpeech.sayAnswer(answer)

def formatSearchTerm(term):
    formattedTerm = re.sub(r" ", "+", term)
    return formattedTerm

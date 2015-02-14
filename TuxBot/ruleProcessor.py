import os
from subprocess import call # run external commands
import utilities # many functions live there
import timeProcessor # for calculate hours
import webbrowser # opens default web browser 4 web search
import psutil # for monitor cpu and memory
import re # regex

def startVariablesFromPersist():
    timeProcessor.startVariablesFromPersist()

def monitorMemoryAndCPU():
    percCpu = psutil.cpu_percent(interval=1)
    percMemory = psutil.virtual_memory().percent
    if(percCpu > 95):
        utilities.printAndSay(k.respond('CPU ERROR'))
    if(percMemory > 85):
        utilities.printAndSay(k.respond('MEMORY ERROR'))

def getCpuStatus():
    percCpu = psutil.cpu_percent(interval=1)
    return percCpu

def getMemoryStatus():
    percMemory = psutil.virtual_memory().percent
    return percMemory

def getSwapStatus():
    percSwap = psutil.swap_memory().percent
    return percSwap

def processAnswer(answer):
    if answer == "":
        True == True
    elif answer[:4] == "OPEN":
        res = utilities.readDirectoryList(answer[5:])
        if res != 1:
            call(res, shell=True)
        else:
            utilities.printAndSay('Sorry, I cannot open that.')
    elif answer[:4] == "BASH":
        call(answer[5:], shell="True")
    elif answer[:9] == "EDIT PATH":
        cwd = os.getcwd()
        fullpath = "%windir%\system32\\notepad.exe " + os.path.abspath(os.path.join(cwd, os.pardir)) + "\directories.txt"
        call(fullpath, shell="True")
    elif answer[:4] == "CALC":
        call("set /a "+answer[5:], shell="True")
        print ""
    elif answer[:9] == "START_DAY":
        res = timeProcessor.startDay()
        if res != 1:
            utilities.printAndSay(answer[10:])
    elif answer[:11] == "START_LUNCH":
        res = timeProcessor.startLunch()
        if res != 1:
            utilities.printAndSay(answer[12:])
    elif answer[:10] == "STOP_LUNCH":
        res = timeProcessor.stopLunch()
        if res != 1:
            utilities.printAndSay(answer[11:])
    elif answer[:10] == "FINISH_DAY":
        time = timeProcessor.calculateTime()
        if time != 1:
            utilities.printAndSay(answer[11:])
            timeProcessor.formatTimeAndShow(time)
    elif answer[:9] == "VIEW CSV":
        # get file's directory
        cwd = os.getcwd()
        cwd = re.sub(r" ", "\ ", cwd)
        csvFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeBase.csv"
        call("libreoffice " +  csvFile, shell=True)
    elif answer[:11] == "BING SEARCH":
        formattedSearch = utilities.formatSearchTerm(answer[12:])
        webbrowser.open('http://www.bing.com/search?q='+formattedSearch)
    elif answer[:13] == "GOOGLE SEARCH":
        formattedSearch = utilities.formatSearchTerm(answer[14:])
        webbrowser.open('https://www.google.com.br/#q='+formattedSearch)
    elif answer[:13] == "MEMORY STATUS":
        utilities.printAndSay('The used memory is '+str(getMemoryStatus())+'%.')
    elif answer[:11] == "SWAP STATUS":
        utilities.printAndSay('The used swap is '+str(getSwapStatus())+'%.')
    elif answer[:10] == "CPU STATUS":
        utilities.printAndSay('The CPU is at '+str(getCpuStatus())+'%.')
    elif answer[:17] == "CPU MEMORY STATUS":
        utilities.printAndSay('The CPU is at '+str(getCpuStatus())+'% '+'and the used memory is '+str(getMemoryStatus())+'%.')
    elif answer[:17] == "LUNCH STATUS":
        res = timeProcessor.getLeftLunchTime()
        if res != -1:
            if res > 0:
                utilities.printAndSay("The left lunch time is: " + str(res))
            else:
                utilities.printAndSay("No time left. Get back to work!")
    elif answer == "HELP":
        print "This is the manual for the Tuxbot."
        print "\n You may talk with the robot at any time, asking it. \n And also you have \"magical\" words to tell the bot to do something for you:"
        print "\n OPEN * -> opens an application. The availability of the apps may vary."
        print "\n EDIT [DIRECTORY] PATH[S] -> edit paths that opens applications"
        print "\n CALC * -> do some calculation"
        print "\n SEARCH * IN * -> do some offline search of something in some place"
        print "\n Calculate time on work: Just use this:"
        print "\n START DAY -> start the cronometer, on morning."
        print "\n START LUNCH -> stop the cronometer for lunch."
        print "\n STOP LUNCH -> starts the cronometer for afternoon."
        print "\n FINISH DAY -> stops the cronometer and calculates time, giving the result. It also saves the result on a csv file."
        print "\n VIEW CSV -> opens csv file where time is stored."
        print "\n You can also search on web using Bing or Google."
    else:
        utilities.printAndSay(answer)

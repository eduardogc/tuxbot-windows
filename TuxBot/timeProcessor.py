from datetime import datetime, timedelta
import os
import csvProcessor
import textToSpeech
import re

dt1 = 0
dt2 = 0
dt3 = 0
dtLunch = 0
dt1Formatted = 0
dt2Formatted = 0
dt3Formatted = 0
dtLunchFormatted = 0
startedDay = False
startedLunch = False
stoppedLunch = False

def clearDatetimeFile():
    cwd = os.getcwd()
    timeDatFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeprocessor.dat"
    open(timeDatFile, 'w').close()

def startVariablesFromPersist():
    cwd = os.getcwd()
    timeDatFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeprocessor.dat"
    if os.stat(timeDatFile).st_size != 0:
        with open(timeDatFile, 'r') as f:
             content = f.readlines()
        global dt1
        global dt2
        global dt3
        global dt1Formatted
        global dt2Formatted
        global dt3Formatted
        global startedDay
        global startedLunch
        global stoppedLunch
        tam = len(content)
        if tam >= 1:
            dt1 = processLine(content[0])
            dt1Formatted = formatHour(dt1.time())
            if str(dt1) != "0":
                startedDay = True
        if tam >= 2:
            dt2 = processLine(content[1])
            dt2Formatted = formatHour(dt2.time())
            if str(dt2) != "0":
                startedLunch = True
        if tam >= 3:
            dt3 = processLine(content[2])
            dt3Formatted = formatHour(dt3.time())
            if str(dt3) != "0":
                stoppedLunch = True

def processLine(line):
    res = re.sub(r"\n", "", line)
    res = datetime.strptime(res, "%Y-%m-%d %H:%M:%S.%f")
    return res

def editLines(lineToWrite, timeGot):
    cwd = os.getcwd()
    timeDatFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeprocessor.dat"
    with open(timeDatFile, 'r') as file:
        data = file.readlines()
    if(data != []):
        if len(data) >= lineToWrite + 1:
            data[lineToWrite] = timeGot
        else:
            data.append(timeGot)
    else:
        data.append(timeGot)
    with open(timeDatFile, 'w') as file:
        file.writelines(data)


def startDay():
    if startedDay == True:
        printAndSay('You already started your day, bro.')
        return 1
    global dt1
    global dt1Formatted
    global startedDay
    startedDay = True
    dt1 = datetime.now()
    editLines(0, str(dt1)+'\n')
    dt1Formatted = formatHour(dt1.time())
    return 0

def startLunch():
    if not startedDay:
        printAndSay('Oops! You didn\'t started day!')
        return 1
    if startedLunch == True:
        printAndSay('Someone forgot what ate. You already did that, take a snack.')
        return 1
    global dt2
    global dt2Formatted
    global startedLunch
    startedLunch = True
    dt2 = datetime.now()
    editLines(1, str(dt2)+'\n')
    dt2Formatted = formatHour(dt2.time())
    return 0

def stopLunch():
    if not startedLunch:
        printAndSay('Oops! You didn\'t started the lunch!')
        return 1
    if stoppedLunch == True:
        printAndSay('You already did that. Someone\'s sleeping after lunch, and it\'s not me.')
        return 1
    global dt3
    global dt3Formatted
    global stoppedLunch
    stoppedLunch = True
    dt3 = datetime.now()
    editLines(2, str(dt3)+'\n')
    dt3Formatted = formatHour(dt3.time())
    return 0

def calculateTime():
    if not stoppedLunch:
        printAndSay('Oops! You didn\'t got your meal!')
        return 1
    dt4 = datetime.now()
    dt4Formatted = formatHour(dt4.time())
    dr1 = (dt2 - dt1) + (dt4 - dt3)
    dr1Formatted = formatHour(dr1)
    csvProcessor.writeCSV(dt1Formatted, dt2Formatted, dt3Formatted, dt4Formatted, dr1Formatted)
    global startedDay, startedLunch, stoppedLunch
    startedDay = startedLunch = stoppedLunch = False
    clearDatetimeFile()
    return dr1Formatted

def getLeftLunchTime():
    if not startedLunch:
        printAndSay('Oops! You didn\'t started the lunch!')
        return -1
    if stoppedLunch == True:
        printAndSay('You already finished your lunch.')
        return -1
    global dtLunch
    dtLunch = datetime.now()
    drL = timedelta(hours=1, minutes=30) - (dtLunch - dt2)
    dtLunchFormatted = formatHour(drL)
    return dtLunchFormatted

def formatTimeAndShow(time):
    timeformat = str(time).split(':')
    printAndSay("Time spent on activities: " + timeformat[0] + " hours, " + timeformat[1] + " minutes and " + timeformat[2] + " seconds.")
    printAndSay("Your time was stored on a csv file. Just ask me to open it if u need.")

def formatHour(dt):
    formattedHour = str(dt).split('.')
    return formattedHour[0]

def printAndSay(answer):
    print answer
    textToSpeech.sayAnswer(answer)

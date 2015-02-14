# -*- coding: utf-8 -*-
import csv
import os
import time

def writeCSV(entrada, saidaAlmoco, voltaAlmoco, saida, totalDia):
    # verify if the file exists
    firstTime = verifyFirstTime()
    # get file's directory
    cwd = os.getcwd()
    csvFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeBase.csv"
    with open(csvFile, 'a') as csvfile:
        fieldnames = ['DATA', 'ENTRADA', 'SAIDA_ALMOCO', 'VOLTA_ALMOCO', 'SAIDA', 'TOTAL_DIA']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if firstTime == True:
            writer.writeheader()
        writer.writerow({'DATA': time.strftime("%d/%m/%Y"), 'ENTRADA': entrada, 'SAIDA_ALMOCO': saidaAlmoco, 'VOLTA_ALMOCO': voltaAlmoco, 'SAIDA': saida, 'TOTAL_DIA': totalDia})

def readCSV():
    # get file's directory
    cwd = os.getcwd()
    csvFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeBase.csv"
    with open(csvFile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['DATA'], row['ENTRADA'], row['SAIDA_ALMOCO'], row['VOLTA_ALMOCO'], row['SAIDA'], row['TOTAL_DIA'])

def verifyFirstTime():
    # get file's directory
    cwd = os.getcwd()
    csvFile = os.path.abspath(os.path.join(cwd, os.pardir)) + "/timeBase.csv"
    if not os.path.isfile(csvFile):
        return True
    else:
        return False

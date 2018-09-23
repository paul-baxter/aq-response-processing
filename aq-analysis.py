import sys
import getopt
import os
import re
import numpy

###
### Very basic AQ data extraction from website questionnaire
###
### data from the 2018 Lincoln Summer Scientist
###

def main(argv):

    print ''
    print 'AQ data extraction'
    print '------------------'

    inputfile = 'data_in.csv'   #default
    outputfile = 'aq_data.csv' #default

    try:
        opts, args = getopt.getopt(argv[1:], 'hi:', ['help', 'input='])
    except getopt.GetoptError as err:
        print err
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-i', '--input'):
            inputfile = arg

    lineCount = 0
    allData = []
    singleData = []
    if os.path.exists(inputfile):
        try:
            datafile = open(inputfile, 'r')
            for line in datafile:
                #need to ignore the first 4 lines...
                if lineCount < 4:
                    lineCount += 1  #!!!
                    continue
                line = line.rstrip()
                splitLine = line.split(',')
                #if not enough data on line, then skip
                if len(splitLine) < 28:
                    continue
                #perform line operations
                pID = splitLine[17]         #participant ID
                #handle cases where there is no ID provided...
                if pID == '':
                    pID = 'error'
                    print 'pID error detected'
                duration = splitLine[5]     #questionnaire duration
                #if time taken is too low, then something wrong - log error...
                if int(duration) < 10:
                    duration = 'too short'
                    print 'duration error detected'
                singleData.append(pID)
                singleData.append(duration)
                #calculate response-based score
                score = AQscore(splitLine)
                singleData.append(score)
                if score == 'error':
                    singleData.append('error')
                elif int(score) > 6:
                    singleData.append('1')
                elif int(score) <= 6:
                    singleData.append('0')
                #line count increment...
                lineCount += 1
                #next line prep
                allData.append(singleData)
                singleData = [] #assign empty list, don't delete...
        finally:
            datafile.close()
    else:
        print 'File does not exist: ', inputfile
        sys.exit()

    print ''

    #sort the list by pID (not based on integer conversion...)
    allData.sort(key=lambda x: x[0])

    try:
        outfile = open(outputfile, "w")
        outfile.write('pID,duration,AQscore,AQ>6\n')
        for participant in allData:
            toWrite = ','.join(participant)
            outfile.write(toWrite + '\n')
    except IOError as err:
        print err
    finally:
        outfile.close()

    print 'DONE'


#####################################################################

def usage():
    print 'Usage: aq-analysis.py -i <inputfile.csv>'


def matchResponseAgree(response):
    if (response == 'Slightly Agree') or (response == 'Definitely Agree'):
        return (1, 'ok')
    elif (response == 'Slightly Disagree') or (response == 'Definitely Disagree'):
        return (0, 'ok')
    else:
        print 'ERROR: unrecognised question response - ', response
        return (-1, 'error')


def matchResponseDisagree(response):
    if (response == 'Slightly Agree') or (response == 'Definitely Agree'):
        return (0, 'ok')
    elif (response == 'Slightly Disagree') or (response == 'Definitely Disagree'):
        return (1, 'ok')
    else:
        print 'ERROR: unrecognised question response - ', response
        return (-1,'error')


def AQscore(splitLine):
    #calculate the AQ score from the split line data
    score = 0
    back = ''
    errMsg = ''
    #Q1
    back, errMsg = matchResponseAgree(splitLine[18])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q2
    back, errMsg = matchResponseDisagree(splitLine[19])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q3
    back, errMsg = matchResponseDisagree(splitLine[20])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q4
    back, errMsg = matchResponseDisagree(splitLine[21])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q5
    back, errMsg = matchResponseAgree(splitLine[22])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q6
    back, errMsg = matchResponseDisagree(splitLine[23])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q7
    back, errMsg = matchResponseAgree(splitLine[24])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q8
    back, errMsg = matchResponseDisagree(splitLine[25])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q9
    back, errMsg = matchResponseDisagree(splitLine[26])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #Q10
    back, errMsg = matchResponseAgree(splitLine[27])
    if errMsg == 'error':
        return 'error'
    score += int(back)
    #result
    return str(score)



if __name__ == "__main__":
    main(sys.argv)

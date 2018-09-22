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
                duration = splitLine[5]     #questionnaire duration
                singleData.append(pID)
                singleData.append(duration)
                #calculate response-based score
                print(singleData)
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

    try:
        outfile = open(outputfile, "w")
        outfile.write('Data\n')
        for participant in allData:
            toWrite = ','.join(participant)
            outfile.write(toWrite + '\n')
    except err:
        print err
    finally:
        outfile.close()

    print 'DONE'


#####################################################################

def usage():
    print 'Usage: aq-analysis.py -i <inputfile.csv>'


def matchResponse(response):
    if (response == 'Slightly Agree') or (response == 'Definitely Agree'):
        return 1
    elif (response == 'Slightly Disagree') or (response == 'Definitely Disagree'):
        return 0
    else:
        print ('Error: unrecognised question response - ', response)
        return -1


if __name__ == "__main__":
    main(sys.argv)

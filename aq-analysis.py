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

    lineWordCount = 0
    lineNumbers = numpy.array([])
    words = {}
    delims = ", ", "-", "\n", "."                  #delimiters
    regexPattern = '|'.join(map(re.escape, delims))     #regular expression
    if os.path.exists(inputfile):
        try:
            datafile = open(inputfile, 'r')
            for line in datafile:
                splitLine = re.split(regexPattern, line)
                if splitLine[0] == '':
                    continue
                lineWordCount += len(splitLine)
                lineNumbers = numpy.append(lineNumbers, [len(splitLine)])
                record_word_cnt(splitLine, words)
        finally:
            datafile.close()
    else:
        print 'File does not exist: ', inputfile
        sys.exit()

    print ''

    try:
        outfile = open(outputfile, "w")
        outfile.write('Data\n')
    except err:
        print err
    finally:
        outfile.close()


#####################################################################

def usage():
    print 'Usage: aq-analysis.py -i <inputfile.csv>'


if __name__ == "__main__":
    main(sys.argv)

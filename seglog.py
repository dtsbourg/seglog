import argparse
import csv
import math
import operator
import os
import re
import sys

def usage():
    return """seglog.py

    Splits a log file into multiple files based on a parameter predicate

        Arguments:

        `-h`: help message for this script
        `-i`: relative path to input file
        `-o`: prefix for output file name
        `-p`: string representation of predicate 

        Default settings:

        `output_path` is the current directory
        headers are displayed on each split file
        segmented files are prefixed with `flight-{n}.txt`

        Available operators: > / >= / < / <= / == / !=

        Example usage:

        ```
        >> python seglog.py -i log.txt -o flight -p "state >= 0 && acc_x > 20"
        >> python seglog.py -i ../Desktop/Log_file_201.txt -p "gps_status==2 || healthy != 0"
        ```

    """

def create_log(chunk, output_file, output_path, n):
    """ Create the log file and place it at the output_path """

    current_output = os.path.join(  # Create new output file
        os.getcwd(),
        output_path,
        "{}-{}.txt".format(output_file, n)
        )

    with open(current_output, 'w+') as output_csv:
        writer = csv.writer(output_csv, delimiter='\t')
        writer = writer.writerows(chunk)


def read_log(file):
    """ Read the log file and populate the all_rows array with the read results """

    with open(file, 'r') as input_csv:
        datareader = csv.reader(input_csv, delimiter='\t')
        all_rows = []
        for row in datareader:
           all_rows.append(row)

        return all_rows

def op_map(op_char):
    """ Map provided operator with Python function """

    ops = { "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
            "==": operator.eq,
            "!=": operator.ne }
    return ops[op_char]

def parse_file(input_file, output_file, predicate):
    """ Main driver """

    output_path = os.getcwd() + "/logs/"

    print '\nReading log file : ', input_file, "\n"

    all_rows = read_log(input_file)  # Read log file

    print "Extracting header rows : \n"

    header = all_rows.pop(0)         # Extract header

    print '\n'.join('{}: {}'.format(*k) for k in enumerate(header))     # Print rows with indices

    print "\nSplitting log with : "
    
    ### Log splitting ###
    predicates = parse_predicate(predicate) # Array of parsed predicates
    chunk = [[] for j in range(100)]        # Prepare empty chunks
    j = 0
    match = False
    for i in range(0, len(all_rows)):
        pred = True
        for p in predicates:
            param_index = header.index(p[0])
            operator = op_map(p[1])
            threshold = p[2]
            pred &= operator(float(all_rows[i][param_index]), float(threshold))

        if pred and i != len(all_rows)-1:
            match = True
            chunk[j].append(all_rows[i])
        else:
            if match == True: # We found a segment
                chunk[j].insert(0, header)                              # Add header to new file
                create_log(chunk[j], output_file, output_path, j+1)     # Create new file
                j+=1                                                    # Increment file counter
                match = False                                           # Move on to next file

    if j == 0:
        print "Unable to segment log file, please choose another predicate"
    else:
        print "Done segmenting log file."
        print "File segmented into ", j, " files."

def parse_predicate(input):
    """ Parse predicate input form CLI """

    match = re.findall("(?:(?:(\w+)\s*([!=><]{1,2})\s*((?:\-?\d*\.?)?\d+))\s*(?:[&|]{0,2})\s*)", input)
    print match, '\n'
    return match
    
def parse_args():
    """ Parse command line arguments with the argparse library """

    parser = argparse.ArgumentParser(usage=usage())
    # Optional Arguments
    parser.add_argument("-o", "--output_file", help="output file name template (no extension)", type=str, required=False, default="flight")

    requiredNamed = parser.add_argument_group('required named arguments')
    # Required Arguments
    requiredNamed.add_argument("-i", "--input_file", help="input log file (with extension)", type=str, required=True)
    requiredNamed.add_argument("-p", "--predicate" , help="predicate : \"var_name operator threshold\" ", type=str, required=True)
 
    return parser.parse_args()

def clean_log_dir():
    """ Clean the output directory of previous logs """

    filelist = [ f for f in os.listdir(os.getcwd() + "/logs") if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.getcwd() + "/logs/" + f)

def check_dir_structure():
    """ Check if output directory exists, if not create it """
    
    if not os.path.isdir(os.getcwd() + "/logs/"):
        os.mkdir(os.getcwd() + "/logs/")

def main():
    check_dir_structure()
    clean_log_dir()
    args = parse_args()
    parse_file(args.input_file, args.output_file, args.predicate)

### Main ###
if __name__ == "__main__":
    main()

import sys, getopt
import pandas as pd


def main(argv):

    # Parse arguments
    input_file, output_file = arg_parser(argv)

    # Import results
    results_table = pd.read_excel(input_file)

    # count true positives, true negatives, false positives and false negatives
    confmat = (
        results_table
        .groupby(['label', 'classification'])
        .count()
        .unstack()
    )

    print(confmat)
    # calculate scores

    # write results to file
    

def arg_parser(argv):
    opts, args = getopt.getopt(argv,"i:o:",["ifile=","ofile="])

    for opt, arg in opts:
        if opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg
    return input_file, output_file


if __name__ == "__main__":
   main(sys.argv[1:])
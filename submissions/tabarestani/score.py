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
    confmat.fillna(0, inplace=True)
    print(confmat)
    try:
        true_positives  = confmat.iloc[1, 2]
    except IndexError:
        true_positives = 0

    try:
        false_positives  = confmat.iloc[0, 2]
    except IndexError:
        false_positives = 0

    try:
        true_negatives  = confmat.iloc[0, 1]
    except IndexError:
        true_negatives = 0

    try:
        false_negatives  = confmat.iloc[1, 1]
    except IndexError:
        false_negatives = 0

    

    # calculate some metrics


    # write results to file
    string = f'tp = {true_positives}, fp = {false_positives}, tn = {true_negatives}, fn = {false_negatives}'
    print(f'writing results to: {output_file}')
    with open(output_file, 'w') as file:
        file.write(string)

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
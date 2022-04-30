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

    true_positives  = confmat.iloc[1, 1]
    false_positives  = confmat.iloc[0, 1]
    true_negatives  = confmat.iloc[0, 0]
    false_negatives  = confmat.iloc[1, 0]

    # calculate some metrics


    # write results to file
    print(f'writing results to: {output_file}')
    with open(output_file, 'w') as file:
        file.writelines(confmat.__str__())

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
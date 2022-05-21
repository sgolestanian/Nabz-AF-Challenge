# This script will run your model on the whole test dataset
# and store the results in an excel.
from contextlib import redirect_stdout
import sys, getopt
import progressbar

from model import AFDetector
from scipy.io import loadmat
import pandas as pd
import numpy as np


def main(argv):

    # Parse argumnets
    dataset_path, output_file = arg_parser(argv)

    # Load dataset
    print(f'Loading dataset from {dataset_path}')
    matfile = loadmat(dataset_path)
    test_dataset = matfile['Nabz_PL'][0]
    dataset_fs = np.array(matfile['Fs']).squeeze() # dataset sampling freq
    print(f'Sampling freq: {dataset_fs}')

    # Initialize af_detector
    af_detector = AFDetector(sample_rate = dataset_fs)

    print(len(test_dataset))
    result_table = []
    with progressbar.ProgressBar(max_value=len(test_dataset), redirect_stdout=True) as bar:
        for i, data in enumerate(test_dataset):
            filename = data[0][0]
            recordname = filename.split('.')[0]
            label_field = data[3]
            if len(label_field)==0:
                continue
            label_str = label_field[0]
            label = 1 if label_str=='AF' else 0
            ecg_lead_1 = np.array(data[1][0])
            if len(ecg_lead_1)==0:
                bar.update(i)
                continue
            af_class = af_detector.classify(ecg_lead_1).numpy()
            result_table.append([recordname, label, af_class])
            bar.update(i)

    result_table = pd.DataFrame(result_table, columns = ['recordname', 'label', 'classification'])
    result_table.to_excel(output_file, index=False)
    print(f'Wrote results in: {output_file}')

def arg_parser(argv):
    opts, args = getopt.getopt(argv,"d:o:",["dataset=","output="])

    for opt, arg in opts:
        if opt == '-d' or opt == '--dataset':
            dataset_file = arg
        elif opt == '-o' or opt == '--output':
            output_file = arg
    
    if not dataset_file.endswith('.mat'):
        print('Invalid dataset path.')
        sys.exit(2)

    if not output_file.endswith('.xlsx'):
        print('Output file must be *.xlsx.')
        sys.exit(2)
    return dataset_file, output_file


if __name__ == "__main__":
   main(sys.argv[1:])

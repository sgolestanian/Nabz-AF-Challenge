# This script will run your model on the whole test dataset
# and store the results in an excel.

from .model import AFDetector
from scipy.io import loadmat
import pandas as pd


DATASET_PATH = ''
DATASET_SAMPLERATE = 800

# Initialize af_detector
af_detector = AFDetector(sample_rate = DATASET_SAMPLERATE)

# Load dataset
test_dataset = loadmat(DATASET_PATH)


result_table = []
for data in test_dataset:
    # process data

    # store data in table
    #result_table.append()
    pass

result_table = pd.DataFrame(result_table, columns = ['recordname', 'label', 'classification'])
result_table.to_excel('results.xlsx')

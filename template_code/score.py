import pandas as pd

# Import results
results_table = pd.read_excel('results.xlsx')

# count true positives, true negatives, false positives and false negatives
confmat = (
    results_table
    .groupby(['label', 'classification'])
    .count()
    .unstack()
)

# calculate scores

# write results to file
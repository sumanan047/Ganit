import pandas as pd
import h5py

with h5py.File('finite_difference_results.h5', 'r') as hf:
    data = hf['data'][:]
    time = hf['time'][:]
    space = hf['space'][:]

df = pd.DataFrame(data=data, index=time, columns=space)

print(df)
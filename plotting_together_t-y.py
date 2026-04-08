
# %%

import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %% Read files and combine dataframe

# Condition search term for files
DIR_DATA      = "/Users/m.wehrens/Data_UVA/_BIODSC_smallconsults/20260408_Seb_combiningdata/"
STR_CONDITION = "_cAMPinG1_"

# Look for the files
data_file_list = glob.glob(
    DIR_DATA + "*" + STR_CONDITION + "*.xlsx"
    )

# Load them as df, adding filename as identifier for the sample
df_list = []
for file in data_file_list:
    # Load
    df = pd.read_excel(file)
    # Extract filename
    df['filename'] = file.split('/')[-1]
    
    # Fix time column, removing " s" and converting to real
    df['Time'] = df['Time'].str.replace(" s", "").astype(float)
    
    # Filter based on "Region" column, those starting with "ROI "
    df = df[df['Region'].str.startswith("ROI ")]
    
    # Add to list
    df_list.append(df)

# Now merge
df_data = \
    pd.concat(df_list, ignore_index=True)



# %% Now determine bins

# Determine the average interval
mean_interval = np.mean([np.max(df['Time'])/len(df) for df in df_list])
# Determine the longest time an experiment took
total_time = np.max(df['Time'])
# Now set time bin edges accordingly
time_bin_edges = np.arange(0, total_time + mean_interval, mean_interval) - mean_interval/2
# Determine bin centers
time_bin_centers = (time_bin_edges[:-1] + time_bin_edges[1:]) / 2

# Assign each time point in the df a bin
# Function to assign bin to timepoint
def get_bin(t):
    """return bin center based on t"""
    for i in range(len(time_bin_edges)-1):
        if time_bin_edges[i] <= t < time_bin_edges[i+1]:
            return time_bin_centers[i]
    return np.nan  
# Apply to df
df_data['time_bin'] = df_data['Time'].apply(get_bin)


# %% Now plot

FIELD_VALUE = "Mean τ, Intensity Weighted  ns"

# Calculate the average and standard error for each of the bins and plot the
# datapoints that way per bin
df_plot = df_data.groupby('time_bin')[['Time', FIELD_VALUE]].agg(['mean', 'sem']).reset_index()

# Now plot using seaborn
sns.set_style("whitegrid")
# Add seperate lines for each dataset
sns.lineplot(x='Time', y=FIELD_VALUE, data=df_data, hue='filename', errorbar=None) #, alpha=0.5, linewidth=0.5)
plt.plot(df_list[0]['Time'], df_list[0][FIELD_VALUE])
# Add average line
sns.lineplot(x=('Time', 'mean'), y=(FIELD_VALUE, 'mean'), data=df_plot, linewidth=1.0)
# now add error bars
plt.errorbar(x=df_plot[('Time', 'mean')], 
             y=df_plot[(FIELD_VALUE, 'mean')],
             xerr=df_plot[('Time', 'sem')],
             yerr=df_plot[(FIELD_VALUE, 'sem')], fmt='none', capsize=5)



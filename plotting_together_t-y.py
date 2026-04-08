
# %%

import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %% Read files and combine dataframe

# Condition search term for files
DIR_DATA      = "/Users/m.wehrens/Data_UVA/_BIODSC_smallconsults/20260408_Seb_combiningdata/"
STR_CONDITION = "_cAMPinG1_"
# STR_CONDITION = "_Flamindo2_"
# STR_CONDITION = "_GFLamp2_"

# Make a plot subdir
os.makedirs("plots", exist_ok=True)

# misc
cm_to_inch = 1/2.54

# %%

# Look for the files
data_file_list = glob.glob(
    DIR_DATA + "*" + STR_CONDITION + "*.xlsx"
    )
# Remove temp files starting with ~
data_file_list = [f for f in data_file_list if not os.path.basename(f).startswith("~")]

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
mean_interval = np.mean([np.max(df['Time'])/(len(np.unique(df['Time']))-1) for df in df_list])
# Determine the longest time an experiment took
total_time = np.max(df['Time'])
# Now set time bin edges accordingly
time_bin_edges = np.arange(0, total_time + 2*mean_interval, mean_interval) - mean_interval/2
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
df_plot = df_data.groupby('time_bin')[['Time', FIELD_VALUE]].agg(['mean', 'sem', 'std']).reset_index()

# Plot in style 1
# Now plot using seaborn
fig, ax = plt.subplots(figsize=(10*cm_to_inch, 5*cm_to_inch))
sns.set_style("white")
# plot the bin edges as lines
for edge in time_bin_edges:
    ax.axvline(x=edge, color='grey', linestyle='-', linewidth=.5)
# Now scatter plot Time vs. FIELD_VALUE
sns.scatterplot(x='Time', y=FIELD_VALUE, data=df_data, hue='filename', style='Region', ax=ax, s=2**2)
# And scatterplot of the average
sns.scatterplot(x=df_plot[('Time', 'mean')], y=df_plot[(FIELD_VALUE, 'mean')], color='black', s=3**2, label='Average', ax=ax)
# add error bars
ax.errorbar(x=df_plot[('Time', 'mean')], 
            y=df_plot[(FIELD_VALUE, 'mean')],
            xerr=df_plot[('Time', 'std')],
            yerr=df_plot[(FIELD_VALUE, 'sem')], fmt='none', capsize=0, 
            linewidth=1.0,
            color='black')
# remove the legend
ax.legend().remove()
plt.tight_layout()
fig.savefig("plots/combined_plot1" + STR_CONDITION + ".pdf")
fig.savefig("plots/combined_plot1" + STR_CONDITION + ".png", dpi=600)

# Plot in style 2
fig, ax = plt.subplots(figsize=(10*cm_to_inch, 5*cm_to_inch))
# Now plot using seaborn
# Style without grid
sns.set_style("white")
# Add seperate lines for each dataset
sns.lineplot(x='Time', y=FIELD_VALUE, data=df_data, hue='filename', 
             errorbar=None, units='Region', estimator=None,
             linewidth=.25, ax=ax)
# Add average line
sns.lineplot(x=('Time', 'mean'), y=(FIELD_VALUE, 'mean'), data=df_plot, linewidth=1.0, color='black', ax=ax)
# now add error bars
ax.errorbar(x=df_plot[('Time', 'mean')], 
            y=df_plot[(FIELD_VALUE, 'mean')],
            xerr=df_plot[('Time', 'std')],
            yerr=df_plot[(FIELD_VALUE, 'sem')], fmt='none', capsize=0, 
            linewidth=1,
            color='black')
# remove legend
ax.legend().remove()
plt.tight_layout()
# Save the plot
fig.savefig("plots/combined_plot2" + STR_CONDITION + ".pdf")
fig.savefig("plots/combined_plot2" + STR_CONDITION + ".png", dpi=600)

# %%

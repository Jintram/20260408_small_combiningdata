

# Combining different datasets in a y(t) plot

.. when t series are not exactly consistent. 

See the file `plotting_together_t-y.py`.

My solution was to first determine bins based on the # of measurements 
and total amount of time, and then bin both the time data and 
y values accordingly.

See example plots below (and in `plots_examples_frozen/`). Grey vertical lines in 'plot1'
indicate bins. Coloring is per sample, symbols indicate ROIs. Same in 'plot2',
except that bin edges are not shown, and one line is shown per ROI.

![Combined plot example](plots_examples_frozen/combined_plot1_Flamindo2_.png)

![Combined plot example](plots_examples_frozen/combined_plot2_Flamindo2_.png)

## Potential improvements
 
 
The interval during the loop seems ±constant, but the time between the 
1st and 2nd measurement isn't. Might be smarter to set up bins 
centered around another datapoint, not t=0.

Perhaps the interval within one dataset isn't constant, could also calculate /
check that out that more accurately. (I'm now simply assuming it's identical, 
and therefor dividing total_time/(n_measurements-1).)
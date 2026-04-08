

# Combining different datasets in an y(t) plot

.. when t series are not exactly consistent. 

My solution was to first determine bins based on the # of measurements 
and total amount of time, and then bin both the time data and 
y values accordingly.

See example plots in `plots_examples_frozen/`. Grey vertical lines in 'plot1'
indicate bins. Coloring is per sample, symbols indicate ROIs. Same in 'plot2',\
except that bin edges are not shown, and one line is shown per ROI.


See the file `plotting_together_t-y.py`.
from bokeh.plotting import *
from numpy import pi

# define starts/ends for wedges from percentages of a circle
percents = [0,0.04228571428571429,0.09485714285714286,0.4137142857142857,0.4491428571428571]

myList = []
for i in range(len(percents)):
    myList.append(sum(percents[:i+1]))

#percent = [0, a, a+b, a+b+c, a+b+c+d, 1]

starts = [p*2*pi for p in myList[:-1]]
ends = [p*2*pi for p in myList[1:]]

# a color and legend for each pie piece
colors = ["red", "green", "blue", "orange"]
labels = ['Administration', 'Student Leaders', 'Faculty', 'Students']

p = figure(x_range=(-1,1.5), y_range=(-1,1.5),title="Email Sent in CS111 Spring 2015")

for i in range(len(percents)-1):
    p.wedge(x=0, y=0, radius=1, start_angle=starts[i], end_angle=ends[i], color=colors[i], legend=labels[i])
    p.text(1.5,0,"Faculty", text_font_size ="30pt")

# display/save everythin  
output_file("pie.html")
show(p)
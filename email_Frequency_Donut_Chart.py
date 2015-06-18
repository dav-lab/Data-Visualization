from __future__ import print_function
from bokeh.plotting import *
import base64
from math import pi, sin, cos

from bokeh.browserlib import view
from bokeh.colors import teal, tomato, gold, yellowgreen
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Wedge, AnnularWedge, ImageURL, Text
from bokeh.models import ColumnDataSource, Plot, Range1d
from bokeh.resources import INLINE

import pandas as pd

df= pd.read_csv('donutTest.csv')

#centers the chart
xdr = Range1d(start=-2, end=2)
ydr = Range1d(start=-2, end=2)


title = "Number of Emails Sent"
plot = Plot(title=title, x_range=xdr, y_range=ydr, plot_width=800, plot_height=800)

colors = {"Faculty": teal, "Student": yellowgreen, "StudentLdr": tomato, "Admin": gold}


aggregated = df.groupby("Type").agg(sum)#groups and sums the data by type
selected = aggregated[aggregated.NumEmails >=1].copy()#makes a copy of aggregated with only emails greater than or equal to 1
types = selected.index.tolist()#creates a list of the types (['Admin','Faculty,'...]) 

#following code creates list of angles for wedges
radians = lambda x: 2*pi*(x/100)
angles = selected.NumEmails.map(radians).cumsum()
end_angles = angles.tolist()
start_angles = [0] + end_angles[:-1]

#creates a ColumnDataSource for information about wedges to be used when plotting
person_source = ColumnDataSource(dict(
    start  = start_angles,
    end    = end_angles,
    colors = [colors[person] for person in types ],
))

#creates the inner wedges
glyph = Wedge(x=0, y=0, radius=1, line_color="white",
    line_width=2, start_angle="start", end_angle="end", fill_color="colors", fill_alpha=0.7)

plot.add_glyph(person_source, glyph)

def polar_to_cartesian(r, start_angles, end_angles):
    cartesian = lambda r, alpha: (r*cos(alpha), r*sin(alpha))
    points = []

    for start, end in zip(start_angles, end_angles):
        points.append(cartesian(r, (end + start)/2))

    return zip(*points)

for person, start_angle, end_angle in zip(types, start_angles, end_angles):
    #creatings chart
    versions = df[(df.Type == person) & ((df.NumEmails/100)*875 >= 12)]
    versions2 = df[(df.Type == person) & ((df.NumEmails/100)*875 < 12)]
    angles = versions.NumEmails.map(radians).cumsum() + start_angle
   
    #list of start to end angles
    end = angles.tolist() + [end_angle]
    start = [start_angle] + end[:-1]
    base_color = colors[person]
    
    fill = [ base_color.lighten(i*0.05) for i in range(len(versions) + 1) ]#lightens colors larger - > small
    emailtext = [(float(emails)/100.0)*875.0 for emails in versions.NumEmails  ]#number of emails sent by person
    totalOther = 0 # counter for number of emails sent by other
    for emails in versions2.NumEmails:
        totalOther += (float(emails)/100.0)*875.0
    nametext = [name for name in versions.Names  ]# name of the person
    text = [(b.split('@')[0] + ': '+ str(int(round(a)))) for a,b in zip(emailtext,nametext)]#formats the text displayed on the wedges
    x, y = polar_to_cartesian(1.25, start, end)
    source = ColumnDataSource(dict(start=start, end=end, fill=fill))#dictionary with start, end, and color fill values
    #Following creates outer wedges
    glyph = AnnularWedge(x=0, y=0,
        inner_radius=1, outer_radius=1.5, start_angle="start", end_angle="end",
        line_color="white", line_width=2, fill_color="fill", fill_alpha=0.7)
    plot.add_glyph(source, glyph)
    
    #Following angles the text within the wedges
    text_angle = [(start[i]+end[i])/2 for i in range(len(start))]
    text_angle = [angle + pi if pi/2 < angle < 3*pi/2 else angle for angle in text_angle]
    
    #checks if the person is a student and inserts other where there is an empty space
    #we only wanted to include the top 5 student contributors
    if person == 'Student':
        text.insert(10, 'other: ' + str(int(round(totalOther))))
    
    #The following is plotting the text for the outer wedges
    text_source = ColumnDataSource(dict(text=text, x=x, y=y, angle=text_angle))
    glyph = Text(x="x", y="y", text="text", angle="angle",
        text_align="center", text_baseline="middle")
    plot.add_glyph(text_source, glyph)

text.insert(3, 'other: ' + str(int(round(totalOther))))#inserts other for the last wedge created (StudentLdr)

x, y = polar_to_cartesian(1.25, start, end)



numtext = [ "%.02f%%" % value for value in selected.NumEmails ]#formats number of emails with percentages (inner wedges)
nametext = [name for name in types] #list of names (inner wedges)
text = [b + ': '+str(a) for a,b in zip(numtext,nametext)]

x, y = polar_to_cartesian(0.7, start_angles, end_angles)

#plottingthe text for the inner wedge
text_source = ColumnDataSource(dict(text=text, x=x, y=y))
glyph = Text(x="x", y="y", text="text", text_align="center", text_baseline="middle", text_font_size = '10pt', text_font_style = 'bold')
plot.add_glyph(text_source, glyph)


doc = Document()
doc.add(plot)


if __name__ == "__main__":
    filename = "donut.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Donut Chart"))
    print("Wrote %s" % filename)
    view(filename)
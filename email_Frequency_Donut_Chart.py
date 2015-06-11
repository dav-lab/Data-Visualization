from __future__ import print_function
from bokeh.plotting import *
import base64
from math import pi, sin, cos

from bokeh.browserlib import view
from bokeh.colors import skyblue, seagreen, tomato, orchid, firebrick, lightgray
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Wedge, AnnularWedge, ImageURL, Text
from bokeh.models import ColumnDataSource, Plot, Range1d
from bokeh.resources import INLINE

import pandas as pd

#df = browsers_nov_2013
df= pd.read_csv('donutTest.csv')

#centers the chart?
xdr = Range1d(start=-2, end=2)
ydr = Range1d(start=-2, end=2)
#
#title = "Web browser market share (November 2013)"
title = "Number of Emails Sent"
plot = Plot(title=title, x_range=xdr, y_range=ydr, plot_width=800, plot_height=800)
#
#colors = {"Chrome": seagreen, "Firefox": tomato, "Safari": orchid, "Opera": firebrick, "IE": skyblue, "Other": lightgray}
colors = {"Faculty": seagreen, "Student": tomato, "StudentLdr": orchid, "Admin": skyblue}
#aggregated = df.groupby("Browser").agg(sum)
aggregated = df.groupby("Type").agg(sum)
selected = aggregated[aggregated.NumEmails >=1].copy()
#selected.loc["Other"] = aggregated[aggregated.Share < 1].sum()
#browsers = selected.index.tolist()
types = selected.index.tolist()
##
radians = lambda x: 2*pi*(x/100)
angles = selected.NumEmails.map(radians).cumsum()
#
end_angles = angles.tolist()
start_angles = [0] + end_angles[:-1]
#
#browsers_source = ColumnDataSource(dict(
#    start  = start_angles,
#    end    = end_angles,
#    colors = [colors[browser] for browser in browsers ],
#))
person_source = ColumnDataSource(dict(
    start  = start_angles,
    end    = end_angles,
    colors = [colors[person] for person in types ],
))
#
glyph = Wedge(x=0, y=0, radius=1, line_color="white",
    line_width=2, start_angle="start", end_angle="end", fill_color="colors")

plot.add_glyph(person_source, glyph)
#
def polar_to_cartesian(r, start_angles, end_angles):
    cartesian = lambda r, alpha: (r*cos(alpha), r*sin(alpha))
    points = []

    for start, end in zip(start_angles, end_angles):
        points.append(cartesian(r, (end + start)/2))

    return zip(*points)
#
#first = True
#
#for browser, start_angle, end_angle in zip(browsers, start_angles, end_angles):
#    #creatings chart
#    versions = df[(df.Browser == browser) & (df.Share >= 0.5)]
#    angles = versions.Share.map(radians).cumsum() + start_angle
#    #list of start to end angles
#    end = angles.tolist() + [end_angle]
#    start = [start_angle] + end[:-1]
for person, start_angle, end_angle in zip(types, start_angles, end_angles):
    #creatings chart
    versions = df[(df.Type == person) & ((df.NumEmails/100)*875 >= 12)]
    versions2 = df[(df.Type == person) & ((df.NumEmails/100)*875 < 12)]
    angles = versions.NumEmails.map(radians).cumsum() + start_angle
    #list of start to end angles
    end = angles.tolist() + [end_angle]
    start = [start_angle] + end[:-1]
#    
#    base_color = colors[browser]
#    #lightens colors larger - > small
#    fill = [ base_color.lighten(i*0.05) for i in range(len(versions) + 1) ]
#    #Where is the fifth slice coming from?
#    text = [ number if share >= 1 else "" for number, share in zip(versions.VersionNumber, versions.Share) ]
#    x, y = polar_to_cartesian(1.25, start, end)
#    #dictionary with start, end, and color fill values
#    source = ColumnDataSource(dict(start=start, end=end, fill=fill))
#    #assuming this creates the wedges
#    glyph = AnnularWedge(x=0, y=0,
#        inner_radius=1, outer_radius=1.5, start_angle="start", end_angle="end",
#        line_color="white", line_width=2, fill_color="fill")
#    plot.add_glyph(source, glyph)
    base_color = colors[person]
    #lightens colors larger - > small
    fill = [ base_color.lighten(i*0.05) for i in range(len(versions) + 1) ]
    
    #Where is the fifth slice coming from?
    emailtext = [(float(emails)/100.0)*875.0 for emails in versions.NumEmails  ]
    totalOther = 0
    for emails in versions2.NumEmails:
        totalOther += (float(emails)/100.0)*875.0
    nametext = [name for name in versions.Names  ]
    #text = [ number if share >= 1 else "" for number, share in zip(versions.VersionNumber, versions.Share) ]
    text = [(b.split('@')[0] + ': '+ str(int(round(a)))) if a>=12 else 'yolo' for a,b in zip(emailtext,nametext)]
    x, y = polar_to_cartesian(1.25, start, end)
    #dictionary with start, end, and color fill values
    source = ColumnDataSource(dict(start=start, end=end, fill=fill))
    #assuming this creates the wedges
    glyph = AnnularWedge(x=0, y=0,
        inner_radius=1, outer_radius=1.5, start_angle="start", end_angle="end",
        line_color="white", line_width=2, fill_color="fill")
    plot.add_glyph(source, glyph)
#
    text_angle = [(start[i]+end[i])/2 for i in range(len(start))]
    text_angle = [angle + pi if pi/2 < angle < 3*pi/2 else angle for angle in text_angle]
    if person == 'Student':
        text.insert(10, 'other: ' + str(int(round(totalOther))))
    #if first and text:
    #    text.insert(0, 'other')
    #    offset = pi / 48
    #    text_angle.insert(0, text_angle[0] - offset)
    #    start.insert(0, start[0] - offset)
    #    end.insert(0, end[0] - offset)
    #    x, y = polar_to_cartesian(1.25, start, end)
    #    first = False
    
    text_source = ColumnDataSource(dict(text=text, x=x, y=y, angle=text_angle))
    glyph = Text(x="x", y="y", text="text", angle="angle",
        text_align="center", text_baseline="middle")
    plot.add_glyph(text_source, glyph)

text.insert(3, 'other: ' + str(int(round(totalOther))))
#offset = pi / 48
#text_angle.insert(0, text_angle[0] - offset)
#start.insert(0, 10)
#end.insert(0, 10)
x, y = polar_to_cartesian(1.25, start, end)



numtext = [ "%.02f%%" % value for value in selected.NumEmails ]
nametext = [name for name in types]
text = [b + ': '+str(a) for a,b in zip(numtext,nametext)]

x, y = polar_to_cartesian(0.7, start_angles, end_angles)

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
import datetime
import bisect
from bokeh.plotting import ColumnDataSource, figure, show, output_file
import numpy as np
from collections import OrderedDict
from bokeh.models import HoverTool

months = ["Jan","Feb","Mar","Apr","May","Jun"]
weekNumbers=[]

dates=[]
weekNumber=[]
s = datetime.datetime(2015,1,25)
e = datetime.datetime(2015,6,2)
t = s
while (t < e):
    t=t+datetime.timedelta(days=1)
    dates.append(t)
    w=str(months[t.month-1])+str(t.isocalendar()[1])
    if w not in weekNumbers:
        weekNumbers.append(w)
    weekNumber.append(w)
   

schedule={'2015-01-26': ['Lec 1', 'PS0 due', 'PS1 out'],
'2015-01-28': ['Lab 1'],
'2015-01-29': ['Lec 2'],
'2015-02-02': ['Lec 03'],
'2015-02-03': ['PS1 in', 'PS2 out'],
'2015-02-04': ['Lab 2'],
'2015-02-05': ['Lec 4'],
'2015-02-09': ['Lec 5'],
'2015-02-10': ['PS2 in', 'PS3 out'],
'2015-02-11': ['Lab 3'],
'2015-02-12': ['Lec 6'],
'2015-02-17': ['PS3 in', 'PS4 out'],
'2015-02-18': ['Lab 4'],
'2015-02-19': ['Lec 7'],
'2015-02-23': ['Lec 8'],
'2015-02-24': ['PS4 in', 'PS5 out'],
'2015-02-25': ['Lab 5'],
'2015-02-26': ['Lec 9'],
'2015-03-02': ['Lec 10'],
'2015-03-03': ['PS5 in'],
'2015-03-04': ['Lab 6'],
'2015-03-05': ['PS6 out'],
'2015-03-09': ['Lec 11'],
'2015-03-10': ['PS6 in', 'PS7 out'],
'2015-03-11': ['Lab 7'],
'2015-03-12': ['Lec 12'],
'2015-03-16': ['Lec 13', 'Lec 12'],
'2015-03-17': ['PS7 in', 'PS8 out'],
'2015-03-18': ['Lab 8'],
'2015-03-30': ['Lec 14'],
'2015-04-01': ['Lab 9', 'PS8 in', 'PS9 out'],
'2015-04-02': ['Lec 15'],
'2015-04-06': ['Lec 16'],
'2015-04-07': ['PS9 in', 'Exam2 out'],
'2015-04-08': ['Lab 10'],
'2015-04-09': ['Lec 17'],
'2015-04-13': ['Lec 18'],
'2015-04-14': ['Exam2 in', 'PS10 out'],
'2015-04-15': ['Lab 11'],
'2015-04-16': ['Lec 19'],
'2015-04-21': ['Lec 20'],
'2015-04-22': ['Lab 12'],
'2015-04-23': ['Lec 21'],
'2015-04-24': ['PS10 in'],
'2015-04-27': ['Lec 22'],
'2015-04-30': ['Lec 23'],
'2015-05-04': ['Lec 24'],
'2015-05-06': ['Lab 13'],
'2015-05-07': ['lec 25']}

date=[{'2015-06-02': 2}, {'2015-05-18': 2}, {'2015-05-17': 1}, {'2015-05-15': 1}, {'2015-05-13': 4}, {'2015-05-12': 6}, {'2015-05-11': 1}, {'2015-05-10': 1}, {'2015-05-08': 3}, {'2015-05-07': 7}, {'2015-05-06': 5}, {'2015-05-05': 3}, {'2015-05-04': 3}, {'2015-05-03': 9}, {'2015-05-02': 1}, {'2015-05-01': 3}, {'2015-04-30': 1}, {'2015-04-29': 4}, {'2015-04-28': 5}, {'2015-04-27': 4}, {'2015-04-26': 2}, {'2015-04-24': 2}, {'2015-04-23': 12}, {'2015-04-22': 10}, {'2015-04-21': 17}, {'2015-04-20': 6}, {'2015-04-19': 5}, {'2015-04-18': 6}, {'2015-04-17': 1}, {'2015-04-16': 3}, {'2015-04-15': 2}, {'2015-04-14': 19}, {'2015-04-13': 9}, {'2015-04-12': 21}, {'2015-04-11': 17}, {'2015-04-10': 2}, {'2015-04-09': 11}, {'2015-04-08': 5}, {'2015-04-07': 21}, {'2015-04-06': 10}, {'2015-04-05': 19}, {'2015-04-04': 6}, {'2015-04-03': 5}, {'2015-04-02': 7}, {'2015-04-01': 4}, {'2015-03-31': 5}, {'2015-03-30': 2}, {'2015-03-29': 5}, {'2015-03-28': 1}, {'2015-03-19': 2}, {'2015-03-18': 1}, {'2015-03-17': 1}, {'2015-03-16': 3}, {'2015-03-15': 4}, {'2015-03-14': 14}, {'2015-03-12': 3}, {'2015-03-11': 7}, {'2015-03-10': 3}, {'2015-03-09': 2}, {'2015-03-08': 9}, {'2015-03-07': 9}, {'2015-03-06': 2}, {'2015-03-05': 4}, {'2015-03-04': 3}, {'2015-03-03': 10}, {'2015-03-02': 8}, {'2015-03-01': 7}, {'2015-02-28': 13}, {'2015-02-27': 10}, {'2015-02-26': 3}, {'2015-02-25': 7}, {'2015-02-24': 5}, {'2015-02-23': 5}, {'2015-02-22': 16}, {'2015-02-21': 10}, {'2015-02-20': 6}, {'2015-02-19': 6}, {'2015-02-18': 5}, {'2015-02-17': 6}, {'2015-02-16': 8}, {'2015-02-15': 31}, {'2015-02-14': 11}, {'2015-02-13': 6}, {'2015-02-12': 10}, {'2015-02-11': 9}, {'2015-02-10': 16}, {'2015-02-09': 15}, {'2015-02-08': 16}, {'2015-02-07': 17}, {'2015-02-06': 4}, {'2015-02-05': 10}, {'2015-02-04': 6}, {'2015-02-03': 9}, {'2015-02-02': 10}, {'2015-02-01': 17}, {'2015-01-31': 9}, {'2015-01-30': 22}, {'2015-01-29': 26}, {'2015-01-28': 41}, {'2015-01-27': 88}, {'2015-01-26': 9}]

weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
days=[str(i) for i in range(1,32)]
colors = [
    "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
    "#ddb7b1", "#cc7878", "#933b41", "#550b1d"
]


month=[]

day=[]
weekday=[]
numberEmails=[]
events=[]

result=dict((k,v) for d in date for (k,v) in d.items())

for i in dates:
    i=i.strftime('%Y-%m-%d')
    if i not in result:
        result[i]=0

for key in sorted(result.iterkeys()):
    if key in schedule:
       events.append(schedule[key])
    else:
        events.append("None")
    month.append(months[(datetime.datetime.strptime(key, '%Y-%m-%d').month)-1])
    day.append(datetime.datetime.strptime(key, '%Y-%m-%d').day)
    weekday.append(weekdays[datetime.datetime.strptime(key, '%Y-%m-%d').weekday()])
    numberEmails.append(result[key])

bins=[]
for i in range(len(colors)):
    if i!=len(colors)-1:
        bins.insert(i,((max(numberEmails)-min(numberEmails))/float(len(colors)))*(i+1))
    else:
        bins.insert(i,max(numberEmails)+1)

def assignColor(number,breakpoints=bins,c=colors):
    i=bisect.bisect(breakpoints,number)
    return c[i]

color=[assignColor(number) for number in numberEmails]

source = ColumnDataSource(
    data=dict(weekNumber=weekNumber,weekday=weekday, day=day, month=month, color=color, number=numberEmails, event=events)
)
output_file('emails.html')
TOOLS = "resize,hover,save,pan,box_zoom,wheel_zoom"
p = figure(title="CS111 Emails",
    x_range=weekdays, y_range=list(reversed(weekNumbers)),
    x_axis_location="above", plot_width=900, plot_height=600,
    toolbar_location="left", tools=TOOLS)

p.rect("weekday", "weekNumber", 1, 1, source=source,
    color="color", line_color=None)

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ('date', '@month @day'),
    ('emails', '@number'),
    ('event','@event')
])
show(p)

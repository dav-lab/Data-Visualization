from collections import OrderedDict

import numpy as np
import pandas as pd

from bokeh.models import HoverTool

from bokeh.charts import Histogram, show, output_file

from collections import Counter

normal = [3, 2, 1, 2, 1, 250, 11, 2, 2, 17, 7, 11, 4, 7, 9, 4, 5, 3, 4, 13, 1, 10, 2, 2, 2, 3, 4, 5, 4, 3, 26, 2, 2, 8, 1, 4, 11, 1, 7, 17, 9, 3, 5, 20, 1, 3, 4, 3, 9, 5, 2, 5, 6, 7, 6, 5, 7, 3, 18, 37, 2, 9, 2, 3, 6, 2, 34, 4, 4, 3, 2, 2, 3, 31, 28, 1, 3, 2, 1, 4, 64, 2, 3, 6, 6, 2, 1, 12, 2]

# Minus Lyn and Sohie
#normal = [3, 2, 1, 2, 1, 11, 2, 2, 17, 7, 11, 4, 7, 9, 4, 5, 3, 4, 13, 1, 10, 2, 2, 2, 3, 4, 5, 4, 3, 26, 2, 2, 8, 1, 4, 11, 1, 7, 17, 9, 3, 5, 20, 1, 3, 4, 3, 9, 5, 2, 5, 6, 7, 6, 5, 7, 3, 18, 37, 2, 9, 2, 3, 6, 2, 34, 4, 4, 3, 2, 2, 3, 31, 28, 1, 3, 2, 1, 4, 2, 3, 6, 6, 2, 1, 12, 2]

# Dictionary
#dictionary = {u'bmorris@wellesley.edu': 3, u'jcampbe5@wellesley.edu': 2, u'csuntan@wellesley.edu': 1, u'jkim64@wellesley.edu': 2, u'llazo2@wellesley.edu': 1, u'fturbak@wellesley.edu': 250, u'sfan@wellesley.edu': 11, u'erogalew@wellesley.edu': 2, u'jpark14@wellesley.edu': 2, u'apfoerts@wellesley.edu': 17, u'mjain2@wellesley.edu': 7, u'jyang6@wellesley.edu': 11, u'avergosd@wellesley.edu': 4, u'shollan2@wellesley.edu': 7, u'maili.goodman@wellesley.edu': 9, u'sarmstr3@wellesley.edu': 4, u'amcclure@wellesley.edu': 5, u'sxu2@wellesley.edu': 3, u'ctsui@wellesley.edu': 4, u'dmckenzi@wellesley.edu': 13, u'jliu6@wellesley.edu': 1, u'hzhu3@wellesley.edu': 10, u'msvanber@wellesley.edu': 2, u'tcampbe2@wellesley.edu': 2, u'jcho7@wellesley.edu': 2, u'inoonan@wellesley.edu': 3, u'akaplon@wellesley.edu': 4, u'gferolit@wellesley.edu': 5, u'kkenneal@wellesley.edu': 4, u'jhom@wellesley.edu': 3, u'bcarver@wellesley.edu': 26, u'etaft2@wellesley.edu': 2, u'cgrote@wellesley.edu': 2, u'czheng@wellesley.edu': 8, u'msowder@wellesley.edu': 1, u'lconsidi@wellesley.edu': 4, u'hpeltzsm@wellesley.edu': 11, u'kleahy@wellesley.edu': 1, u'ajackso2@wellesley.edu': 7, u'hyaskawa@wellesley.edu': 17, u'bramanud@wellesley.edu': 9, u'ypan@wellesley.edu': 3, u'achen6@wellesley.edu': 5, u'rpricejo@wellesley.edu': 20, u'erivera@wellesley.edu': 1, u'ssun2@wellesley.edu': 3, u'bji@wellesley.edu': 4, u'svoigt@wellesley.edu': 3, u'rdodell@wellesley.edu': 9, u'jtannady@wellesley.edu': 5, u'jcherayi@wellesley.edu': 2, u'mmarkovi@wellesley.edu': 5, u'dvanderk@wellesley.edu': 6, u'haugst@wellesley.edu': 7, u'ekysel@wellesley.edu': 6, u'mjung@wellesley.edu': 5, u'achristy@wellesley.edu': 7, u'jjin@wellesley.edu': 3, u'xwu4@wellesley.edu': 18, u'rpurcell@wellesley.edu': 37, u'etang@wellesley.edu': 2, u'ayuan2@wellesley.edu': 9, u'cstenson@wellesley.edu': 2, u'hchao@wellesley.edu': 3, u'jabernat@wellesley.edu': 6, u'aschwar3@wellesley.edu': 2, u'sburns@wellesley.edu': 34, u'manaya@wellesley.edu': 4, u'jiye@wellesley.edu': 4, u'dhsiao@wellesley.edu': 3, u'ekuszmau@wellesley.edu': 2, u'lhobert@wellesley.edu': 2, u'mkim30@wellesley.edu': 3, u'rfeng2@wellesley.edu': 31, u'sbuck@wellesley.edu': 28, u'cliu4@wellesley.edu': 1, u'vzhao@wellesley.edu': 3, u'esternro@wellesley.edu': 2, u'ylee17@wellesley.edu': 1, u'astclair@wellesley.edu': 4, u'slee@wellesley.edu': 64, u'azhou4@wellesley.edu': 2, u'mwillia4@wellesley.edu': 3, u'jyoung4@wellesley.edu': 6, u'mclark3@wellesley.edu': 6, u'txu2@wellesley.edu': 2, u'chardwic@wellesley.edu': 1, u'kderamus@wellesley.edu': 12, u'mfendroc@wellesley.edu': 2}
#emails = dictionary.keys()
#normal = dictionary.values()

freqList = Counter(normal).values()

distributions = OrderedDict(normal=normal)

# create a pandas data frame from the dict
df = pd.DataFrame(distributions)
distributions = df.to_dict()

for k, v in distributions.items():
    distributions[k] = v.values()

output_file("Email per Person Frequency.html")

TOOLS = "resize,hover,save,pan,box_zoom,wheel_zoom"

#hover = hist.select(dict(type=HoverTool))
#hover.tooltips = OrderedDict([
#    ('Number of Emails', dictionary.keys()),
#    ('Participants', dictionary.values()),
#])

hover = HoverTool(
    tooltips = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("desc", "@freqList"),
    ]
)

#hist = Histogram(df, bins=len(normal), legend=True)
hist = Histogram(df, bins=10, legend=True, title = 'Email per Person Frequency Histogram', tools=[hover], xlabel = 'Numbers of Emails Sent', ylabel = 'Frequency')

show(hist)

#-------------------------------------------------------------------------------

# EXAMPLE TO WORK OFF. DELETE LATER

#from bokeh.plotting import figure, output_file, show, ColumnDataSource
#from bokeh.models import HoverTool
#
#output_file("toolbar.html")
#
#source = ColumnDataSource(
#    data=dict(
#        x=[1,2,3,4,5],
#        y=[2,5,8,2,7],
#        desa=['A', 'b', 'C', 'd', 'E'],
#    )
#)
#
#hover = HoverTool(
#    tooltips = [
#        ("index", "$index"),
#        ("(x,y)", "($x, $y)"),
#        ("desc", "@desa"),
#    ]
#)
#
#p = figure(plot_width=400, plot_height=400, tools=[hover],
#           title="Mouse over the dots")
#
#p.circle('x', 'y', size=20, source=source)
#
#show(p)
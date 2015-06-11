import pprint

CS111 = (open('CS111JS.txt', 'r')).read()

# Creates list of all non-empty lines in CS111 schedule JS
CS111List = []
for line in CS111.split('\n'):
    if len(line) != 0:
        CS111List.append(line)

# Creates list with (date, event)
CS111LessonList = []
monthDict = {'Jan': 01, 'Feb': 02, 'Mar': 03, 'Apr': 04, 'May': 05}

for i in range(0, len(CS111List)):
    for month in monthDict.keys():
        if month in CS111List[i] and len(CS111List[i-2].strip()[3:]) in range(1,10):
            CS111LessonList.append(('2015-0' + str(monthDict[CS111List[i].strip()[3:6]]) + '-' + str(CS111List[i].strip()[1:3]), CS111List[i-2].strip()[3:]))

# Creates dictionary with date as key and event list as value
CS111Dict = {}

for lessonTuple in CS111LessonList:
    date = lessonTuple[0]
    lesson = lessonTuple[1]
    if date not in CS111Dict:
        CS111Dict[date] = [lesson]
    else:
        CS111Dict[date].append(lesson)
#
for value in CS111Dict.values():
    if len(value)>1:
        if value[0] == value[1]:
            value.pop(1)

# Sorts dictionary by key

# OPTION 1 (only prints)
pprint.pprint(CS111Dict)

# OPTION 2 (can return)
#for key in sorted(CS111Dict):
#    print "%s: %s" % (key, CS111Dict[key])

# Include SI and help room sessions!

# Faculty and Student Leaders
{'Faculty': ['rpricejo@wellesley.edu', 'fturbak@wellesley.edu', 'slee@wellesley.edu', 'sbuck@wellesley.edu'], 
'Student Leaders': ['jcherayi@wellesley.edu', 'mfendroc@wellesley.edu', 'afoun@wellesley.edu', 'mjain2@wellesley.edu', 'mjung@wellesley.edu', 'ctsui@wellesley.edu', 'svoigt@wellesley.edu', 'sburns@wellesley.edu', 'bcarver@wellesley.edu']}
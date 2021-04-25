
import collections
import io ,Bidirectional_Search  , Astar
import eel
import json
import ids
import problem
from state import State
import copy

eel.init("frontend")

mynodes = list()
mygraph = collections.defaultdict(list)
robot =""
goal = []
butters = []


myinput = """5	6
1	1	1	1	x	1
2	1	1b	1r	1b	2
2p	x	1	1	1	2
2	1	1	1	1	2
1	x	x	x	1	1p"""

# address = "test3.txt"
# with open(address) as reader :
#     # print(reader.read())
#     myinput = reader.read()
# # print(myinput)

buf = io.StringIO(myinput)
n , m = map(int ,buf.readlines(1)[0].replace("\t" , " ").replace("\n" , "").split(" "))
for i in range(n):
    buffread = buf.readlines(1)[0].replace("\t" , " ").replace("\n" , "").split(" ")
    mynd = []
    for ii in range(m) : 
        mynd.append(buffread[ii])
    mynodes.append(mynd)

# x = n
# for i in mynodes :
#     print(i , end=" ")
#     if x == 1 :
#         x = n
#         print()
#     else:
#         x -= 1

for i in range(n):
    for ii in range(m) :
        pos = str(i) + str(ii)
        # pos = (i , ii)
        kind = 'o'
        if mynodes[i][ii].count('r') > 0 :
            kind = 'r'
            robot = pos
        elif mynodes[i][ii].count('p') > 0 :
            kind = 'p'
            goal.append(pos)
        elif mynodes[i][ii].count('b') > 0 :
            kind = 'b'
            butters.append(pos)
        elif mynodes[i][ii].count('x') > 0 :
            kind = 'x'
        mygraph[pos].append(kind)

        if kind == 'x':
            mygraph[pos].append(-1)
            continue
        elif not mygraph[pos][0] == 'o' :
            mygraph[pos].append(int(mynodes[i][ii][:-1]))
        else :
            mygraph[pos].append(int(mynodes[i][ii]))

        # mygraph[pos].append(-1)

        if i > 0 and not mynodes[i-1][ii] == 'x' :
            cc = mynodes[i-1][ii]
            cc = cc.replace('r',"").replace('b',"").replace('p',"")
            mygraph[pos].append((str(i-1) + str(ii) , cc))
            # mygraph[pos].append(((i-1 , ii) , cc))

        if i < (n-1) and not mynodes[i+1][ii] == 'x' : 
            cc = mynodes[i+1][ii]
            cc = cc.replace("r","").replace("b","").replace("p","")
            mygraph[pos].append((str(i+1) + str(ii) , cc))
            # mygraph[pos].append(((i+1 , ii) , cc))

        if ii > 0 and not mynodes[i][ii-1] == 'x' : 
            cc = mynodes[i][ii-1]
            cc = cc.replace("r","").replace("b","").replace("p","")
            mygraph[pos].append((str(i) + str(ii-1) , cc))
            # mygraph[pos].append(((i , ii-1) , cc))

        if ii < (m-1) and not mynodes[i][ii+1] == 'x' : 
            cc = mynodes[i][ii+1]
            cc = cc.replace("r","").replace("b","").replace("p","")
            mygraph[pos].append((str(i) + str(ii+1) , cc))
            # mygraph[pos].append(((i , ii+1) , cc))


# print(mygraph)


# path = Bidirectional_Search.BidirectionalSearch(mygraph , "10" , "22")

# print(path)

# print("what a bummer!")





@eel.expose
def main():
    init()
    GRAPH = copy.deepcopy(mygraph)
    butterPaths =[]
    robotPaths = []
    for i in range(len(butters)):
        if i > 0:
            robotPos = butterPaths[i-1][-2]
        else:
            robotPos = robot
        search = "ids"
        if search == "ids":
            q = ids.iterativeDeepening(mygraph , butters[i] , goal[i] ,20,robot=robotPos)
            print(q)
        elif search == "bidirectional":
            None
        elif search =="astar":
            q = Astar.a_star(mygraph ,  butters[i]  , goal[i]  , robotPos )
            print(q)
        butterPaths.append(q)
        robotPaths.append(findRobotPaths(robotPos , q , search , i))
        print(butterPaths)
        print(robotPaths)
    return get_json_result({
        "graph" : GRAPH,
        "pathButters" : butterPaths,
        "pathsRobot" :robotPaths})
    

    
def get_json_result(results):
    return json.dumps(results)


def whereRobotGo(first ,second):
    direction = problem.whichDirection(first,second)
    return problem.placeRobot(direction , first)

def init():
    State.setRobot(robot)
    for i in range(len(butters)):
        State.setButter(i , butters[i])



def findRobotPaths(firstRobotCoordinate ,pathButter, search, whichButter):
    robotPaths = []
    robotCoordinate  = firstRobotCoordinate
    for i in range(len(pathButter)-1):
        coordinate = whereRobotGo(pathButter[i] , pathButter[i+1])
        State.setButter(whichButter , pathButter[i])
        tmp = mygraph[pathButter[i]][0]
        mygraph[pathButter[i]][0] = 'x'
        if(search == "ids"):
            # tmp = mygraph[pathButter[i]][0]
            # mygraph[pathButter[i]][0] = 'x'
            robotPath = ids.iterativeDeepening(mygraph , robotCoordinate , coordinate ,20)
            # mygraph[pathButter[i]][0] = tmp
        elif search == "bidirectional":
            None
        elif search == "astar":
            robotPath =  Astar.a_star(mygraph , robotCoordinate , coordinate )
        mygraph[pathButter[i]][0] = tmp
        robotCoordinate = pathButter[i]
        robotPaths.append(robotPath)

    tmp = mygraph[pathButter[-1]][0]
    mygraph[pathButter[-1]][0] = 'x'    
    if(search == "ids"):
        # tmp = mygraph[pathButter[-1]][0]
        # mygraph[pathButter[-1]][0] = 'x'
        robotPath = ids.iterativeDeepening(mygraph , robotCoordinate , pathButter[-2] ,20)
        # mygraph[pathButter[-1]][0] = tmp
    elif search == "bidirectional":
            None
    elif search == "astar":
            robotPath = Astar.a_star(mygraph , robotCoordinate , pathButter[-2] )
    # mygraph[pathButter[-1]][0] = tmp
    robotPaths.append(robotPath)
    return robotPaths

eel.start('index.html' ,size=(500,500))


# init()
# q = Astar.a_star(mygraph ,  "12" , "42"  )
# print(q)

# path = Bidirectional_Search.BidirectionalSearch(mygraph , "12" , "42")
# print(path)

import argparse
from textwrap import TextWrapper
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="connected component",
                    action="store_true", default=False)
parser.add_argument("-r", "--radius", type=int, help="radius for collective influence", default=False)
parser.add_argument("num_nodes", help="nodes for removal")
parser.add_argument("input_file", help="input file")

args = parser.parse_args()

con_comp = args.c
radius = args.radius
nodes2rmv = args.num_nodes

file = args.input_file

prefix = '    '
preferredWidth = 80
wrapper = TextWrapper( width=preferredWidth, subsequent_indent=' '*len(prefix))

nodeList = list()
with open(file) as inputfile:
    for line in inputfile.readlines():
        nodeList.append(tuple(line.strip().split()))

d = defaultdict(list)
for k, v in nodeList:
    d[k].append(v)
    d[v].append(k)

num_of_keys = len(d.keys())
all_keys = list(d.keys())
all_keys = sorted([int(x) for x in all_keys])
str1 = ', '.join(str(e) for e in all_keys)
print(wrapper.fill('Size: {:d} members: [{:s}]'.format(num_of_keys, str1)))


def KeyWithMaxVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def GetVal(d):
    return d.get(KeyWithMaxVal(d))


def getConnectedComponents(d):
    def findRoot(a_node, a_root):
        while a_node != a_root[a_node][0]:
            a_node = a_root[a_node][0]
        return (a_node,a_root[a_node][1])
    myRoot = {}
    for myNode in d.keys():
        myRoot[myNode] = (myNode, 0)
    # print(myRoot)
    for myI in d:
        # print(d[myI])
        for myJ in d[myI]:
            # print(myJ)
            (myRoot_myI,myDepthMyI) = findRoot(myI,myRoot)
            # print(findRoot(myI,myRoot))
            (myRoot_myJ,myDepthMyJ) = findRoot(myJ,myRoot)
            if myRoot_myI != myRoot_myJ:
                myMin = myRoot_myI
                myMax = myRoot_myJ

                if myDepthMyI > myDepthMyJ:
                    myMin = myRoot_myJ
                    myMax = myRoot_myI
                myRoot[myMax] = (myMax,max(myRoot[myMin][1]+1,myRoot[myMax][1]))
                myRoot[myMin] = (myRoot[myMax][0],-1)
    myToRet = {}
    for myI in d:
        if myRoot[myI][0] == myI:
            myToRet[myI] = []
    for myI in d:
        myToRet[findRoot(myI,myRoot)[0]].append(myI)
    return myToRet




def run_net_destruction(d):
    updated_dic = dict(d)
    count_dic = {}
    for k, v in d.items():
        count_dic[k] = len([item for item in v if item])
    print('Removing node: {:d} with metric: {:d}'.format(int(KeyWithMaxVal(count_dic)), int(GetVal(count_dic))))
    c = KeyWithMaxVal(count_dic)
    for q, v in updated_dic.items():
        try:
            v.remove(c)
        except:
            pass
    updated_dic[c] = []
    con_com = getConnectedComponents(updated_dic)
    for k in con_com:
        num_of_keys_1 = len(con_com[k])
        # print(num_of_keys_1)
        all_keys = list(con_com[k])
        all_keys = sorted([int(x) for x in all_keys])
        str1 = ', '.join(str(e) for e in all_keys)
        # print(con_com[k])
        print(wrapper.fill('Size: {:d} members: [{:s}]'.format(num_of_keys_1, str1)))
    return updated_dic


# while nodes2rmv:
v1 = run_net_destruction(d)
v2 = run_net_destruction(v1)
v3 = run_net_destruction(v2)
v4 = run_net_destruction(v3)

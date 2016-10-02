from rpy2.robjects.packages import importr
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
pandas2ri.activate()



def DrawGraph(Achievement, layout = "random"):
    if layout == "random":
        pos = nx.random_layout(Achievement)
    if layout == "shell":
        pos = nx.shell_layout(Achievement)
    if layout == "spring":
        pos = nx.spring_layout(Achievement)
    if layout == "spectral":
        pos = nx.spectral_layout(Achievement)

    # for nodes
    auth1 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==1]
    auth2 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==2]
    auth3 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==3]
    auth4 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==4]


    auth5_10  = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=5  and d["paper_num"] < 11 ]
    auth11_20 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=11 and d["paper_num"] < 21 ]
    auth21_30 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=21 and d["paper_num"] < 31 ]

    auth31_   =  [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=31]


    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth1, node_size=50)
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth2, node_size=100, node_color = 'g')
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth3, node_size=200, node_color = 'y')
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth4, node_size=300, node_color = 'b')


    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth5_10,  node_size=400, node_color = 'c')
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth11_20, node_size=600, node_color = 'm')
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth21_30, node_size=800, node_color = 'k')

    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth31_, node_size=1000, node_color = 'k')


    # for edges
    edge1 = [ (u,v) for (u,v,d) in Achievement.edges(data = True) if d["freq"] == 1]
    edge2 = [ (u,v) for (u,v,d) in Achievement.edges(data = True) if d["freq"] == 2]
    edge3 = [ (u,v) for (u,v,d) in Achievement.edges(data = True) if d["freq"] == 3]


    nx.draw_networkx_edges(Achievement, pos, edgelist = edge1, width = 1, edge_color = "grey")
    nx.draw_networkx_edges(Achievement, pos, edgelist = edge2, width = 3,  edge_color = 'b')
    nx.draw_networkx_edges(Achievement, pos, edgelist = edge3, width = 10, edge_color = "m")

    # for labels
    names = {}
    for v, d in Achievement.nodes(data = True):
        names[v] = d["full_name"]
    nx.draw_networkx_labels(Achievement,pos,names,font_size=2, color ="w")



def DrawNetGraph(Achievement, filename):


    Links = pd.DataFrame(data=Achievement.edges(data = True))
    freq = Series([edge['freq'] for edge in Links[2]])

    Links['freq'] = freq
    del Links[2]



    Nodes = pd.DataFrame(data=Achievement.nodes(data = True))
    paper_num = Series([auth['paper_num'] for auth in Nodes[1]])
    full_name = Series([auth['full_name'] for auth in Nodes[1]])

    Nodes['paper_num'] = paper_num
    Nodes['full_name'] = full_name
    del Nodes[1]

    l = list(Nodes[0])
    Nodes[0] = Nodes[0].map(lambda a: l.index(a))
    Links[0] = Links[0].map(lambda a: l.index(a))
    Links[1] = Links[1].map(lambda a: l.index(a))


    Links_r = pandas2ri.py2ri(Links)
    ro.globalenv['source'] = Links_r[0]
    ro.globalenv['target'] = Links_r[1]
    # the index must be the integers
    ro.globalenv['freq']   = Links_r[2]
    ro.r('Links=data.frame(source,target,freq)')


    Nodes_r = pandas2ri.py2ri(Nodes)
    ro.globalenv['author_id'] = Nodes_r[0]
    ro.globalenv['num'] = Nodes_r[1]
    # the index must be the integers
    ro.globalenv['name'] = Nodes_r[2]
    ro.r('Nodes=data.frame(author_id,num,name)')

    utils = importr('utils')
    networkD3 = importr('networkD3')
    magrittr = importr('magrittr')
    R_command = '''
    a = forceNetwork(Links = Links,
                 Nodes = Nodes,
                 Source = "source",
                 Target = "target",
                 Value = "freq",
                 NodeID = "name",
                 Nodesize = "num",
                 Group = "num",
                 opacity = 0.9,
                 zoom = TRUE,
                 legend = TRUE,
                 fontSize = 15,
                 bounded = TRUE,
                 charge = -30,
                 linkWidth = JS("function(d) { return d.value*d.value; }"),
                 linkDistance = 40,
                 radiusCalculation = JS("3*Math.sqrt(d.nodesize)+5"))
                 '''

    ro.r(R_command)
    ro.r('saveNetwork(network =a ,file = "%s.html")'%filename)

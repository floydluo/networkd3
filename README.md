
## Part 0 Set up

### Before you start this tutorial, you need have the following things done.

 1. Install R in you desktop.

       Type `R` in your terminal or powershell.

       __If you enter R's interface, you are done!__

       R-3.3.1 for Mac OS: https://cran.r-project.org/bin/macosx/

       R-3.3.1 for Windows: https://cran.r-project.org/bin/windows/base/


 2. Install `numpy`, `matplotlib`, `pandas`.

 3. Install `networkX`.

 4. Install `sqlite3`.

 5. Install `rpy2`

 6. Most Important: have the database `data.sqlite` database in the current directory.

### This is a Data Visualizaition tutorial

We have all the inforamtion of the authors and documents from MISQ.

And we want to explore a relationship -- coauthorship.

By the means of drawing the dynamic network graphs, we can find some insight of the authors' relationship and make good representation of the data we got.

## Part 1 Manipulate the Data


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
import networkx as nx

# itertools is used to make the combinations list between any two authors in one documents.
import itertools

# sqlite3 is used to query authors-documents data from data.sqlite
import sqlite3
```


```python
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (16,12)

# show the figures in the notebook
%matplotlib inline
```

__Here we use `sqlite3` and SQL language to query the data we want from the database.__


__Then use `pandas` to manipulate the tables.__


```python
# make connection to the database
con = sqlite3.connect("data.sqlite")

# the SQL language, aim to get authors and their's documents information.
auth_docu_mod ='''
select authors_id, documents_id, full_name, title
from authors a, documents b, documents_authors c
where a.id=c.authors_id and c.documents_id=b.id;
'''
```


```python
# in this way, we get the table we want to manipulated.
X = pd.read_sql(auth_docu_mod, con)

# this showsthe number of author-document relationship: 2757
print(len(X))

# this code will show the first 5 rows of the table.
X.head()
```

    2757





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>authors_id</th>
      <th>documents_id</th>
      <th>full_name</th>
      <th>title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Gerald//Matlin</td>
      <td>How to Survive a Management Assessment</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>A.//Jenkins</td>
      <td>What the Information Analyst Should Know About...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>Randall//Johnson</td>
      <td>What the Information Analyst Should Know About...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>3</td>
      <td>Alfonso//Cardenas</td>
      <td>Technology for the Automatic Generation of App...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>4</td>
      <td>Robert//Bostrom</td>
      <td>MIS Problems and Failures: A Socio-Technical P...</td>
    </tr>
  </tbody>
</table>
</div>




```python
# now we want a Series
# whose index is documents' ids and
# whose value is this document's authors number.
Documents = X.documents_id.groupby(by = X.documents_id).size()

# totally, we get 1287 documents.
print(len(Documents))

# show the first 3 values.
Documents.head(3)
```

    1287





    documents_id
    1    1
    2    2
    3    1
    dtype: int64




```python
# this code is try to show the distribution of this Series
discribe = Documents.groupby(Documents).size().reset_index()
discribe
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>353</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>537</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>299</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>13</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>2</td>
    </tr>
    <tr>
      <th>7</th>
      <td>14</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



__'index' is the one paper's authors number__

we can see:

the number of papers with 1 author is 353.

the number of papers with 2 author is 537.

...

there is just one paper whose authors number is 14 !


```python
# the same logic can be applied in Authors


Authors = X.groupby(by = X.authors_id).size()
print(len(Authors))

Authors.head(3)
```

    1685





    authors_id
    1    2
    2    1
    3    1
    dtype: int64




```python
discribe = Authors.groupby(Authors).size().reset_index()
discribe
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1255</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>216</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>104</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>42</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>23</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>14</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>4</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>5</td>
    </tr>
    <tr>
      <th>10</th>
      <td>12</td>
      <td>3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>14</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>15</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>16</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>18</td>
      <td>2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>30</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>64</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



There are 1255 authors who published 1 paper  in MISQ.

There are 216  authors who published 2 papers in MISQ.

There are a super star who published 30 papers in MISQ.

And, strikingly, there is an author who published 64 papers by himself.

But this author's name is "MIS Quarterly" (I don't know why)


```python
# here I put all authors id in a set, for a further issue.
all_authors = set(X.authors_id)

# this show the total number of the authors: 1685
len(all_authors)
```




    1685



## Part 2 Make Combination


```python
# from this part, we start make combination between co-authors.

# here Y is an array, and the element is the unique document_ids of all documents
Y = X["documents_id"].unique()

x = []
y = {}

uniq = Y

len(Y)
```




    1287




```python
# this code make a dictionary y
# for every pair of key and value
# the key is the document_id
# the value is a Series whose elements are author_ids for the document that its key represents.

for article in uniq:
    y[article] = X.loc[X['documents_id'] == article]['authors_id']

len(y)
```




    1287



__Here is a sample code shows how `itertools.combinations` work__


```python
# first create a list
article = [ "auth1", "auth2", "auth3", "auth4"]

# then choose any two of them, the combinations' number is 2C4 = 6
# itertools.combinations() can do this job

g = itertools.combinations(article, 2)

# the type of g is generator, for some concerns, I will transfer it to a list.
print(type(g))
for i in g:
    print(i)
```

    <class 'itertools.combinations'>
    ('auth1', 'auth2')
    ('auth1', 'auth3')
    ('auth1', 'auth4')
    ('auth2', 'auth3')
    ('auth2', 'auth4')
    ('auth3', 'auth4')



```python
# create a list to contains all the combinations relationships.
combinations = []

for article in y:

    # here y[article] can be regarded as a list
    # I add list() here, to change generator to list.
    g = list(itertools.combinations(y[article], 2))

    for sub in g:
        combinations.append(sub)

# to show how many relationship we get.
len(combinations)

```




    2243



If the list is only one element, then its combination will be 0.

Let's check whether 2243 is a correct result:



```python
# obviously, it is correct
537 + 299*3 + 76*6 + 13*10 + 6*15 + 2*21 +91
```




    2243



## Part 3 Single Auth, Success Auth and Edges

__The aim is: Get Three Tables, and Used Them to Make Networks__


```python
# here I divide the authors into two groups: success-authors and single-dogs (just a joke)
# the suc_authors are the authors who are in the list of combinations.
# the singlg_dogs are the authors who are not in the list of combinations

# to show in the networks graph
# suc_authors will have at least one edge to connect other authors
# single_dogs will just be the single dots in the graph.


suc_authors = set()
for edge in combinations:
    for auth in edge:
        suc_authors.add(auth)

single_dogs= all_authors - suc_authors

# the number of single dogs
print(len(single_dogs))
# the number of succes authors
print(len(suc_authors))

# something interesting I want to add
# intuitively, the authors who just have one paper published have great probablities to be single dogs
# however
# there are a lot of success authors just have one paper published, and
# there are also some single dogs who published 2, even 3 documents.
```

    118
    1567



```python
# here I need to add the names as the labels.
# so I want to create a DataFrame A_N, author and name

A_N = X[['authors_id', 'full_name']]
A_N = A_N.drop_duplicates()
A_N.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>authors_id</th>
      <th>full_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Gerald//Matlin</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>A.//Jenkins</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Randall//Johnson</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Alfonso//Cardenas</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Robert//Bostrom</td>
    </tr>
  </tbody>
</table>
</div>




```python
# and I change the index to authors_ids in order to spare some trouble.
A_N.index = A_N.authors_id
A_N.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>authors_id</th>
      <th>full_name</th>
    </tr>
    <tr>
      <th>authors_id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Gerald//Matlin</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>A.//Jenkins</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Randall//Johnson</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Alfonso//Cardenas</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>Robert//Bostrom</td>
    </tr>
  </tbody>
</table>
</div>




```python
# after we get author's name, then we should get authors' documents number

# then I split the table Authors to two sub-tables
# SA_paper_num: Single Author paper number
# SuA_paper_num: Succes Author paper number

SA_paper_num = Authors.ix[single_dogs]
SA_paper_num.head()
```




    authors_id
    1536    1
    1       2
    4       1
    522     1
    15      1
    dtype: int64




```python
# I must add this line to ignore those ugly pink warning boxes

from warnings import filterwarnings
filterwarnings('ignore')
```


```python
# these code is to combine authors' names and authors' papers' number together.

Single_Auth = A_N[A_N.authors_id.isin(single_dogs)]
Single_Auth["paper_num"] = SA_paper_num

Single_Auth.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>authors_id</th>
      <th>full_name</th>
      <th>paper_num</th>
    </tr>
    <tr>
      <th>authors_id</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Gerald//Matlin</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Alfonso//Cardenas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>15</td>
      <td>Peter//B.</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>19</td>
      <td>C.W.//Getz</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>20</td>
      <td>Hugh//Juergens</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
# the same logic is also applied to Success Authors

SuA_paper_num = Authors.ix[suc_authors]
SuA_paper_num.head()

Success_Auth = A_N[A_N.authors_id.isin(suc_authors)]
Success_Auth['paper_num'] = SuA_paper_num

Success_Auth.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>authors_id</th>
      <th>full_name</th>
      <th>paper_num</th>
    </tr>
    <tr>
      <th>authors_id</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>A.//Jenkins</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Randall//Johnson</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>Robert//Bostrom</td>
      <td>5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>J.//Heinen</td>
      <td>2</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>James//Johnson</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Here, the table `Single_Auth` and `Success_Auth` can be regarded as the `nodes` in the NetworkX

__Next, we should get the `edges` from the list: `combinations`.__


```python
# make the edges to Series
Edges = Series(combinations)

# for the depulicated edges, we want to get the frequency in the Series.
# therefore I need this code to make out a table with every unique Edge and its frequency.
Edges = Edges.groupby(Edges).size().reset_index()
Edges.rename(columns = {0: 'frequency', "index" : 'Edge'}, inplace = True)

# have a little view
Edges.head()

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Edge</th>
      <th>frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>(2, 3)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>(5, 6)</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>(5, 222)</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>(5, 223)</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>(7, 8)</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



__Here, we get three `Date Frame` objects: `Single_Auth`, `Success_Auth`, `Edges`. Hit the aim!__

## Part 4 Use Python's NetworkX

### 0 Introduction to NetworkX

Please refer networkx's docs: https://networkx.readthedocs.io/en/stable/

### Preface

We can think the network as a tree, the nodes (authors) in a same tree can be regarded in the same commuity.

For the whole authors from `misq` data, there are must be many trees, therefore many communities.

In a certain sense, communities may be independent to each others.

The size of the communities are different. Some communities just have one author, some have two, three, four authors, some may have hundreds authors.

It is necessary to separate them apart to each other by following some rules.

1. `First Blood`: the communities whose author number is one.

2. `Double Kill`: the communities whose author number is two.

3. `Triple Kill`: the communities whose author number is three.

4. `Quadra Kill`: the communities whose author number is four.

5. `Penta Kill`:  the communities whose author number is five or six.

6. `Rampage`:     the communities whose author number is seven or eight.

7. `Godlike`:     the communities whose author number is 10, 11, 12, 13

8. `Legendary`:   the communities whose author number is more than 700.



### 1 First Blood


```python
# this shows how to index from DataFrame
a = Single_Auth.iloc[0]
print(a)
a.authors_id
```

    authors_id                 1
    full_name     Gerald//Matlin
    paper_num                  2
    Name: 1, dtype: object





    1




```python
# 1 with 118

# First Blood, is a collection of subgraphs whose node number is only 1
First_Blood = nx.Graph()

# from Single_Auth, add all the nodes to the big graph: First_Blood.
for i in range(len(Single_Auth)):
    a = Single_Auth.iloc[i]
    # note: I also add full_name and paper_num as the attributes to each node
    First_Blood.add_node(a.authors_id, full_name =a.full_name, paper_num = a.paper_num)


```


```python
# then we want to classify different authors and draw them out in different styles

auth1 = [ auth for (auth, d) in First_Blood.nodes(data = True) if d["paper_num"] ==1]
auth2 = [ auth for (auth, d) in First_Blood.nodes(data = True) if d["paper_num"] ==2]
auth3 = [ auth for (auth, d) in First_Blood.nodes(data = True) if d["paper_num"] ==3]
auth4 = [ auth for (auth, d) in First_Blood.nodes(data = True) if d["paper_num"] >=4]
```


```python
# to see the distribution
print(len(auth1))
print(len(auth2))
print(len(auth3))
print(len(auth4))

```

    99
    15
    3
    1



```python
# let's generate a layout of this node number
pos = nx.random_layout(First_Blood)

```


```python
# now we can draw them out

# the authors who just have 1 paper
nx.draw_networkx_nodes(First_Blood,pos,nodelist = auth1, node_size=30)

# the authors who just have 2 papers, and assign its with the size: 60, color: green
nx.draw_networkx_nodes(First_Blood,pos,nodelist = auth2, node_size=60, node_color = 'g')
# the same logic
nx.draw_networkx_nodes(First_Blood,pos,nodelist = auth3, node_size=100, node_color = 'y')

# and an interesting node
nx.draw_networkx_nodes(First_Blood,pos,nodelist = auth4, node_size=500, node_color = 'b', alpha = 0.4)

```




    <matplotlib.collections.PathCollection at 0x119251fd0>



![output_47_1](https://cloud.githubusercontent.com/assets/18824134/19021641/3a012e40-88f9-11e6-81db-58f70de5a108.png)


### 2 More than First Blood


```python
# now for the success authors
G = nx.Graph()

# base on the same logics

# add nodes from Success_Auth
for i in range(len(Success_Auth)):
    a = Success_Auth.iloc[i]
    G.add_node(a.authors_id, full_name =a.full_name, paper_num = a.paper_num)

# add nodes from Edges
for i in range(len(Edges)):
    edge = Edges.iloc[i]
    G.add_edge(edge.Edge[0], edge.Edge[1], freq = edge.frequency)
```


```python
# Then we can generate the subgraphs
# G has many subgraphs
# a subgraphs consists of nodes which have edges between each
# the subgraphs are independent from each others.

# transfer the generator to list
subgraphs = list(nx.connected_component_subgraphs(G))

# get the length of the subgraphs
length = len(subgraphs)
length
```




    294




```python
# here I can group the subgraphs base on theirs nodes number
# I create a Series to record each subgraph's nodes number

subgraphs_size = Series()
for i in range(length):
    subgraphs_size.loc[i] = len(subgraphs[i].nodes())
print(subgraphs_size.head())

# then I use this code to see the distribution of subgraphs' nodes number's distribution
discribe = subgraphs_size.groupby(subgraphs_size).size().reset_index()
discribe
```

    0      2
    1     13
    2    721
    3      2
    4      4
    dtype: int64





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>0</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2</td>
      <td>156</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>84</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4</td>
      <td>30</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7</td>
      <td>4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>8</td>
      <td>3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>11</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>12</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>13</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>721</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Each subgraphs can be regarded as a community.

156 subgraphs have 2 nodes

84 subgraphs have 3 nodes

30 subgraphs have 4 nodes

Interesting and strikingly,

There is a subgraph whose node number is 721, the biggest community in the database


```python
# here I group them by their node number.

# 2 nodes
double_kill = [ subg for subg in subgraphs if len(subg.nodes()) == 2 ]

# 3 nodes
triple_kill = [ subg for subg in subgraphs if len(subg.nodes()) == 3 ]

# 4 nodes
quadra_kill = [ subg for subg in subgraphs if len(subg.nodes()) == 4 ]

# 5 - 6 nodes
penta_kill  = [ subg for subg in subgraphs
               if len(subg.nodes()) == 5  or len(subg.nodes()) == 6 ]

# 7 - 8 nodes (no 9 nodes)
rampage     = [ subg for subg in subgraphs
               if len(subg.nodes()) == 7  or len(subg.nodes()) == 8 ]

# 10, 11, 12, 13 nodes
godlike     = [ subg for subg in subgraphs
               if len(subg.nodes()) >= 10 and len(subg.nodes()) < 14]


# 721 biggest nodes              
legendary   = [ subg for subg in subgraphs
               if len(subg.nodes()) >= 14 ]
```


```python
# initialize them from nx.Graph()
Double_Kill = nx.Graph()
for subg in double_kill:
    Double_Kill.add_edges_from(subg.edges(data = True))
    Double_Kill.add_nodes_from(subg.nodes(data = True))


Triple_Kill = nx.Graph()
for subg in triple_kill:
    Triple_Kill.add_edges_from(subg.edges(data = True))
    Triple_Kill.add_nodes_from(subg.nodes(data = True))

Quadra_Kill = nx.Graph()
for subg in quadra_kill:
    Quadra_Kill.add_edges_from(subg.edges(data = True))
    Quadra_Kill.add_nodes_from(subg.nodes(data = True))

Penta_Kill = nx.Graph()
for subg in penta_kill:
    Penta_Kill.add_edges_from(subg.edges(data = True))
    Penta_Kill.add_nodes_from(subg.nodes(data = True))

Rampage = nx.Graph()
for subg in rampage:
    Rampage.add_edges_from(subg.edges(data = True))
    Rampage.add_nodes_from(subg.nodes(data = True))

Godlike = nx.Graph()
for subg in godlike:
    Godlike.add_edges_from(subg.edges(data = True))
    Godlike.add_nodes_from(subg.nodes(data = True))

Legendary = nx.Graph()
for subg in legendary:
    Legendary.add_edges_from(subg.edges(data = True))
    Legendary.add_nodes_from(subg.nodes(data = True))
```


__Then follow the same logic, we can define a function to do this job__



```python
# create a function to draw them out.



# Achievement are:
# First_Blood
# Double_Kill
# Triple_Kill
# ...
# Legendary

# layout are:
# "random"
# "spring"
# "spectral"
# "shell"

def DrawGraph(Achievement, layout = "random"):
    # choose a layout of graph
    if layout == "random":
        pos = nx.random_layout(Achievement)
    if layout == "shell":
        pos = nx.shell_layout(Achievement)
    if layout == "spring":
        pos = nx.spring_layout(Achievement)
    if layout == "spectral":
        pos = nx.spectral_layout(Achievement)

    # for nodes

    # classify the authors base on their document number
    auth1 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==1]
    auth2 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==2]
    auth3 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==3]
    auth4 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] ==4]


    auth5_10  = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=5  and d["paper_num"] < 11 ]
    auth11_20 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=11 and d["paper_num"] < 21 ]  
    auth21_30 = [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=21 and d["paper_num"] < 31 ]

    auth31_   =  [ auth for (auth, d) in Achievement.nodes(data = True) if d["paper_num"] >=31]


    # draw these author nodes

    # here we can change the nodes' size and color and transparent degree by parameter: alpha
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth1, node_size=60)
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth2, node_size=130, node_color = 'g')
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth3, node_size=150, node_color = 'y')
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth4, node_size=200, node_color = 'b')


    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth5_10,  node_size=400, node_color = 'c',alpha = 0.7)
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth11_20, node_size=500, node_color = 'm',alpha = 0.8)
    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth21_30, node_size=800, node_color = 'k',alpha = 0.9)

    nx.draw_networkx_nodes(Achievement,pos,nodelist = auth31_, node_size=1000, node_color = 'r', alpha = 0.5)


    # for edges

    # classify the edges based on their freqs
    edge1 = [ (u,v) for (u,v,d) in Achievement.edges(data = True) if d["freq"] == 1]
    edge2 = [ (u,v) for (u,v,d) in Achievement.edges(data = True) if d["freq"] == 2]
    edge3 = [ (u,v) for (u,v,d) in Achievement.edges(data = True) if d["freq"] == 3]


    # here we can change the nodes' size and color and width and transparent degree.
    nx.draw_networkx_edges(Achievement, pos, edgelist = edge1, width = 1, edge_color = "grey")
    nx.draw_networkx_edges(Achievement, pos, edgelist = edge2, width = 5,  edge_color = 'b',alpha = 0.8)
    nx.draw_networkx_edges(Achievement, pos, edgelist = edge3, width = 7, edge_color = "m",alpha = 0.7)

    # for labels
    names = {}
    for v, d in Achievement.nodes(data = True):
        names[v] = d["full_name"]
    nx.draw_networkx_labels(Achievement,pos,names,font_size=2, color ="b")


```


```python
DrawGraph(First_Blood)
```






```python
plt.close()
```


```python
DrawGraph(First_Blood, layout = "spring")
```


![output_59_0](https://cloud.githubusercontent.com/assets/18824134/19021708/e09689a8-88f9-11e6-8333-2fe58bf827cd.png)




```python
DrawGraph(Double_Kill)
```


![output_60_0](https://cloud.githubusercontent.com/assets/18824134/19021645/3a611a08-88f9-11e6-99b0-746785ea3a5c.png)




```python
DrawGraph(Double_Kill, layout = "spring")
```


![output_61_0](https://cloud.githubusercontent.com/assets/18824134/19021643/3a5bb900-88f9-11e6-8682-18cda35000d7.png)




```python
DrawGraph(Triple_Kill)
```


![output_62_0](https://cloud.githubusercontent.com/assets/18824134/19021644/3a5e02dc-88f9-11e6-9617-9ddcef0e5dd9.png)



```python
DrawGraph(Triple_Kill, layout = "spring")
```


![output_63_0](https://cloud.githubusercontent.com/assets/18824134/19021642/3a40c834-88f9-11e6-8da5-f379896b7e12.png)




```python
DrawGraph(Quadra_Kill)
```


![output_64_0](https://cloud.githubusercontent.com/assets/18824134/19021648/3a738b02-88f9-11e6-8f94-c37929fb21df.png)




```python
DrawGraph(Quadra_Kill, layout = "spring")
```


![output_65_0](https://cloud.githubusercontent.com/assets/18824134/19021649/3a83d796-88f9-11e6-9ae6-9c5fe804bc23.png)




```python
DrawGraph(Penta_Kill)
```


![output_66_0](https://cloud.githubusercontent.com/assets/18824134/19021650/3a878206-88f9-11e6-842b-731e1f01005e.png)




```python
DrawGraph(Penta_Kill, layout = "spring")
```


![output_67_0](https://cloud.githubusercontent.com/assets/18824134/19021651/3a8d8c0a-88f9-11e6-967d-be60eb4f370b.png)



```python
DrawGraph(Rampage)
```


![output_68_0](https://cloud.githubusercontent.com/assets/18824134/19021652/3a8fcc36-88f9-11e6-9d43-1dfd261cfa80.png)



```python
DrawGraph(Rampage, layout = "spring")

```


![output_69_0](https://cloud.githubusercontent.com/assets/18824134/19021653/3a9189fe-88f9-11e6-9871-a72d9d4cdd7a.png)




```python
DrawGraph(Godlike)
```


![output_70_0](https://cloud.githubusercontent.com/assets/18824134/19021654/3aa0bfdc-88f9-11e6-9e32-52d4bc90f7ae.png)




```python
DrawGraph(Godlike, layout = "spring")
```


![output_71_0](https://cloud.githubusercontent.com/assets/18824134/19021655/3aac35b0-88f9-11e6-9dc2-dc52ee91e2b4.png)



```python
DrawGraph(Legendary)
```


![output_72_0](https://cloud.githubusercontent.com/assets/18824134/19021656/3ab07350-88f9-11e6-9af8-b2037d7f2ddb.png)




```python
DrawGraph(Legendary, layout = "spring")
```


![output_73_0](https://cloud.githubusercontent.com/assets/18824134/19021657/3ab9bb68-88f9-11e6-9451-39a1db8d6441.png)




```python

```


```python

```


```python

```

## Part 5 Use R's NetworkD3

__Obviously, the graphs we got were in mess__

Even thought significant improvements can be achieved, I turned to `networkd3` now.

This is a R package.


```python
# import "importr", which means import R.
from rpy2.robjects.packages import importr

# import R object
import rpy2.robjects as ro

# import the tool to change Data Frame to R's data.frame
from rpy2.robjects import pandas2ri
pandas2ri.activate()
```

### Take the Legendary as an example


```python
# load the Links data from Legendary to Data Frame

Links = pd.DataFrame(data=Legendary.edges(data = True))
Links.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>8</td>
      <td>{'freq': 1}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7</td>
      <td>9</td>
      <td>{'freq': 1}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>84</td>
      <td>{'freq': 1}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8</td>
      <td>9</td>
      <td>{'freq': 1}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8</td>
      <td>439</td>
      <td>{'freq': 1}</td>
    </tr>
  </tbody>
</table>
</div>



__Notice that the elements in the third column are dictionaries.__

__We have to change its form__


```python
# just in this way

freq = Series([edge['freq'] for edge in Links[2]])
Links['freq'] = freq
len(freq)
```




    1294




```python
Links.head()

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>8</td>
      <td>{'freq': 1}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7</td>
      <td>9</td>
      <td>{'freq': 1}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>84</td>
      <td>{'freq': 1}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8</td>
      <td>9</td>
      <td>{'freq': 1}</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8</td>
      <td>439</td>
      <td>{'freq': 1}</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



__Now the column `freq` is cumbersome, why not delete it?__


```python
del Links[2]
Links.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>8</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7</td>
      <td>9</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>84</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8</td>
      <td>9</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8</td>
      <td>439</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



__The same logic for Nodes__


```python
Nodes = pd.DataFrame(data=Legendary.nodes(data = True))
Nodes.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>{'paper_num': 1, 'full_name': 'James//Johnson'}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>{'paper_num': 7, 'full_name': 'Kenneth//Kozar'}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>{'paper_num': 1, 'full_name': 'David//Ruch'}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>{'paper_num': 2, 'full_name': 'James//Danziger'}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22</td>
      <td>{'paper_num': 3, 'full_name': 'Malcom//Munro'}</td>
    </tr>
  </tbody>
</table>
</div>




```python
Nodes[1][0]
```




    {'full_name': 'James//Johnson', 'paper_num': 1}




```python
paper_num = Series([auth['paper_num'] for auth in Nodes[1]])
print(len(paper_num))
```

    721



```python
full_name = Series([auth['full_name'] for auth in Nodes[1]])
print(len(full_name))
```

    721



```python
Nodes['paper_num'] = paper_num
Nodes['full_name'] = full_name

```


```python
Nodes.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>paper_num</th>
      <th>full_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>{'paper_num': 1, 'full_name': 'James//Johnson'}</td>
      <td>1</td>
      <td>James//Johnson</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>{'paper_num': 7, 'full_name': 'Kenneth//Kozar'}</td>
      <td>7</td>
      <td>Kenneth//Kozar</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>{'paper_num': 1, 'full_name': 'David//Ruch'}</td>
      <td>1</td>
      <td>David//Ruch</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>{'paper_num': 2, 'full_name': 'James//Danziger'}</td>
      <td>2</td>
      <td>James//Danziger</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22</td>
      <td>{'paper_num': 3, 'full_name': 'Malcom//Munro'}</td>
      <td>3</td>
      <td>Malcom//Munro</td>
    </tr>
  </tbody>
</table>
</div>




```python
del Nodes[1]
Nodes.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>paper_num</th>
      <th>full_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>1</td>
      <td>James//Johnson</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>7</td>
      <td>Kenneth//Kozar</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>1</td>
      <td>David//Ruch</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>2</td>
      <td>James//Danziger</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22</td>
      <td>3</td>
      <td>Malcom//Munro</td>
    </tr>
  </tbody>
</table>
</div>



### Here is the Nodes and Links we have


```python
Nodes.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>paper_num</th>
      <th>full_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>1</td>
      <td>James//Johnson</td>
    </tr>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>7</td>
      <td>Kenneth//Kozar</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>1</td>
      <td>David//Ruch</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>2</td>
      <td>James//Danziger</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22</td>
      <td>3</td>
      <td>Malcom//Munro</td>
    </tr>
  </tbody>
</table>
</div>




```python
Links.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>8</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7</td>
      <td>9</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>84</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8</td>
      <td>9</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>8</td>
      <td>439</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### A big problem to solve

__Notice our author's label is a series of number__

__This series of number is not as 0, 1, 2, 3, .....__

__But in the form as 7, 8, 9, 13....__

__However, this thing matters__.


__Error raised in Rstudio__




![screen shot 2016-10-02 at 11 09 49 pm](https://cloud.githubusercontent.com/assets/18824134/19021538/9bd5b79c-88f6-11e6-8808-f70462875ec6.png)


Here my label is not as the form of 1, 2, 3, 4...

![screen shot 2016-10-02 at 11 09 38 pm](https://cloud.githubusercontent.com/assets/18824134/19021539/9d8058b8-88f6-11e6-82b0-749f49c8e4c9.png)

Error raised

### Change to the Required Form


```python
l = list(Nodes[0])
def sort(a):
    return l.index(a)
```


```python
sort(439)
```




    132




```python
sort2 = lambda a: l.index(a)
sort2(439)
```




    132




```python
Nodes[0] = Nodes[0].map(sort)
```


```python
# by this way, the problem is solved

Links[0] = Links[0].map(sort)
Links[1] = Links[1].map(sort)
Links.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>28</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>132</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



### Enter R language


```python
# transfer to the r object
Links_r = pandas2ri.py2ri(Links)
```


```python
# make the object: source, target
ro.globalenv['source'] = Links_r[0]
ro.globalenv['target'] = Links_r[1]

# the index must be the integers
ro.globalenv['freq'] = Links_r[2]

ro.r('Links=data.frame(source,target,freq)')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>target</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>28</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>132</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>109</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>130</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>66</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1</td>
      <td>52</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>3</td>
      <td>100</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>4</td>
      <td>705</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>4</td>
      <td>149</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>4</td>
      <td>5</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>5</td>
      <td>150</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>5</td>
      <td>43</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>5</td>
      <td>16</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>5</td>
      <td>111</td>
      <td>2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>6</td>
      <td>49</td>
      <td>2</td>
    </tr>
    <tr>
      <th>19</th>
      <td>6</td>
      <td>40</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>6</td>
      <td>69</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>6</td>
      <td>52</td>
      <td>2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>6</td>
      <td>53</td>
      <td>2</td>
    </tr>
    <tr>
      <th>23</th>
      <td>6</td>
      <td>54</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>6</td>
      <td>48</td>
      <td>2</td>
    </tr>
    <tr>
      <th>25</th>
      <td>7</td>
      <td>8</td>
      <td>1</td>
    </tr>
    <tr>
      <th>26</th>
      <td>7</td>
      <td>9</td>
      <td>1</td>
    </tr>
    <tr>
      <th>27</th>
      <td>8</td>
      <td>166</td>
      <td>1</td>
    </tr>
    <tr>
      <th>28</th>
      <td>8</td>
      <td>269</td>
      <td>1</td>
    </tr>
    <tr>
      <th>29</th>
      <td>8</td>
      <td>352</td>
      <td>1</td>
    </tr>
    <tr>
      <th>30</th>
      <td>8</td>
      <td>299</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1265</th>
      <td>651</td>
      <td>652</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1266</th>
      <td>653</td>
      <td>654</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1267</th>
      <td>655</td>
      <td>656</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1268</th>
      <td>657</td>
      <td>658</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1269</th>
      <td>659</td>
      <td>660</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1270</th>
      <td>661</td>
      <td>662</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1271</th>
      <td>661</td>
      <td>663</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1272</th>
      <td>662</td>
      <td>687</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1273</th>
      <td>662</td>
      <td>663</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1274</th>
      <td>662</td>
      <td>688</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1275</th>
      <td>667</td>
      <td>668</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1276</th>
      <td>667</td>
      <td>669</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1277</th>
      <td>668</td>
      <td>669</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1278</th>
      <td>672</td>
      <td>673</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1279</th>
      <td>675</td>
      <td>676</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1280</th>
      <td>681</td>
      <td>682</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1281</th>
      <td>685</td>
      <td>686</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1282</th>
      <td>687</td>
      <td>688</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1283</th>
      <td>689</td>
      <td>690</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1284</th>
      <td>691</td>
      <td>692</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1285</th>
      <td>696</td>
      <td>697</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1286</th>
      <td>696</td>
      <td>698</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1287</th>
      <td>697</td>
      <td>698</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1288</th>
      <td>699</td>
      <td>701</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1289</th>
      <td>699</td>
      <td>700</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1290</th>
      <td>700</td>
      <td>701</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1291</th>
      <td>702</td>
      <td>703</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1292</th>
      <td>706</td>
      <td>707</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1293</th>
      <td>706</td>
      <td>708</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1294</th>
      <td>707</td>
      <td>708</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>1294 rows × 3 columns</p>
</div>




```python
# this is the same logic for Nodes
Nodes_r = pandas2ri.py2ri(Nodes)
ro.globalenv['author_id'] = Nodes_r[0]
ro.globalenv['num'] = Nodes_r[1]

# the index must be the integers
ro.globalenv['name'] = Nodes_r[2]

ro.r('Nodes=data.frame(author_id,num,name)')

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>author_id</th>
      <th>num</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1</td>
      <td>James//Johnson</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>7</td>
      <td>Kenneth//Kozar</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>1</td>
      <td>David//Ruch</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3</td>
      <td>2</td>
      <td>James//Danziger</td>
    </tr>
    <tr>
      <th>5</th>
      <td>4</td>
      <td>3</td>
      <td>Malcom//Munro</td>
    </tr>
    <tr>
      <th>6</th>
      <td>5</td>
      <td>5</td>
      <td>Gordon//Davis</td>
    </tr>
    <tr>
      <th>7</th>
      <td>6</td>
      <td>8</td>
      <td>Gerardine//DeSanctis</td>
    </tr>
    <tr>
      <th>8</th>
      <td>7</td>
      <td>1</td>
      <td>Charles//Franz</td>
    </tr>
    <tr>
      <th>9</th>
      <td>8</td>
      <td>7</td>
      <td>Daniel//Robey</td>
    </tr>
    <tr>
      <th>10</th>
      <td>9</td>
      <td>1</td>
      <td>Robert//Koeblitz</td>
    </tr>
    <tr>
      <th>11</th>
      <td>10</td>
      <td>30</td>
      <td>Izak//Benbasat</td>
    </tr>
    <tr>
      <th>12</th>
      <td>11</td>
      <td>5</td>
      <td>Albert//Dexter</td>
    </tr>
    <tr>
      <th>13</th>
      <td>12</td>
      <td>2</td>
      <td>Cynthia//Breath</td>
    </tr>
    <tr>
      <th>14</th>
      <td>13</td>
      <td>13</td>
      <td>Blake//Ives</td>
    </tr>
    <tr>
      <th>15</th>
      <td>14</td>
      <td>3</td>
      <td>Tor//Guimaraes</td>
    </tr>
    <tr>
      <th>16</th>
      <td>15</td>
      <td>1</td>
      <td>Vasudevan//Ramanujam</td>
    </tr>
    <tr>
      <th>17</th>
      <td>16</td>
      <td>4</td>
      <td>J.//Couger</td>
    </tr>
    <tr>
      <th>18</th>
      <td>17</td>
      <td>3</td>
      <td>Francois//Bergeron</td>
    </tr>
    <tr>
      <th>19</th>
      <td>18</td>
      <td>5</td>
      <td>Mary//Culnan</td>
    </tr>
    <tr>
      <th>20</th>
      <td>19</td>
      <td>3</td>
      <td>E.//Swanson</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20</td>
      <td>7</td>
      <td>Michael//Vitale</td>
    </tr>
    <tr>
      <th>22</th>
      <td>21</td>
      <td>2</td>
      <td>Robert//Leitheiser</td>
    </tr>
    <tr>
      <th>23</th>
      <td>22</td>
      <td>10</td>
      <td>James//Wetherbe</td>
    </tr>
    <tr>
      <th>24</th>
      <td>23</td>
      <td>3</td>
      <td>James//Brancheau</td>
    </tr>
    <tr>
      <th>25</th>
      <td>24</td>
      <td>4</td>
      <td>Andrew//Boynton</td>
    </tr>
    <tr>
      <th>26</th>
      <td>25</td>
      <td>9</td>
      <td>Robert//Zmud</td>
    </tr>
    <tr>
      <th>27</th>
      <td>26</td>
      <td>1</td>
      <td>George//Houdeshel</td>
    </tr>
    <tr>
      <th>28</th>
      <td>27</td>
      <td>8</td>
      <td>Hugh//Watson</td>
    </tr>
    <tr>
      <th>29</th>
      <td>28</td>
      <td>1</td>
      <td>John//Mahium</td>
    </tr>
    <tr>
      <th>30</th>
      <td>29</td>
      <td>4</td>
      <td>Houston//Carr</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>692</th>
      <td>691</td>
      <td>1</td>
      <td>Jonathan//Hua Ye</td>
    </tr>
    <tr>
      <th>693</th>
      <td>692</td>
      <td>1</td>
      <td>Hock/Hai/Teo</td>
    </tr>
    <tr>
      <th>694</th>
      <td>693</td>
      <td>1</td>
      <td>Michelle//Carter</td>
    </tr>
    <tr>
      <th>695</th>
      <td>694</td>
      <td>1</td>
      <td>Giri/Kumar/Tayi</td>
    </tr>
    <tr>
      <th>696</th>
      <td>695</td>
      <td>1</td>
      <td>Anand//Jeyaraj</td>
    </tr>
    <tr>
      <th>697</th>
      <td>696</td>
      <td>1</td>
      <td>Scott/R./Boss</td>
    </tr>
    <tr>
      <th>698</th>
      <td>697</td>
      <td>1</td>
      <td>Gregory//Moody</td>
    </tr>
    <tr>
      <th>699</th>
      <td>698</td>
      <td>1</td>
      <td>Peter//Polak</td>
    </tr>
    <tr>
      <th>700</th>
      <td>699</td>
      <td>1</td>
      <td>Ilgaz//Arikan</td>
    </tr>
    <tr>
      <th>701</th>
      <td>700</td>
      <td>1</td>
      <td>Jessica//Pye</td>
    </tr>
    <tr>
      <th>702</th>
      <td>701</td>
      <td>1</td>
      <td>Amrit//Tiwana</td>
    </tr>
    <tr>
      <th>703</th>
      <td>702</td>
      <td>1</td>
      <td>Wencui//Han</td>
    </tr>
    <tr>
      <th>704</th>
      <td>703</td>
      <td>1</td>
      <td>Serkan//Ada</td>
    </tr>
    <tr>
      <th>705</th>
      <td>704</td>
      <td>1</td>
      <td>Richard//Nolan</td>
    </tr>
    <tr>
      <th>706</th>
      <td>705</td>
      <td>1</td>
      <td>Basil//Wheeler</td>
    </tr>
    <tr>
      <th>707</th>
      <td>706</td>
      <td>1</td>
      <td>Il//Im</td>
    </tr>
    <tr>
      <th>708</th>
      <td>707</td>
      <td>1</td>
      <td>Jongkun//Jun</td>
    </tr>
    <tr>
      <th>709</th>
      <td>708</td>
      <td>1</td>
      <td>SEOK-OH//JEONG</td>
    </tr>
    <tr>
      <th>710</th>
      <td>709</td>
      <td>1</td>
      <td>Roland/T./Rust</td>
    </tr>
    <tr>
      <th>711</th>
      <td>710</td>
      <td>1</td>
      <td>Lior//Fink</td>
    </tr>
    <tr>
      <th>712</th>
      <td>711</td>
      <td>1</td>
      <td>Dorit//Nevo</td>
    </tr>
    <tr>
      <th>713</th>
      <td>712</td>
      <td>1</td>
      <td>Jack//Ewers</td>
    </tr>
    <tr>
      <th>714</th>
      <td>713</td>
      <td>2</td>
      <td>Scott//Hamilton</td>
    </tr>
    <tr>
      <th>715</th>
      <td>714</td>
      <td>1</td>
      <td>Lynne//Bracker</td>
    </tr>
    <tr>
      <th>716</th>
      <td>715</td>
      <td>1</td>
      <td>Ian//Montgomery</td>
    </tr>
    <tr>
      <th>717</th>
      <td>716</td>
      <td>1</td>
      <td>Jack//Hogue</td>
    </tr>
    <tr>
      <th>718</th>
      <td>717</td>
      <td>1</td>
      <td>Robert//Alloway</td>
    </tr>
    <tr>
      <th>719</th>
      <td>718</td>
      <td>1</td>
      <td>Robert//Mann</td>
    </tr>
    <tr>
      <th>720</th>
      <td>719</td>
      <td>1</td>
      <td>Michael//Shank</td>
    </tr>
    <tr>
      <th>721</th>
      <td>720</td>
      <td>1</td>
      <td>Charles//Dickinson</td>
    </tr>
  </tbody>
</table>
<p>721 rows × 3 columns</p>
</div>




```python
# import R's library
utils = importr('utils')
networkD3 = importr('networkD3')
magrittr = importr('magrittr')
```


```python
# have a look at our data.fram object
ro.r("Nodes[1:5,]")
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>author_id</th>
      <th>num</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1</td>
      <td>James//Johnson</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>7</td>
      <td>Kenneth//Kozar</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>1</td>
      <td>David//Ruch</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3</td>
      <td>2</td>
      <td>James//Danziger</td>
    </tr>
    <tr>
      <th>5</th>
      <td>4</td>
      <td>3</td>
      <td>Malcom//Munro</td>
    </tr>
  </tbody>
</table>
</div>




```python
ro.r("Links[1:5,]")
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>target</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>28</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>132</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
# write the R command
# here the configuration can be set.
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
             radiusCalculation = JS("3* Math.sqrt(d.nodesize) +5 "))
             '''
```

__For more specific description of the function `forceNetwork`, please have a check in the MarkDown file: `forceNetwork.md` in this repository__


```python
ro.r(R_command)
```




    R object with classes: ('forceNetwork', 'htmlwidget') mapped to:
    <ListVector - Python:0x11a4dbe88 / R:0x11f08a420>
    [ListV..., RNULL..., RNULL..., ..., RNULL..., RNULL..., ListV...]
    R object with classes: ('forceNetwork', 'htmlwidget') mapped to:
    <ListVector - Python:0x11a4dbe88 / R:0x11f08a420>
    [ListV..., RNULL..., RNULL..., ..., RNULL..., RNULL..., ListV...]
      width: <class 'rpy2.rinterface.RNULLType'>
      rpy2.rinterface.NULL
      height: <class 'rpy2.rinterface.RNULLType'>
      rpy2.rinterface.NULL
      ...
      x: <class 'rpy2.rinterface.RNULLType'>
      rpy2.rinterface.NULL
      width: <class 'rpy2.rinterface.RNULLType'>
      rpy2.rinterface.NULL
    R object with classes: ('forceNetwork', 'htmlwidget') mapped to:
    <ListVector - Python:0x11a4dbe88 / R:0x11f08a420>
    [ListV..., RNULL..., RNULL..., ..., RNULL..., RNULL..., ListV...]




```python
ro.r('saveNetwork(network = a, file = "8_legendary.html")')
```




    rpy2.rinterface.NULL



### Create a Function to Do this Job


```python
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
                 charge = -80,
                 linkWidth = JS("function(d) { return d.value*d.value; }"),
                 linkDistance = 40,
                 radiusCalculation = JS("3*Math.sqrt(d.nodesize)+5"))
                 '''

    ro.r(R_command)
    ro.r('saveNetwork(network = a ,file = "%s.html")'%filename)

```


```python
# make the html files

DrawNetGraph(Double_Kill, "2_double")
DrawNetGraph(Triple_Kill, "3_triple")
DrawNetGraph(Quadra_Kill, '4_quadra')
DrawNetGraph(Penta_Kill, "5_penta")
DrawNetGraph(Rampage, "6_rampage")
DrawNetGraph(Godlike, "7_godlike")

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```

### Find the index


```python
l = [2,3,5,4,8,12]

a =2


```


```python
l.index(2)
```




    0




```python
l.index(12)
```




    5




```python
[ l.index(i) for i in l]
```




    [0, 1, 2, 3, 4, 5]




```python
def index(a, l):
    return l.index(a)
```


```python
l = list(Nodes[0])
l.index(8)
```




    8




```python
l[:10]
```




    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]




```python

```


```python

```

# Good Game


```python

```


```python

```


```python

```


```python

```


```python

```

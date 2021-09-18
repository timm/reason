import re, random

from functools import cmp_to_key as by 

class o:
  def __init__(i, **d)  : i.__dict__.update(d)
  def __repr__(i) : return "{"+ ', '.join(
    [f":{k} {v}" for k, v in i.__dict__.items() if k[0] != "_"])+"}"
class Col(o):
  def __init__(i,at,s): 
    i.n,i.at,i.name = 0,at,s
    i.w = -1 if "-" in s else 1 

  def add(i,x,n=1):
    if "?" != x:
      i.n += 1; x = i.add1(x,n)
    return x

  def add1(i,x,n): return x

  def dist(i,x,y): return 1 if x==y=="?" else i.dist1(x,y)

class Num(Col):
  def __init__(i,*l,**kw): 
    super().__init__(*l, **kw)
    i.lo, i.hi = 1E32, -1E32

  def add1(i,x,n):
    x = float(x)
    if x > i.hi: i.hi = x
    if x < i.lo: i.lo = x
    return x

  def dist1(i,x,y):
    if x=="?": 
      y= i.norm(y); x= 0 if y > .5 else 1
    elif y=="?": 
      x= i.norm(x); y= 0 if x > .5 else 1
    else:
      x,y = i.norm(x), i.norm(y)
    return abs(x - y)

  def norm(i,x):
    return 0 if abs(i.hi - i.lo) < 1E-31 else (x - i.lo)/(i.hi - i.lo)

class Sym(Col):
  def dist1(i,x,y): return 0 if x==y else 1

class Sample(o):
  def __init__(i,inits=[]): 
    i.x, i.y, i.all, i.rows = [],[],[],[]
    [i.add(x) for x in inits]
  def add(i,lst):
    if i.all: 
      lst = [col.add(x) for col,x in zip(i.all,lst)]
      i.rows += [Row(i, lst)]
    else: 
      for n,x in enumerate(lst):
        z = Skip if "?" in x else (Num if x[0].isupper() else Sym)
        z = z(n,x)
        i.all += [z]
        if "?" not in x:
          (i.y if "+" in x or "-" in  x or "!" in x else i.x).append(z)

class Row(o):
  def __init__(i, s,lst,): i._sample, i.cells = s, lst
  def dist(i,j):
    d,cols = 1E-31, i._sample.x
    for col in cols:
      tmp = col.dist(i.cells[col.at], j.cells[col.at])
      d  += tmp**2
    return (d/len(cols))**(1/2)
  def mid(i,j):
    out = [None] * len(i.cells)
    for col,x,y in zip(i._sample.all, i.rows, j.rows):

def first(lst): return lst[0]
def shuffle(lst): random.shuffle(lst); return lst

def csv(file, sep=",", dull=r'([\n\t\r ]|#.*)'):
  def atom(x):
    if x=="?": return x
    try: return float(x)
    except Exception:  return x
  with open(file) as fp:
    for s in fp:
      s = re.sub(dull,"",s)
      if s: yield [atom(x) for x in s.split(sep)]

def gac(rows):
  row1,*rows = rows
  tmp = sorted(rows,key=lambda row2:row1.dist(row2))[2]
  row1,row2, tmp[:2]

random.seed(1)
s=Sample()
for row in csv("../data/auto93.csv"):
  s.add(row)
for row in shuffle(s.rows)[:10]:
  tmp = sorted(s.rows, key=lambda z: row.dist(z))
  print("")
  print(row.cells)
  print(tmp[1].cells, row.dist(tmp[1]))
  print(tmp[-1].cells,row.dist(tmp[-1]))

from gurobipy import *

### Inicialización ###
K = range(4)
R = range(19)
C_k = [13.97, 13.97, 23.74, 23.74]
D_r = [113.45, 92.91, 70.64, 46.42,
       97.16, 127.78, 102.74, 44.64,
       113.45, 93, 70.64, 46.43,
       44.8, 90.25, 73.17,
       113.45, 93, 70.6, 44.64]

### Modelo ###
m = Model("Asignacion")
x = dict()

for k in K:
    for r in R:
        x[k, r] = m.addVar(vtype=GRB.BINARY, lb=0, ub=1,
                           name="{0},{1}".format(k, r))

m.update()

m.setObjective(quicksum(D_r[r]*x[k, r]/C_k[k]
                        for k in K for r in R), GRB.MINIMIZE)
m.update()

# cada ruta tiene un camion
m.addConstrs(quicksum(x[k, r] for k in K) == 1 for r in R)

for k in K:
    for R_d in [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14], [15, 16, 17, 18]]:
        m.addConstr(quicksum(x[k, r] for r in R_d) <= 1)

m.update()

m.optimize()
print(m.getObjective())
solucion = []

for v in m.getVars():
    if v.x > 0.0000001:
        solucion.append(v.varName.split(","))
sol = open("solucion.txt", "w")
dia = [[i for i in range(4)], [i for i in range(4)], [i for i in range(4)], [
    i for i in range(3)], [i for i in range(4)]]


def norm(n):
    if n in [0, 1, 2, 3]:
        return n
    elif n in [4, 5, 6, 7]:
        return n - 4
    elif n in [8, 9, 10, 11]:
        return n - 8
    elif n in [12, 13, 14]:
        return n - 12
    else:
        return n - 15


for s in solucion:
    if s[1] == "15":
        dia[-1][0] = str(int(s[0])+1)
        continue
    dia[int(s[1])//4][norm(int(s[1]))] = str(int(s[0])+1)

for d in dia:
    sol.write("\t".join(d) + "\n")
sol.close()

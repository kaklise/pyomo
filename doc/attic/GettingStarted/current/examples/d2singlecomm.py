# d2singlecomm.py - double indexes instead of an Arc set
# equivelant to singlecomm.py
from pyomo.environ import *

model = AbstractModel()

model.Nodes = Set()

model.Flow = Var(model.Nodes, model.Nodes, domain=NonNegativeReals)
model.FlowCost = Param(model.Nodes, model.Nodes, default = 0.0)

model.Demand = Param(model.Nodes)
model.Supply = Param(model.Nodes)

def Obj_rule(model):
    return sum_product(model.FlowCost, model.Flow)
model.Obj = Objective(rule=Obj_rule, sense=minimize)

def FlowBalance_rule(model, node):
    return model.Supply[node] \
     + sum(model.Flow[i, node] for i in model.Nodes) \
     - model.Demand[node] \
     - sum(model.Flow[node, j] for j in model.Nodes) \
     == 0
model.FlowBalance = Constraint(model.Nodes, rule=FlowBalance_rule)

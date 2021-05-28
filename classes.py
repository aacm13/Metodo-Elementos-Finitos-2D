from enum import Enum

Lines = Enum('Lines', 'NOLINE SINGLELINE DOUBLELINE')
Modes = Enum ('Modes', 'NOMODE INT_FLOAT INT_INT_INT')
Parameters = Enum('Parameters', 'ELEMENT_LENGTH THERMAL_CONDUCTIVITY HEAT_SOURCE')
Sizes = Enum('Sizes', 'NODES ELEMENTS DIRICHLET NEUMANN')

class item:
    id = 0
    x = 0.0
    node1 = 1
    node2 = 1
    value = 0.0

    def getId(self):
        return self.id
    
    def getX(self):
        return self.x
    
    def getNode1(self):
        return self.node1
    
    def getNode2(self):
        return self.node2
    
    def getValue(self):
        return self.value



class Node (item):

    def sentIntFloat(self, iden, x_coo):
        item.id = iden
        item.x = x_coo

    def sentIntIntInt(self, n1, n2, n3):
        pass

class Element(item):
    
    def sentIntFloat(self, n1, r):
        pass
    
    def sentIntIntInt(self, iden, firstN, secondN):
        item.id = iden
        item.node1 = firstN
        item.node2 = secondN

class Condition(item):
    
    def sentIntFloat(self, node_to_apply, prescribed_value):
        item.node1 = node_to_apply
        item.value = prescribed_value
    
    def sentIntIntInt(self, iden, firstN, secondN):
        pass

class Mesh:
    parameters = []
    sizes = []
    node_list = []
    element_list = []
    dirichlet_list = []
    neumann_list = []

    def setParameters(self, l, k, Q):
        
        self.parameters.insert(Parameters.ELEMENT_LENGTH.value -1,l)
        self.parameters.insert(Parameters.THERMAL_CONDUCTIVITY.value - 1, k)
        self.parameters.insert(Parameters.HEAT_SOURCE.value - 1, Q)
    
    def setSizes(self, nNodes, nElemts, nDirich, nNeumn):
      
        self.sizes.insert(0, nNodes)
        self.sizes.insert(1, nElemts)
        self.sizes.insert(2, nDirich)
        self.sizes.insert(3, nNeumn)
     

    def getSize(self, s):
        return self.sizes[s]

    def getParam(self, p):
        return self.parameters[p]

    def create(self):
        
        for i in range(self.sizes[0]):
            obj = Node()
            self.node_list.append(obj)
        
        for i in range(self.sizes[1]):
            obj = Element()
            self.element_list.append(obj)
        
        for i in range(self.sizes[2]):
            obj = Condition()
            self.dirichlet_list.append(obj)

        for i in range(self.sizes[3]):
            obj = Condition()
            self.neumann_list.append(obj)

        

    def getNodes(self):
        return self.node_list
    
    def getElements(self):
        return self.element_list

    def getDirichlet(self):
        return self.dirichlet_list

    def getNeumann(self):
        return self.neumann_list

    def getNode(self, i):
        return self.node_list[i]
    
    def getElement(self, i):
        return self.element_list[i]
    
    def getCondition(self, i, type):
        if(type == Sizes.DIRICHLET):
            return self.dirichlet_list[i]
        else:
            return self.neumann_list[i]
import classes
import mate
from math import sqrt

def showMatrix(kMatrix):
    for i in range(0,len(kMatrix[0])):
        print('[',end=" ")
        for j in range(0, len(kMatrix)):
            print(str(kMatrix[i][j]),end=" " )
        print("]")
        

def showKs(KsMatrix):
    for i in range(0, len(KsMatrix)):
        print("K del elemento " + str(i + 1) + ":\n")
        showMatrix(KsMatrix[i])
        print("************************************\n")

def showVector(v):
    print("[",end=" ")
    for i in range(0, len(v)):
        print(str(v[i]), end = " ")
    print("]",end=" ")

def showbs(bs):
    for i in range(0, len(bs)):
        print("b del elemento " + str(i+1) + ":")
        showVector(bs[i])
        print("\n****************************")

def calculateD(i, mesh):
    e = mesh.getElement(i)
    n1 = mesh.getNode(e.getNode1()-1)
    n2 = mesh.getNode(e.getNode2()-1)
    n3 = mesh.getNode(e.getNode3()-1)

    a = n2.getX()-n1.getX()
    b = n2.getY()-n1.getY()
    c = n3.getX()-n1.getX()
    d = n3.getY()-n1.getY()

    Dv = a*d - b*c

    return Dv

def calculateMag(v1, v2):
    a = pow(v1,2)
    b = pow(v2,2)
    result = a+b
    return sqrt(result)

def calculateArea(i, mesh):
    element = mesh.getElement(i)
    n1 = mesh.getNode(element.getNode1()-1)
    n2 = mesh.getNode(element.getNode2()-1)
    n3 = mesh.getNode(element.getNode3()-1)
    
    a = calculateMag(n2.getX()-n1.getX(), n2.getY()-n1.getY())
    b = calculateMag(n3.getX()-n2.getX(), n3.getY()-n2.getY())
    c = calculateMag(n3.getX()-n1.getX(), n3.getY()-n1.getY())

    s = (a+b+c)/2

    Av = sqrt(s*(s-a)*(s-b)*(s-c))
    return Av

def calculateA(i, matrix, mesh):
    e = mesh.getElement(i)
    n1 = mesh.getNode(e.getNode1()-1)
    n2 = mesh.getNode(e.getNode2()-1)
    n3 = mesh.getNode(e.getNode3()-1)

    matrix[0][0] = n3.getY()-n1.getY()
    matrix[0][1] = n1.getY()-n2.getY()
    matrix[1][0] = n1.getX()-n3.getX()
    matrix[1][1] = n2.getX()-n1.getX()

def calculateB(B):
    B[0][0] = -1
    B[0][1] = 1
    B[0][2] = 0
    B[1][0] = -1
    B[1][1] = 0
    B[1][2] = 1

def createK(element, mesh):    
    k = m.getParameter(c.Parameters.THERMAL_CONDUCTIVITY.value)
    Av = []
    Bv = []
    Kv = []
    Bt = []
    At = []

    Dv = calculateD(element, m)
    Ae = calculateArea(element, m)

    mt.ZeroesF(Av,2)
    mt.ZeroesS(Bv,2,3)
    calculateA(element, Av, m)
    calculateB(Bv)
    mate.transpose(Av, At)
    mate.transpose(Bv, Bt)

    mate.productRealMatrix(k*Ae/(Dv*Dv),mt.productMatrixMatrix(Bt,mt.productMatrixMatrix(At,mt.productMatrixMatrix(Av,Bv,2,2,3),2,2,3),3,2,3),Kv)

    return Kv

def calculateJ(i, mesh):
    e = mesh.getElement(i)
    n1 = mesh.getNode(e.getNode1()-1)
    n2 = mesh.getNode(e.getNode2()-1)
    n3 = mesh.getNode(e.getNode3()-1)

    a = n2.getX()-n1.getX()
    b = n3.getX()-n1.getX()
    c = n2.getY()-n1.getY()
    d = n3.getY()-n1.getY()

    l = a*d -b*c

    return l

def createB(element, mesh):
    b = []
    
    
    Q = mesh.getParam(classes.Parameters.HEAT_SOURCE.value - 1)
    l = calculateJ(element, mesh)
    
    b.append( Q*l/6)
    b.append( Q*l/6)
    b.append( Q*l/6)

    return b

def createLocalSystems(mesh, localKs, localBs):
    
    for i in range(0, mesh.getSize(classes.Sizes.ELEMENTS.value - 1)):
        localKs.append(createK(i, mesh))
        localBs.append(createB(i, mesh))

def kAssemble(element, localK, matrixK):
    index1 = element.getNode1() - 1
    index2 = element.getNode2() - 1
    index3 = element.getNode3()-1
   
    matrixK[index1][index1] += localK[0][0]
    matrixK[index1][index2] += localK[0][1]
    matrixK[index1][index3] += localK[0][2]
    matrixK[index2][index1] += localK[1][0]
    matrixK[index2][index2] += localK[1][1]
    matrixK[index2][index3] += localK[1][2]
    matrixK[index3][index1] += localK[2][0]
    matrixK[index3][index2] += localK[2][1]
    matrixK[index3][index3] += localK[2][1]

def bAssemble(element, localB, vectorB):
    index1 = element.getNode1() - 1
    index2 = element.getNode2() - 1
    index3 = element.getNode3()-1

    vectorB[index1] += localB[0]
    vectorB[index2] += localB[1]
    vectotB[index3] += localb[2]

def assembly(mesh, localKs, localBs, K, b):
    for i in range(0, mesh.getSize(classes.Sizes.ELEMENTS.value)):
        element = mesh.getElement(i)
        kAssemble(element, localKs[i], K)
        bAssemble(element, localBs[i], b)


def applyNeumann(mesh, b):
    for i in range(0, mesh.getSize(classes.Sizes.NEUMANN.value)):

        condition = mesh.getCondition(i, classes.Sizes.NEUMANN.value)
        b[condition.getNode1()-1] += condition.getValue()

def applyDirichlet(mesh, K, b):
    for i in range(0, mesh.getSize(classes.Sizes.DIRICHLET.value)):
        
        condition = mesh.getCondition(i, classes.Sizes.DIRICHLET.value)
        index = condition.getNode1() - 1
        
        K.pop(index)
        
        b.pop(index)

        for row in range(0, len(K)):
            
            cell = K[row][index]
            K[row].pop(index)
            b[row] = b[row] + (-1 * condition.getValue() * cell)

def calc(K, b, T):
    Kinversa = []
    mate.inverseMatrix(K, Kinversa)
    mate.productMatrixVector(K, b, T)
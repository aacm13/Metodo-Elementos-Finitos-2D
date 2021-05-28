import classes
import mate

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


def createK(element, mesh):    

    K = []
    row1 = []
    row2 = []

    k = mesh.getParam(classes.Parameters.THERMAL_CONDUCTIVITY.value - 1)
    l = mesh.getParam(classes.Parameters.ELEMENT_LENGTH.value - 1)

    row1.append(k/l)
    row1.append(-k/l)

    row2.append(-k/l)
    row2.append(k/l)

    K.append(row1)
    K.append(row2)

    return K



def createB(element, mesh):
    b = []
    
    
    Q = mesh.getParam(classes.Parameters.HEAT_SOURCE.value - 1)
    l = mesh.getParam(classes.Parameters.ELEMENT_LENGTH.value - 1)
    
    b.append( Q*l/2)
    b.append( Q*l/2)

    return b

def createLocalSystems(mesh, localKs, localBs):
    
    for i in range(0, mesh.getSize(classes.Sizes.ELEMENTS.value - 1)):
        localKs.append(createK(i, mesh))
        localBs.append(createB(i, mesh))

def kAssemble(element, localK, matrixK):
    index1 = element.getNode1() - 1
    index2 = element.getNode2() - 1
   
    matrixK[index1:index1] += localK[0:1]
    matrixK[index1:index2] += localK[0:2]
    matrixK[index2:index1] += localK[:1]
    matrixK[index2:index1] += localK[1:2]

def bAssemble(element, localB, vectorB):
    index1 = element.getNode1() - 1
    index2 = element.getNode2() - 1

    vectorB[index1] += localB[0]
    vectorB[index2] += localB[1]

def assembly(mesh, localKs, localBs, K, b):
    for i in range(0, mesh.getSize(1)):
        element = mesh.getElement(i)
        kAssemble(element, localKs[i], K)
        bAssemble(element, localBs[i], b)


def applyNeumann(mesh, b):
    for i in range(0, mesh.getSize(3)):

        condition = mesh.getCondition(i, classes.Sizes.NEUMANN)
        b[condition.getNode1()-1] += condition.getValue()

def applyDirichlet(mesh, K, b):
    for i in range(0, mesh.getSize(2)):
        
        condition = mesh.getCondition(i, classes.Sizes.DIRICHLET)
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
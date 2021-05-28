import sys

def zeroes(matrix, n):
    for i in range(0, n):
        row = [0.0] * n
        matrix.append(row)

def zeroes(vector, n):
    for i in range(0, n):
        vector.append(0.0)

def copyMatrix(matrix, copy):
    zeroes(copy, len(matrix))
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            copy[i][j] = matrix[i][j]

def productMatrixVector(matrix, vector, result):
    for fila in range(0, len(matrix)):
        cell = 0.0
        for celda in range(0, len(vector)):
            cell += matrix[fila][celda] * vector[celda]

        result[fila] += cell

def productRealMatrix(real, matrix, result):
    zeroes(result, len(matrix))
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            result[i][j] = real * matrix[i][j]

def getMinor(matrix, i, j):
    del matrix[i]
    for i in range(0, len(matrix)):
        matrix[i].remove(matrix[j])

def determinant(matrix):
    if(len(matrix) == 1):
        return matrix[0][0] 
    else:
        det = 0.0
        for i in range(0, len(matrix[0])):
            minor = []
            copyMatrix(matrix, minor)
            
            getMinor(minor, 0, i)
            det += pow(-1, i) * matrix[0][i] * determinant(minor)
    
        return det

def cofactors(matrix, cofactors):
    zeroes(cofactors, len(matrix))

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            minor = [0] * 1
            copyMatrix(matrix, minor)
            getMinor(minor, i, j)

            cofactors[i][j] =  pow(-1, i + j) * determinant(minor)

def transpose(matrix, transpose):
    
    zeroes(transpose, len(matrix))

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            transpose[j][i] = matrix[i][j]

def inverseMatrix(matrix, inverse):
    Cof = [0] * 1
    Adj = [0] * 1

    det = determinant(matrix)
    if(det == 0):
        sys.exit("Matriz no es invertible")
    cofactors(matrix, Cof)
    transpose(Cof, Adj)
    productRealMatrix(1/det, Adj, inverse)
    
import mate
import classes
import tools
import shows


def main():
    localKs = []
    localBs = []

    matrix_K = []
    vector_b = []
    vector_T = []
    
    print("------------------SIDEQUEST:POLYGLOT------------------")

    Mesh = classes.Mesh()
    tools.readStuff(Mesh)

    
    shows.createLocalSystems(Mesh, localKs, localBs)

    mate.zeroes(matrix_K, Mesh.getSize(classes.Sizes.NODES.value - 1))
    mate.zeroes(vector_b, Mesh.getSize(classes.Sizes.NODES.value - 1))

    shows.assembly(Mesh, localKs, localBs, matrix_K, vector_b)
    shows.applyNeumann(Mesh, vector_b)
    shows.applyDirichlet(Mesh, matrix_K, vector_b)
    
    mate.zeroes(vector_T, len(vector_b))

    shows.calc(matrix_K, vector_b, vector_T)

    print("Respuesta: ")
    shows.showVector(vector_T)

main()


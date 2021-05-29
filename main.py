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
    filename = "test"
    tools.readStuff(Mesh, filename)

    
    shows.createLocalSystems(Mesh, localKs, localBs)

    mate.zeroesF(matrix_K, Mesh.getSize(classes.Sizes.NODES.value))
    mate.zeroesT(vector_b, Mesh.getSize(classes.Sizes.NODES.value))

    shows.assembly(Mesh, localKs, localBs, matrix_K, vector_b)
    shows.applyNeumann(Mesh, vector_b)
    shows.applyDirichlet(Mesh, matrix_K, vector_b)
    
    mate.zeroesT(vector_T, len(vector_b))

    shows.calc(matrix_K, vector_b, vector_T)

    print("Respuesta: ")
    shows.showVector(vector_T)
    tools.writeResults(Mesh, vector_T, filename)

main()


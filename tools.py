import classes

def getData(file, nlines, n, mode, item_list):
    line = file.readline()
    if nlines == classes.Lines.DOUBLELINE.value : 
        line = file.readline()
        line = file.readline()
    for i in range(n):
        if mode == classes.Modes.INT_FLOAT.value:
            condition = classes.Condition()
            line = file.readline()
            words = []
            for word in line.split():
                words.append(word)
            condition.setValues(classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value, int(words[0]), classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value, float(words[1]))
            item_list.append(condition) 

        if mode == classes.Modes.INT_FLOAT_FLOAT.value:
            node = classes.Node()
            line = file.readline()
            words = []
            for word in line.split():
                words.append(word)
            node.setValues(int(words[0]),float(words[1]), float(words[2]), classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value)
            item_list.append(node)

        if mode == classes.Modes.INT_INT_INT_INT.value:
            element = classes.Element()
            line = file.readline()
            words=[]
            for word in line.split():
                words.append(word)
            element.setValues(int(words[0]), classes.Indicators.NOTHING.value, classes.Indicators.NOTHING.value, int(words[1]), int(words[2]), int(words[3]), classes.Indicators.NOTHING.value)
            item_list.append(element)

def Conditions(n, list, index):
    for i in range(n):
        index.insert(i, list[i].getNode1())
    
    for i in range(n-1):
        pivot = list[i].getNode1()
        for j in range(n):
            if list[j].getNode1() > pivot :
                list[j].setNode1(list[j].getNode1() - 1)

def Extension(newfilename, filename, extension):
    for i in filename:
        newfilename += i
    for i in extension:
        newfilename += i
    return newfilename

def readStuff(Mesh, filename):
    inputfilename = ''
    inputfilename = addExtension(inputfilename, filename, '.dat')
    infile = open(inputfilename, 'r')

    wordsline = []
    line1 = infile.readline()
    line2 = infile.readline()
    
    for word in line1.split():
        wordsline.append(word)
    
    k = float(wordsline[0])
    q = float(wordsline[1])

    wordsline = []
    for word in line2.split():
        wordsline.append(word)

    nnodes = int(wordsline[0])
    neltos = int(wordsline[1])
    ndirich = int(wordsline[2])
    nneu = int(wordsline[3])

    Mesh.setParameters(k, q)
    Mesh.setSizes(nnodes, neltos, ndirich, nneu)
    Mesh.createData()

    infile.readline()
    getData(infile, classes.Lines.SINGLELINE.value, nnodes, classes.Modes.INT_FLOAT_FLOAT.value, m.getNodes())
    getData(infile,classes.Lines.DOUBLELINE.value, neltos, classes.Modes.INT_INT_INT_INT.value, m.getElements())
    getData(infile, classes.Lines.DOUBLELINE.value, ndirich, classes.Modes.INT_FLOAT.value, m.getDirichlet())
    getData(infile, classes.Lines.DOUBLELINE.value, nneu, classes.Modes.INT_FLOAT.value, m.getNeumann())

    infile.close()
    Conditions(ndirich, Mesh.getDirichlet(), Mesh.getDirichletIndex())


def findIndex(vector , s, arr):
    for i in range(s):
        if arr[i] == vector : return True
    return False

def writeResults(Mesh, T, filename):
    outputfilename = ''
    dirich_index = Mesh.getDirichletindex()
    dirich = Mesh.getDirichlet()

    outputfilename = addExtension(outputfilename, filename, '.post.res')
    infile = open(outputfilename,"w+")

    infile.write("archivos resultado\n")
    infile.write("Resultado \"Temperatura\" \"Cargar caso 1\" 1 Escalar en Nodes\nNombreComponentes \"T\"\Valores\n")

    posT = 0
    posD = 0
    n = Mesh.getSize(c.Sizes.NODES.value)
    nd = Mesh.getSize(c.Sizes.DIRICHLET.value)

    for i in range(n):
        if findIndex( i+1, nd, dirich_index):
            infile.write(str(i+1) + " " + str(dirich[posD].getValue()) + "\n")
            posD += 1
        else:
            infile.write(str(i+1) + " " + str(T[posT]) + "\n")
            posT += 1
    
    infile.write("End values\n")

    infile.close()

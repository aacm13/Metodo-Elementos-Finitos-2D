import classes

def getData(file, nlines, n, mode, item_list):
    file.readline()
    if(nlines == classes.Lines.DOUBLELINE):
        file.readline()

    index = 0
    limit = n
    for f in file:
        
            if(mode == classes.Modes.INT_FLOAT and limit > 0):
                row = f.split()
                if(len(row) > 1):
                    e = int(row[0])
                    r = float(row[1])

                    limit -= 1
                    item_list[index].sentIntFloat(e, r)
                                
                    index += 1
    
            elif(mode == classes.Modes.INT_INT_INT and limit > 0):
                
                row = f.split()
                if(len(row) > 1):
                    e1 = int(row[0])
                    e2 = int(row[1])
                    e3 = int(row[2])
                    limit -= 1
                    item_list[index].sentIntIntInt(e1, e2, e3)
                    index += 1


def readStuff(Mesh):
    filename = ""
    flag = True
   
    while(flag):
        try:
            filename = input("Nombre del archivo con datos:\n")
            file = open(filename)
            if(file):
                cont = 0
                for line in file:
                    file_line = line.split()                  

                    if(cont == 0):
                        l = float(file_line[0])
                        k = float(file_line[1])
                        Q = float(file_line[2])

                    if(cont == 1):
                        nNodes = int(file_line[0])
                        nElemts = int(file_line[1])
                        nDirich = int(file_line[2])
                        nNeumn = int(file_line[3])
                        
                    if cont > 1:
                        break       
                    cont += 1             

                Mesh.setParameters(l,k,Q)
                
                Mesh.setSizes(nNodes, nElemts, nDirich, nNeumn)
                Mesh.create()

                
                getData(file, classes.Lines.SINGLELINE, nNodes, classes.Modes.INT_FLOAT, Mesh.getNodes())
                
                getData(file, classes.Lines.DOUBLELINE, nElemts, classes.Modes.INT_INT_INT.value, Mesh.getElements())
                
                getData(file, classes.Lines.DOUBLELINE, nDirich, classes.Modes.INT_FLOAT, Mesh.getDirichlet())
                getData(file, classes.Lines.DOUBLELINE, nNeumn, classes.Modes.INT_FLOAT, Mesh.getNeumann())

                file.close()
                flag = False

        except (FileNotFoundError):
            print("File not found")



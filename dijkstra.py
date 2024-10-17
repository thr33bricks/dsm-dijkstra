LIMIT = 10000
SHOW_GRAPHICS = True

if SHOW_GRAPHICS:
    import networkx as nx
    import matplotlib.pyplot as plt

# TEST CASE:
# 0 5 3 7 0 0 0
# 5 0 1 6 12 0 0
# 3 1 0 5 0 6 0
# 7 6 5 0 4 6 0
# 0 12 0 4 0 3 3
# 0 0 6 6 3 0 4
# 0 0 0 0 3 4 0

def main():
    mat = []
    solMat = []
    start = 0
    end = 0

    print("Enter matrix row by row.")
    print(f"Enter weights 0-{LIMIT - 1}")
    print("Values should be separated by single whitespaces!\n")

    #Read matrix
    firstLineArr = list(map(int,input().split()))

    matDim = len(firstLineArr)
    mat.append(firstLineArr)

    for i in range(matDim - 1):
        lineArr = list(map(int,input().split()))
        mat.append(lineArr)
    
    #Verify matrix
    if not verifyMat(mat):
        print("\nWrong input!\n")
        return

    printMat(mat)

    #Read start end nodes
    print("\nEnter start and end node separated by a single whitespace.")
    startEndArr = list(map(int,input().split()))

    #Verify and save start end nodes
    if not verifyStartEndNodes(startEndArr, matDim):
        print("\nWrong input!\n")
        return
    start = startEndArr[0] - 1
    end = startEndArr[1] - 1

    print("=====================================")

    #Init start solution matrix
    solMat = initSolMat(matDim, start)

    print("\nSTART:")
    printSolMat(solMat)

    #Solution
    for i in range(matDim):
        minNode, curPathWeigh = getMinNode(solMat)
        for j in range(matDim):
            if mat[minNode][j] > 0 and mat[minNode][j] + curPathWeigh < solMat[j][1]:
                solMat[j][1] = mat[minNode][j] + curPathWeigh
                solMat[j][2] = minNode

        solMat[minNode][0] = 1
        print(f"\nSTEP {i+1}:")
        printSolMat(solMat, minNode)

    print("\nFINAL:")
    printSolMat(solMat)

    print("=====================================")

    printPath(solMat, start, end)

    if SHOW_GRAPHICS:
        showGraph(mat)

def verifyMat(mat):
    matDim = len(mat)

    #Verify size
    for i in range(matDim):
        if len(mat[i]) != matDim:
            return False
    
    #Verify diagonal
    for i in range(matDim):
        if mat[i][i] != 0:
            return False
    
    #Verify values
    for i in range(matDim):
        for j in range(matDim):
            if mat[i][j] > LIMIT - 1 or mat[i][j] < 0 or mat[i][j] != mat[j][i]:
                return False
    return True

def verifyStartEndNodes(startEndArr, matDim):
    if len(startEndArr) != 2:
        return False
    if startEndArr[0] < 1 or startEndArr[0] > matDim or \
       startEndArr[1] < 1 or startEndArr[1] > matDim:
        return False
    return True


def printMat(mat):
    matDim = len(mat)

    print("\nMatrix:")

    #First line
    print("\t", end="")
    for i in range(1, matDim + 1):
        print(f"v{i}\t", end="")
    print("")

    #All other lines
    for i in range(matDim):
        print(f"v{i+1}\t", end="")

        for j in range(matDim):
            print(f"{mat[i][j]}\t", end="")
        print()

def initSolMat(len, start):
    solMat = []
    for i in range(len):
        val = 0 if i == start else LIMIT
        solMat.append([0, val, -1])

    return solMat

def printSolMat(solMat, currNode=-1):
    le = len(solMat)

    print("Node\tV\tD\tP")

    for i in range(le):
        print(f"{i+1}\t", end="")

        for j in range(3):
            val = "inf" if solMat[i][j] == LIMIT else solMat[i][j]
            if j == 2 and val != -1:
                val = f"v{val+1}"
            print(f"{val}\t", end="")

        if i == currNode:
            print(" <--", end="")
        print()

def getMinNode(solMat):
    curMin = LIMIT + 1
    curInd = 0
    for i in range(len(solMat)):
        if solMat[i][0] == 0 and solMat[i][1] < curMin:
            curInd = i
            curMin = solMat[i][1]
    return curInd, curMin

def printPath(solMat, start, currNode):
    pathLen = solMat[currNode][1]
    path = []

    while solMat[currNode][2] != -1:
        path.append(currNode)
        currNode = solMat[currNode][2]
    path.append(currNode)
    path.reverse()

    if(currNode != start):
        print("\nThere is no path between selected points!")
        return

    print("\nShortest path: " + "=>".join(f"v{str(e+1)}" for e in path))
    print(f"Length: {pathLen}")

def showGraph(mat):
    G = nx.Graph()

    #Convert matrix to edges with weights
    for i in range(len(mat)):
        for j in range(i+1, len(mat)):
            w = mat[i][j]
            if w != 0 and i != j:
                G.add_edge(str(i+1), str(j+1), weight=w)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.get_current_fig_manager()\
       .set_window_title("Graph Visualization with weights | Ruse University")
    plt.show()

if __name__ == "__main__":
    main()

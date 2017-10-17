from prettytable import PrettyTable
from copy import deepcopy
import visualization
import astar
import copy

class nn():

    class Nonogram():
        dimensions = None
        state = None
        rows = []
        cols = []
        fScore = 0
        gScore = 0
        hScore = 0

    class Row():
        constraints = []
        domain = []

    class Col():
        constraints = []
        domain = []

    #get scenario from file provided in folder 'scenarios'
    def get_scenarioFromFile(filename):
        #read file
        f = open('./scenarios/' + filename, 'r')
        split_list = f.read().split('\n')

        #add dimensions of nonogram
        dimensions = []
        for number in split_list.pop(0).split():
            if len(number) > 0:
                dimensions.append(int(number))
        print ("Dimensions: ", dimensions)

        #add constraint for rows
        rowCons = []
        for line in split_list[:dimensions[1]]:
            row = []
            for number in line.split():
                row.append(int(number))
            rowCons.append(row)
        #reverse row specs as they start bottomleft in scenario
        rowCons.reverse()
        print ("Row constraints: ", rowCons)

        #add constraints for columns
        colCons = []
        for line in split_list[dimensions[1]:]:
            col = []
            for number in line.split():
                col.append(int(number))
            if len(col) > 0:
                colCons.append(col)
        print ("Col constraints: ", colCons)

        return dimensions, rowCons, colCons

    #add Col and Row classes to initial Nonogram class
    #add domains of Col and Row
    def get_initialNonogram(dimensions, rowCons, colCons):
        nonogram = nn.Nonogram()
        nonogram.dimensions = dimensions

        #add Row objects to nonogram
        for index in range(dimensions[1]):
            newRow = nn.Row()
            newRow.constraints = []
            newRow.constraints.append(rowCons[index])
            nonogram.rows.append(newRow)

        #add Col objects to nonogram
        for index in range(dimensions[0]):
            newCol = nn.Col()
            newCol.constraints = []
            newCol.constraints.append(colCons[index])
            nonogram.cols.append(newCol)

        #make empty state
        state = []
        for i in range(dimensions[1]):
            row = [' '] * dimensions[0]
            state.append(row)
        nonogram.state = state

        #get row domains
        for rowIndex in range(dimensions[1]):
            nonogram.rows[rowIndex].domains = nn.get_domains(nonogram.rows[rowIndex].constraints[0], nonogram.dimensions[0])

        #get column domains
        for colIndex in range(dimensions[0]):
            nonogram.cols[colIndex].domains = nn.get_domains(nonogram.cols[colIndex].constraints[0], nonogram.dimensions[1])

        return nonogram

    #make a true new copy of nonogram object
    def get_newNonogram(nonogram):
        newNonogram = deepcopy(nonogram)
        newNonogram.state = deepcopy(nonogram.state)
        newNonogram.rows = deepcopy(nonogram.rows)
        newNonogram.cols = deepcopy(nonogram.cols)
        newNonogram.fScore = deepcopy(nonogram.fScore)
        newNonogram.gScore = deepcopy(nonogram.gScore)
        newNonogram.hScore = deepcopy(nonogram.hScore)
        return newNonogram

    #filter out domains not coherent with row domains
    def filterDomains(nonogram):
        newNonogram = nn.get_newNonogram(nonogram)
        isDone = True
        for rowIndex in range(len(newNonogram.rows)):
            newRowDomains = []
            rowDomains = newNonogram.rows[rowIndex].domains
            rowOk = False
            for rowDomainIndex, rowDomain in enumerate(rowDomains):
                rowDomainOk = True
                for i in range(len(rowDomain)):
                    columnDomainOk = False
                    for k in range(len(newNonogram.cols[i].domains)):
                        if rowDomain[i] == newNonogram.cols[i].domains[k][rowIndex]:
                            columnDomainOk = True
                    if not columnDomainOk:
                        rowDomainOk = False
                if rowDomainOk:
                    rowOk = True
                    newRowDomains.append(rowDomain)
                else:
                    isDone = False
                    print ("Filtering out domain...")
                    print (rowDomain)
                    continue
            newNonogram.rows[rowIndex].domains = newRowDomains
            print (newRowDomains)
            if not rowOk:
                print ("row not OK: ", rowIndex)
                return newNonogram, False

        return newNonogram, isDone

    #calculate heuristic score based on total row domains
    def get_hScore(nonogram):
        totalDomains = 0
        for rowIndex in range(len(nonogram.rows)):
            totalDomains += len(nonogram.rows[rowIndex].domains) - 1
        return totalDomains

    #find successors of state
    def get_successors(nonogram):
        successors = []
        min_rowDomainIndex = 0
        min_domain = 10000000000000

        #choose row with the least domains
        for rowIndex, row in enumerate(nonogram.rows):
            if len(row.domains) < 1:
                return []
            if len(row.domains) == 1:
                nonogram.state[rowIndex] = row.domains[0]
            if len(nonogram.rows[rowIndex].domains) < min_domain and len(row.domains) > 1:
                min_rowDomainIndex = rowIndex
                min_domain = len(row.domains)
        rowIndex = min_rowDomainIndex

        #check for abnormalities
        if rowIndex > nonogram.dimensions[0]:
            return []
        if len(nonogram.rows[rowIndex].domains) < 1:
            return []
        for d in nonogram.rows[rowIndex].domains:
            if 'X' not in d:
                return []

        #find successors and revise them before filtering out their domains
        for rowDomain in nonogram.rows[rowIndex].domains:
            print ("getting successor...")
            newNonogram = nn.get_newNonogram(nonogram)
            newNonogram.state[rowIndex] = rowDomain
            newNonogram.rows[rowIndex].domains = [rowDomain]
            newNonogram, stateOk = nn.REVISE(newNonogram, rowIndex)
            newNonogram, stateOk = nn.filterDomains(newNonogram)
            successors.append(newNonogram)
        return successors

    #revise nonogram state by reducing domains
    def REVISE(nonogram, rowIndex):
        newNonogram = nn.get_newNonogram(nonogram)
        stateOk = True
        lastOkCol = 0
        for colIndex in range(newNonogram.dimensions[0]):
            colOk = False
            newColDomains = []
            for colDomainIndex, colDomain in enumerate(newNonogram.cols[colIndex].domains):
                colDomainOk = True
                #compare legal column entries to row entry
                if colDomain[rowIndex] != newNonogram.state[rowIndex][colIndex]:
                    colDomainOk = False
                if colDomainOk:
                    colOk = True
                    newColDomains.append(colDomain)
            if not colOk:
                stateOk = False
            newNonogram.cols[colIndex].domains = newColDomains
        return newNonogram, stateOk

    #check if state is goal
    def isGoal(nonogram):
        for rowIndex, row in enumerate(nonogram.rows):
            if len(nonogram.rows[rowIndex].domains) > 1:
                return False
        nn.display(nonogram, 500)
        newNonogram, isDone = nn.filterDomains(nonogram)
        if isDone:
            return True
        else:
            return False

    #calculate gScore
    def get_gScore(nonogram):
        return nonogram.gScore + 1

    #get all possible domains based on constraints
    def get_domains(constraints, dimension):
        #if no constraints, add empty row
        if len(constraints) == 0:
            row = []
            for x in range(dimension):
                row.append(' ')
            return [row]


        domains = []
        for startIndex in range(dimension - constraints[0] + 1):
            #find possible domains
            domain = []
            for x in range(startIndex):
                domain.append(' ')
            for x in range(startIndex, startIndex + constraints[0]):
                domain.append('X')
            x = startIndex + constraints[0]
            if x < dimension:
                domain.append(' ')
                x += 1
            #when done, add domain
            if x == dimension and len(constraints) == 0:
                domains.append(domain)
                break
            #add blocks recursively
            next_startIndex = x
            next_rows = nn.get_domains(constraints[1:len(constraints)], dimension - next_startIndex)
            for next_row in next_rows:
                next_domain = copy.deepcopy(domain)
                for x in range(next_startIndex, dimension):
                    next_domain.append(next_row[x-next_startIndex])
                domains.append(next_domain)
        return domains

    #get path with lowest fScore
    def getLowest_fScore(open):
        min_fScore = 10000000000000
        min_nonogramfScore = None
        index_score = 0
        min_indexScore = None
        for path in open:
            last_nonogram = path[-1]
            if last_nonogram.fScore < min_fScore:
                min_fScore = last_nonogram.fScore
                min_nonogramfScore = last_nonogram
                min_indexScore = index_score
            index_score += 1
        path = open.pop(min_indexScore)
        return path

    #print number of nodes generated, nodes expanded and nodes in path
    def print_resultStats(result):
        path = result[0]
        nodesExplored = result[1]
        nodesExpanded = result[2]
        print ("number of nodes generated:", nodesExplored)
        print ("Number of nodes expanded:", nodesExpanded)
        print ("Number of nodes in path:", len(path) - 1)

    #print nonogram state
    def print_nonogram(nonogram):
        p = PrettyTable()
        for row in nonogram.state:
           p.add_row(row)
        print (p.get_string(header=False, border=True, vrules=False, padding_width=0))

    #display nonogram state as text and visualization
    def display(nonogram, waitTime):
        nn.print_nonogram(nonogram)
        visualization.run(nonogram, waitTime)

#main function
def main(filename, display):
    dimensions, rowCons, colCons = nn.get_scenarioFromFile(filename)
    initialNonogram = nn.get_initialNonogram(dimensions, rowCons, colCons)
    if display:
        nn.print_nonogram(initialNonogram)
    #initialNonogram, stateOk = nn.filterDomains(initialNonogram)
    result = astar.run(initialNonogram, display, nn)
    if display:
        for nonogram in result[0]:
            nn.print_nonogram(nonogram)
            visualization.run(nonogram, 100)
    #print stats
    nn.print_resultStats(result)

#run main function with given parameters
main(filename='nono-chick.txt', display=True)

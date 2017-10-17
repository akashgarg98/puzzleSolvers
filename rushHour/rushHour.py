from copy import deepcopy
import visualization
from prettytable import PrettyTable
import bfs, dfs, astar

class rH():

    class Board():
        state = None
        vehicles = None
        gScore = 0
        hScore = 0
        fScore = 0

    class Vehicle():
        orientation = None
        coordinates = None
        size = None

    #get scenario from file provided in folder 'scenarios'
    def get_scenarioFromFile(filename):
        f = open('./scenarios/' + filename, 'r')
        scenario = []
        for line in f.read().split('\n'):
            quad = []
            for number in line.split(','):
                if len(number) > 0:
                    quad.append(int(number))
            if len(quad) > 0:
                scenario.append(quad)
        return scenario

    #get possible vehicle moves
    def get_possibleMoves(board):
        possibleMoves = []
        vehicleIndex = 0
        for vehicle in board.vehicles:
            vehicleMoves = rH.get_vehicleMoves(board, vehicle)
            possibleMoves.append(vehicleMoves)
            vehicleIndex += 1
        return possibleMoves

    #move vehicle and get updated board state
    def get_movedState(board, vehicleIndex, move):
        #will work regardless of size of vehicle
        vehicleCoordinates = board.vehicles[vehicleIndex].coordinates
        if move[0] > vehicleCoordinates[0][0]: #moves right
            vehicleCoordinates.append(move)
            #remove first coordinate entry
            del vehicleCoordinates[0]
        elif move[0] < vehicleCoordinates[0][0]: #moves left
            #add move as first coordinate entry
            vehicleCoordinates.insert(0, move)
            #remove last coordinate entry
            del vehicleCoordinates[-1]
        elif move[1] < vehicleCoordinates[0][1]: #moves up
            #add move as first coordinate entry
            vehicleCoordinates.insert(0, move)
            #remove last coordinate entry
            del vehicleCoordinates[-1]
        elif move[1] > vehicleCoordinates[0][1]: #moves down
            vehicleCoordinates.append(move)
            #remove first coordinate entry
            del vehicleCoordinates[0]
        board.vehicles[vehicleIndex].coordinate = vehicleCoordinates
        return rH.get_updatedBoardState(board)

    #find successors of node
    def get_successors(board):
        boardStates = []
        possibleMoves = rH.get_possibleMoves(board)
        for vehicleIndex, vehicleMoves in enumerate(possibleMoves):
            for move in vehicleMoves:
                new_state = rH.get_movedState(deepcopy(board), vehicleIndex, move)
                boardStates.append(new_state)
        return boardStates

    #calculate and return hScore
    def get_hScore(board):
        distanceToGoal = len(board.state[0]) - board.vehicles[0].size - board.vehicles[0].coordinates[-1][0]
        obstaclesToGoal = 0
        for spotToGoal in board.state[2][board.vehicles[0].coordinates[-1][0]:]:
            if spotToGoal != ' ':
                obstaclesToGoal += 1
        hScore = distanceToGoal + obstaclesToGoal
        return hScore

    #calculate and return gScore
    def get_gScore(board):
        gScore = board.gScore + 1
        return gScore

    #get path with lowest fScore
    def getLowest_fScore(open):
        min_fScore = 10000000000000
        min_boardfScore = None
        index_score = 0
        min_indexScore = None
        for path in open:
            last_board = path[-1]
            if last_board.fScore < min_fScore:
                min_fScore = last_board.fScore
                min_boardfScore = last_board
                min_indexScore = index_score
            index_score += 1
        path = open.pop(min_indexScore)
        return path

    #updates board.state based on board.vehicles
    def get_updatedBoardState(board):
        board.state = [[' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ']]
        index = 0
        for vehicle in board.vehicles:
            for coordinate in vehicle.coordinates:
                board.state[coordinate[1]][coordinate[0]] = str(index)
            index += 1
        return board

    #returns initial board with vehicles added
    def get_initialBoard(scenario):
        board = rH.Board()
        board.state = [[' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ']]
        board.vehicles = []
        for vehicle in scenario:
            board.vehicles.append(rH.addVehicle(vehicle))
        return rH.get_updatedBoardState(board)

    #add Vechicle object based on quads provided
    def addVehicle(quad):
        vehicle = rH.Vehicle()
        vehicle.orientation = quad[0]
        vehicle.x = quad[1]
        vehicle.y = quad[2]
        vehicle.size = quad[3]
        vehicle.coordinates = [[vehicle.x, vehicle.y]]
        if vehicle.orientation == 0: #lies horizontally
            vehicle.coordinates.append([vehicle.x + 1, vehicle.y])
            #if vehicle is truck, add coordinate
            if vehicle.size == 3:
                vehicle.coordinates.append([vehicle.x + 2, vehicle.y])
        elif vehicle.orientation == 1: #lies vertically
            vehicle.coordinates.append([vehicle.x, vehicle.y + 1])
            #if vehicle is truck, add coordinate
            if vehicle.size == 3:
                vehicle.coordinates.append([vehicle.x, vehicle.y + 2])
        return vehicle

    #get possible vehicle moves
    def get_vehicleMoves(board, vehicle):
        legal_moves = []
        potential_moves = []
        if vehicle.orientation == 0: #can move horizontally
            #right side of the vehicle
            potential_moves.append([vehicle.coordinates[-1][0] + 1, vehicle.coordinates[-1][1]]) #move right
            #left side of the vehicle
            potential_moves.append([vehicle.coordinates[0][0] - 1, vehicle.coordinates[0][1]]) #move left
        elif vehicle.orientation == 1: #can move vertically
            #highest point of vehicle
            potential_moves.append([vehicle.coordinates[0][0], vehicle.coordinates[0][1] - 1]) #move up
            #lowest point of vehicle
            potential_moves.append([vehicle.coordinates[-1][0], vehicle.coordinates[-1][1] + 1]) #move down
        for move in potential_moves:
            if rH.isLegalMove(board, vehicle, move[0], move[1]):
                legal_moves.append(move)
        return legal_moves

    #check if move is legal
    def isLegalMove(board, cur_vehicle, x, y):
        #check if move is inside grid
        if x in range(0,6) and y in range(0,6):
            #check if spot is available
            for vehicle in board.vehicles:
                for coordinate in vehicle.coordinates:
                    if coordinate[0] == x and coordinate[1] == y:
                        return False
            return True
        return False

    #check if board state is goal state
    def isGoal(board):
        goalCoordinate = [5, 2]
        for coordinate in board.vehicles[0].coordinates:
            if coordinate == goalCoordinate:
                return True

    #print number of moves and nodes explored
    def print_resultStats(result):
        path = result[0]
        tries = result[1]
        print("Number of moves: ", len(path) - 1)
        print("Number of nodes explored: ", tries)

    #print board state
    def print_board(board):
        p = PrettyTable()
        for row in board.state:
            p.add_row(row)
        print (p.get_string(header=False, border=True, vrules=False, padding_width=0))

    #display board state using Pygame script
    def display(board, waitTime):
        rH.print_board(board)
        visualization.run(board, waitTime)

#main function
def main(filename, algorithm, display):
    scenario = rH.get_scenarioFromFile(filename)
    initial_board = rH.get_initialBoard(scenario)
    if display:
        rH.print_board(initial_board)
    if algorithm == 'astar':
        result = astar.run(initial_board, display, rH)
    elif algorithm == 'bfs':
        result = bfs.run(initial_board, display, rH)
    elif algorithm == 'dfs':
        result = dfs.run(initial_board, display, rH)
    if display:
        for board in result[0]:
            rH.print_board(board)
            visualization.run(board, 100)
    #print stats
    rH.print_resultStats(result)

#run main function with given parameters
main(filename='medium-1.txt', algorithm='astar', display=True)

from __future__ import division
from __future__ import print_function
from math import fabs
from math import sqrt

class WindMap:
    def __init__(self, numOfRows, numOfColumns, altitude, rows):
        self.numOfRows = numOfRows
        self.numOfColumns = numOfColumns
        self.altitude = altitude
        self.rows = rows
        
    def getPositionAfterWindBlows(self, currentPosition):
        a, b = self.rows[currentPosition[0]][currentPosition[1]]
        return (currentPosition[0] + a, (currentPosition[1] + b) % self.numOfColumns)

class Balloon:
    def __init__(self, _id, row, column, altitude, windmaps, numberRows, numberColumns, coverageRadius):
        self._id = _id
        self.row = row
        self.column = column
        self.altitude = altitude
        self.isActive = True
        self.windmaps = windmaps
        self.numberRows = numberRows
        self.numberColumns = numberColumns
        self.coverageRadius = coverageRadius

    def copy(self):
        return Balloon(-1, self.row, self.column, self.altitude, self.windmaps, self.numberRows, self.numberColumns, self.coverageRadius)

    #if the target row and column are out of range, return False
    def getDistanceToTarget(self, targetRow, targetColumn):
        if targetRow < 0 or targetRow >= self.numberRows:
            return False
        if targetColumn < 0 or targetColumn > self.numberColumns:
            return False
        rowDistance = fabs(targetRow - self.row)
        columnAbsoluteDistance = fabs(targetColumn - self.column)
        columnDistance = min(columnAbsoluteDistance, self.numberColumns - columnAbsoluteDistance)
        distance = sqrt(rowDistance**2 + columnDistance**2)
        return distance    
    
    def find_nearest_target(self, targets):
        minDist = float("inf")
        minTarget = None
        for (tr,tc) in targets:
            dist = self.getDistanceToTarget(tr,tc)
            if tc >= self.column:
                if dist < minDist:
                    minDist = dist
                    minTarget = (tr,tc)
            else:
                if minTarget == None:
                    if dist < minDist:
                        minDist = dist
                        minTarget = (tr,tc)
        return minTarget

    def find_nearest_reachable_target(self, targets):
        queue = []
        for movement in self.get_possible_moves():
            new_balloon = self.copy()
            new_balloon.move(movement)
            if new_balloon.isActive:
                queue.append((movement, new_balloon))

        depth = 1
        while queue and depth < 3:
            depth += 1
            level = queue[:]
            queue = []

            # start_movement, item = queue.pop(0)
            for start_movement, item in level:
                possible_target = self.find_target_within_range(targets)
                if possible_target:
                    return start_movement, possible_target

                for movement in item.get_possible_moves():
                    new_balloon = item.copy()
                    new_balloon.move(movement)
                    if new_balloon.isActive:
                        queue.append((start_movement, new_balloon))

        # could not find
        if self.altitude == -1:
            return 1, None
        return 0, None

    def find_target_within_range(self, targets):
        target_x = (self.row, self.column)
        radius = self.coverageRadius
        for target in targets:
            if target_x[0] - radius <= target[0] <= target_x[0] + radius and target_x[1] - radius <= target[1] <= target_x[1] + radius:
                return target

    def calc_level_movement(self, target):
        """ returns: -1, 0, 1 """
        min_distance = 99999999
        best_movement = 0
        maxRow = -1
        for movement in self.get_possible_moves():
            distance = self.calc_distance_after_move(movement, target)
            ### IF WITHIN COVERAGE RADIUS OF BOUNDARY 
                #, CHOOSE MOVEMENT WITH MAX GETPOSITIONAFTERWINDBLOWS[ROW]
            # if self.row < self.coverageRadius*3 and 100<self.column<150:
            if (self.row < self.coverageRadius*4 and 100<self.column<150) or self.row < self.coverageRadius*2:
                windMap = self.windmaps[self.altitude + movement]
                nextRow = windMap.getPositionAfterWindBlows((self.row, self.column))[0]
                if nextRow > maxRow:
                    maxRow = nextRow    
                    best_movement = movement
            elif distance < min_distance:
                min_distance = distance
                best_movement = movement
        return best_movement
        
    def get_possible_moves(self):
        if self.altitude == -1:
            return [1]
        moves = [0]
        if self.altitude > 0:
            moves.append(-1)
        if self.altitude < len(self.windmaps) - 1:
            moves.append(1)
        return moves
    
    def calc_distance_after_move(self, movement, target):
        movementWindMap = self.windmaps[self.altitude + movement]
        movementPostion = movementWindMap.getPositionAfterWindBlows((self.row, self.column))
        dummyBaloon = Balloon(-1, movementPostion[0], movementPostion[1], None, None, self.numberRows, self.numberColumns, None)
        return dummyBaloon.getDistanceToTarget(target[0], target[1])
    
    def move(self, movement):
        self.altitude += movement
        self.row, self.column = self.windmaps[self.altitude].getPositionAfterWindBlows((self.row, self.column))
        
        if self.row < 0 or self.row >= self.numberRows:
            self.isActive = False

def parse_input(path):
    with open(path) as fh:
        
        ## FIRST LINE
        line = fh.readline()
        numOfRows, numOfColumns, numOfAltitudes = (int(x) for x in line.split())
        
        
        
        ## SECOND LINE
        line = fh.readline()
        numOfTargets, coverageRadius, numOfBalloons, numOfTurns =  (int(x) for x in line.split())
        
        
        
        ## GET THE STARTING CELL
        line = fh.readline()
        startingCell = tuple([int(x) for x in line.split()])
        
        
        ## GET THE TARGETS
        targets = []
        for i in range(numOfTargets):
            line = fh.readline()
            targets.append(tuple([int(x) for x in line.split()]))
            
            
        ## GET THE WINDMAP FOR EACH ALTITUDE
        windmaps = []
        for i in range(numOfAltitudes):
            rows = [] 
            for j in range(numOfRows):
                columns = []
                line = fh.readline().split()
                for k in range(numOfColumns):
                    columns.append((int(line[2*k]), int(line[2*k+1])))
                
                rows.append(columns)
                
              
            windmaps.append(WindMap(numOfRows, numOfColumns, i + 1, rows))
            
        ## initiate balloons
        balloons = []
        for i in range(numOfBalloons):
            balloons.append(Balloon(i, startingCell[0], startingCell[1], -1, windmaps, numOfRows, numOfColumns, coverageRadius))
            
    #numOfRows, numOfColumns, numOfAltitudes, numOfTargets, coverageRadius, numOfBalloons, numOfTurns, startingCell, targets, windmaps    
    return targets, balloons, numOfTurns
        
    
        
       
    
def get_uncovered_targets(targets, target_x, radius):
    new_targets = []
    for target in targets:
        if not target_x[0] - radius <= target[0] <= target_x[0] + radius:
            new_targets.append(target)
        elif not target_x[1] - radius <= target[1] <= target_x[1] + radius:
            new_targets.append(target)
    return new_targets


def main():
    input_file = 'inputs/small.txt'
    input_file = 'inputs/large.txt'
    
    targets0, balloons, turns = parse_input(input_file)

    with open('outputs/movements.txt', 'w') as output:
        for turn in range(turns):
            targets = targets0[:]
            movements = []
            for b in balloons:
                if not targets:
                    movements.append(0)
                    continue
                if b.isActive:
                    # target = b.find_nearest_target(targets)
                    # movement = b.calc_level_movement(target)
                    movement, target = b.find_nearest_reachable_target(targets)
                    b.move(movement)
                    movements.append(movement)
                    if target:
                        targets = get_uncovered_targets(targets, target, b.coverageRadius)
                else:
                    movements.append(0)
            # print('{}\n'.format(movement))
            output.write('{}\n'.format(' '.join([str(x) for x in movements])))
            # if turn > 5:
            #     break
    
if __name__ == '__main__':
    main()

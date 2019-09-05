import imagematrix
import math

#Naive algorithm that recursivley goes through the tree of energy values and returns a new (not always the most optimal)path every time its called.
#uses a traveled array that stores paths that have already been traveled.
#Once the function reaches the the max height it checks to see if the current path is already in traveled.
#If it is then the current call returns false and the previous call moves onto the next node.
def r_best_seam(self, startx, totalcost, depth, traveled, path, allpaths):
    found = False
    depth+=1
    totalcost += self.energy(startx, depth)
    path.append((startx, depth))
    if depth == self.height-1:
        if path in traveled:
            return False
        traveled.append(path)
        allpaths.append((totalcost, path))
        return True
    else:
        if startx == 0:
            for i in range (2):
                found = r_best_seam(self, i, totalcost, depth, traveled, path, allpaths)
                if found == True:
                    return True
                del path[-1]
        elif startx == (self.width-1):
            for i in range(self.width-3,self.width-1):
                found = r_best_seam(self, i, totalcost, depth, traveled, path, allpaths)
                if found == True:
                    return True
                del path[-1]
        else:
            for i in range(startx-1, startx+2):
                found = r_best_seam(self, i, totalcost, depth, traveled, path, allpaths)
                if found == True:
                    return True
                del path[-1]
        return False

#this function calls the recursive function above for each node with starting height 0
#found == false when their are no more paths to be found
#after finding all paths they are sorted and and the first path is returned
def best_seam_notdp(self):
    traveled = []
    p_traveled = traveled
    allpaths = []
    p_allpaths = allpaths
    for i in range(self.width):
        found = True
        travaled = []
        while found == True:
            found = r_best_seam(self, i, 0, -1, p_traveled,[], p_allpaths)
        print("found")

    allpaths.sort()
    return allpaths[0][1]


#class used in dynamic programming algortihm
#stores x and y, a cost, and a path which will always be the most optimal path to that node.
class Node:
    def __init__(self, x, y, cost, path):
        self.x = x
        self.y = y
        self.cost = cost
        self.path = path.copy()


#Dynamic Programming algorithm
#this algorithm Uses a Energy Table to store all Nodes made using the node class above
#Each Node in the table will store its most optimal path.
#The function loops through each node in the grid and finds its most optimal path by connecting it with then
#using its energy costs + the distance cost
def best_seam_dp(self):
    energy_table = []
    row = []
    for y in range(self.height):
         if y==0:
             for x in range(self.width):
                 row.append(Node(x,0,self.energy(x,0),[(x,0)]))
             energy_table.append(row)
             continue
         row = []
         for x in range(self.width):
             min = math.inf
             if x == 0: #start node
                 for i in range(2):
                     if energy_table[y-1][i].cost < min:
                         min = energy_table[y-1][i].cost
                         minnode = energy_table[y-1][i]
                 path = minnode.path.copy()
                 path.append((x,y))
                 row.append(Node(x,y,self.energy(x,y)+minnode.cost,path))
             elif x == (self.width-1): #end node
                 for i in range(self.width-3,self.width-1):
                     if energy_table[y-1][i].cost < min:
                         min = energy_table[y-1][i].cost
                         minnode = energy_table[y-1][i]
                 path = minnode.path.copy()
                 path.append((x,y))
                 row.append(Node(x,y,self.energy(x,y)+minnode.cost,path))
             else: #middle nodes
                 for i in range(x-1,x+2):
                     if energy_table[y-1][i].cost < min:
                          min = energy_table[y-1][i].cost
                          minnode = energy_table[y-1][i]
                 path = minnode.path.copy()
                 path.append((x,y))
                 row.append(Node(x,y,self.energy(x,y)+minnode.cost,path))
         energy_table.append(row)


    min = math.inf
    #goes through the last element in the energy table and returns the the node with the lowest cost.
    for x in range(self.width):
        if energy_table[self.height-1][x].cost < min:
            min = energy_table[self.height-1][x].cost
            minnode = energy_table[self.height-1][x]

    return minnode.path

#self.energy(x,y) x then y
class ResizeableImage(imagematrix.ImageMatrix):

    def best_seam(self, dp=True):
        if dp == True:
            return best_seam_dp(self)
        else:
            return best_seam_notdp(self)

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

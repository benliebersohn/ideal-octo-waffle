import numpy as np
import sortedcontainers
import attr
import time
import vtk
import find_neighbor
@attr.s
class Point:
    """POD struct that stores coords, a np array of length 3 (x,y,z) and neighbors, 
    a list of IDs of neighboring points.
    """
    coords = attr.ib()
    neighbors = attr.ib()


def condition(points, outletID):
    """Conditions a mesh, in place, by removing pits.

    Inputs:
      points    | A dictionary of the form {ID, Point()} 
      outletID  | ID of the outlet
    """
#points: {0: Point(coords=array([0, 0, 0]), neighbors=[1]), 1: Point(coords=array([1, 0, 1]), neighbors=[0, 2]), 2: Point(coords=array([2, 0, 3]), neighbors=[1, 3]), 3: Point(coords=array([3, 0, 2]), neighbors=[2, 4]), 4: Point(coords=array([4, 0, 1]), neighbors=[3, 5]), 5: Point(coords=array([5, 0, 4]), neighbors=[4])}

    # create a sorted list of elevations, from largest to smallest
    elev = sortedcontainers.SortedList(list(points.items()), key=lambda id_p:id_p[1].coords[2])
    waterway = set([outletID,])
    ww_neighbors = []
    neighbor_elevs = []

    # loop over elevation list from small to large
    while len(elev) is not 0:

        current, current_p = elev.pop(0)
        if current in waterway:

            # still in the waterway
            #print("current_p.neighbors: ",current_p.neighbors)
            waterway.update(current_p.neighbors)
        #else:
            # not in the waterway, fill
            #ww_neighbors = []
            for j in range(len(current_p.neighbors)):
                neighbor_elevs.append(current_p.neighbors[j])
                print("ne",neighbor_elevs)
                if current_p.neighbors[j] in waterway:
                    print("0thing")#,j,current_p.neighbors[j])
                    
            #ww_neighbors = [n for n in current_p.neighbors if n in waterway]   

            if len(ww_neighbors) != 0: #problem 1
                    print("prob 1")
            else:
                    ww_neighbors += [current_p.neighbors[j]]
                    print("ww1",ww_neighbors)
                    current_neighbors = []
                    print("problem 1 fixed")
                    for n in range(len(ww_neighbors)):
                        current_neighbors += [ww_neighbors]
                        #current_p.coords[2] = min(points[n].coords[2])
                        print("2n:",n,"curr",ww_neighbors)#, "points[n].coords[2]:",points[n].coords[2])#, "current_p.coords[2]:", current_p.coords[2])
                
                #current_p.coords[2] = min(points[n].coords[2] for n in ww_neighbors)
            #else:
                #current_p.coords[2] = min(points[n].coords[2] for n in current_p.neighbors)
            
            # push back into elev list with new, higher elevation
                    elev.add( (current,current_p) )
    return

if __name__ == "__main__":
    def make_points_1D(elevs):
        npoints = len(elevs[0])
        points = {}
        #print(elevs[0][1][1])
        for i in range(npoints):
            pid = elevs[0][i][0]
            
            e = elevs[0][i][1][0] #e is elevation value, i is Id
            
            #print("pid, e ",pid, e)
            #print(elevs[0][2])
            #e = find_neighbor.GetValue(i)
            #print("e:",e)
            coords = np.array([i,0,e]) #class point has: coords, neighbors
            #print("coords",e)
            #print(coords)

            neighbors = [find_neighbor.GetNeighborValues(i)]
            #if i == 0:

            #    neighbors = [1,]
            #elif i == len(elevs)-1:
            #    neighbors = [i-1,]
            #else:
            #    neighbors = [i-1,i+1]
            points[i] = Point(coords, neighbors)
            #print(points)
        return points

    def run_test_1D(elev_in):#, elev_out):
      #  print(elev_in)
        points = make_points_1D(elev_in)
        
        output = condition(points, 0) #problem
        print("Problem fix!!")
        return output
        #for i in range(len(elev_in)):
        #assert(points[i].coords[2] == points[i].coords[2])#does nothing #elev_out[i])
   
    sortedID = find_neighbor.GetIdSortedByZ()
    output = run_test_1D([sortedID])#, [0,1,3,3,3,4])

 #   print(output)

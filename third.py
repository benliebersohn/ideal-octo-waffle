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

    # create a sorted list of elevations, from largest to smallest
    elev = sortedcontainers.SortedList(list(points.items()), key=lambda id_p:id_p[1].coords[2])
    waterway = set([outletID,])

    # loop over elevation list from small to large
    counter = 0
    #while len(elev) is not 0:
    while (counter) < 100:
        #print("counter",counter, "len(elev):",len(elev))
        counter += 1
        current, current_p = elev.pop(0)
       # print("current",current, "waterway",waterway)
        if current in waterway:
            # still in the waterway
            #print("current_p.neighbors: ",current_p.neighbors)
            #print("in waterway, add neighbors for point", current)
            waterway.update(current_p.neighbors)
           # print("current_p",current_p,"current_p.neighbors",current_p.neighbors)
            #print("yes in ww, current", current, "waterway", waterway)
        else:
            # not in the waterway, fill
            #print("current_p",current_p,"current_p.neighbors",current_p.neighbors)
            #print("not in ww, current", current, "waterway", waterway)
            ww_neighbors = []
            for n in range(len(current_p.neighbors)):
                if current_p.neighbors[n] in waterway:
                    ww_neighbors += current_p.neighbors[n]
            #ww_neighbors = [n for n in current_p.neighbors if n in waterway]
            print("ww_neighbors",ww_neighbors)
            if len(ww_neighbors) != 0:
                #print("this")
                current_p.coords[2] = min(points[n].coords[2] for n in ww_neighbors)
            else:
                #print("that")
                neighboring_values = []
                for n in range(len(current_p.neighbors)):
                    neighboring_values += current_p.neighbors
                    
                min_neighbor_id = min(neighboring_values)
                print
                min_neighbor_value_pre = find_neighbor.GetValue(min_neighbor_id)

                min_neighbor_value = str(min_neighbor_value_pre)[1:-1]


                print("current_p.coords[2]", current_p, "we wish to change that to:", [min_neighbor_value])
                current_p.coords[2] = min_neighbor_value
                #current_p.coords[2] = min(points[n].coords[2] for n in current_p.neighbors)
            
            # push back into elev list with new, higher elevation
            elev.add( (current,current_p) )
    return


if __name__ == "__main__":
    def make_points_1D(elevs):
        points = {}
        for i,e in enumerate(elevs):
            coords = np.array([i,0,e])
            #if i == 0:
                #neighbors = [1,]
                
            #elif i == len(elevs)-1:
                #neighbors = [i-1,]
            #else:
                #neighbors = [i-1,i+1]
            neighbors = find_neighbor.GetNeighborIdsByPnt(i)
            #print("neighbors",neighbors)
            points[i] = Point(coords, neighbors)
            #print(points[i])
            #print("coords",coords,"neighbors",neighbors)
        return points

    def run_test_1D(elev_in, elev_out):
        points = make_points_1D(elev_in)
        condition(points, 0)
        
        for i in range(len(elev_in)):
            assert(points[i].coords[2] == elev_out[i])
    full_input = find_neighbor.GetIdSortedByZ()
    test_input = []

    for item in range(len(full_input)):
        test_input += full_input[item][1]
    input_list = [0,1,3,2,1,4]
#    print(test_input)
#    print(input_list)
    run_test_1D(test_input, [0,1,3,3,3,4])


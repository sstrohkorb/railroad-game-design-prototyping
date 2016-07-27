
from railroads_python_design_testing import *



#this file defines two functions, 'get_children_locations' and 'get_path_map'
#'get_path_map' makes a call to 'get_children_locations' many times as it loops through an array
#'get_path_map' takes an input, 'distance_grid', and returns the output 'path_map'
#'distance_grid' is an array where the value at a point i,j tells you how many spaces you are from the 0 entry in the array
#'distance_grid' is assumed to be 'distance_map' if no other array is passed to the function
#the output 'path_map' is an array where the value at point i,j is the number of minimum paths from that point to the sink, or the location of the 0 in 'distance_grid'

# def get_children_locations(i,j,grid = distance_map):
def get_children_locations(i, j, grid):
    #i is the row, j is the column of the grid location (the "parent")
    num_rows = len(grid)
    num_columns = len(grid[0])
    child_list = []
    # entry above
    if (i - 1 >= 0):
        if ((grid[i - 1][j] + 1 == grid[i][j]) and grid[i - 1][j] != -1):
            child_list.append([(i-1),j])
    # entry to the right
    if (j + 1 < num_columns):
        if ((grid[i][j + 1] + 1 == grid[i][j]) and grid[i][j + 1] != -1):
            child_list.append([i,(j+1)])
    # entry to the bottom
    if (i + 1 < num_rows):
        if ((grid[i + 1][j] + 1 == grid[i][j]) and grid[i + 1][j] != -1):
            child_list.append([(i+1),j])
    # entry to the left
    if (j - 1 >= 0):
        if ((grid[i][j - 1] + 1 == grid[i][j]) and grid[i][j - 1] != -1):
            child_list.append([i, (j - 1)])
    #function returns a list of child locations, so a list of lists
    return child_list


# def get_path_map(distance_grid = distance_map):
def get_path_map(distance_grid):
    #initialize path_map to all 1's
    path_map = [[1 for i in range(len(distance_grid))] for i in range(len(distance_grid[0]))]
    changes_being_made = True
    while (changes_being_made):
        changes_being_made = False
        #iterating over all matrix entries
        for i in range(len(path_map)):
            for j in range(len(path_map[0])):
                #path_map value is equal to child value if parent has 1 child
                if len(get_children_locations(i,j,distance_grid)) == 1:
                    x,y = (get_children_locations(i,j,distance_grid))[0]
                    if (path_map[i][j] != path_map[x][y]):           
                        path_map[i][j] = path_map[x][y]
                        changes_being_made = True
                #path_map value is equal to sum of child value if parent has 2 childs
                if len(get_children_locations(i,j,distance_grid)) == 2:
                    q,r = (get_children_locations(i,j,distance_grid))[0]
                    s,t = (get_children_locations(i,j,distance_grid))[1]
                    if (path_map[i][j] != path_map[q][r] + path_map[s][t]):
                        path_map[i][j] = path_map[q][r] + path_map[s][t]
                        changes_being_made = True
    #function returns array path_map with now the correct values
    return path_map
    #is it a problem that the "sink" is a 1 instead of a 0 in the path_map?

if __name__ == "__main__":

    path_length = 9

    rand_map = generate_random_map(7, 7, path_length, 9)
    print "Original path: "
    draw_path(rand_map)

    distance_map = get_current_distance_map(rand_map)
    print "\nDistance map:"
    print_distance_path_map(distance_map)

    path_map = get_path_map(distance_map)
    print "\nPath map:"
    print_distance_path_map(path_map)
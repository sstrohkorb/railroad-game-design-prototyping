
from railroads_python_design_testing import *
from path_funx import get_children_locations
from path_funx import get_path_map


'''get_path_map makes a call to 'get_children_locations' many times as it loops through an array. 'get_path_map' takes 
an input, 'distance_grid', and returns the output 'path_map'. 'distance_grid' is an array where the value at a 
point i,j tells you how many spaces you are from the 0 entry in the array. the output 'path_map' is an array where 
the value at point i,j is the number of minimum paths from that point to the sink, or the location of the 0 in distance_grid'''


if __name__ == "__main__":

    path_length = 9

    rand_map = generate_random_map(7, 7, path_length, 9)
    print "Original path: "
    draw_path(rand_map)

    distance_map = get_current_distance_map(rand_map)
    print "\nDistance map:"
    print_distance_path_map(distance_map)

    path_map = path_funx.get_path_map(distance_map)
    print "\nPath map:"
    print_distance_path_map(path_map)

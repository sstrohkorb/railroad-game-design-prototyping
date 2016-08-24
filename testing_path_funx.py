from random import choice
from railroads_python_design_testing import *
from path_funx import *


'''get_path_map makes a call to 'get_children_locations' many times as it loops through an array. 'get_path_map' takes 
an input, 'distance_grid', and returns the output 'path_map'. 'distance_grid' is an array where the value at a 
point i,j tells you how many spaces you are from the 0 entry in the array. the output 'path_map' is an array where 
the value at point i,j is the number of minimum paths from that point to the sink, or the location of the 0 in distance_grid'''


if __name__ == "__main__":

    path_length = 9

    rand_map = generate_random_map(7, 7, path_length, 9)
    print "Original game board: "
    draw_path(rand_map)

    distance_map = get_current_distance_map(rand_map)
    print "\nDistance map:"
    print_distance_path_map(distance_map)

    # path_map = get_path_map(distance_map)
    # print "\nPath map:"
    # print_distance_path_map(path_map)

    heat_map = get_current_heatmap(rand_map)
    NR_board = get_NR_board(distance_map, heat_map)
    print "\nPoints of No Return map:"
    print_distance_path_map(NR_board)

    possible_points_of_no_return = []
    for i in range(len(NR_board)):
        for j in range(len(NR_board[0])):
            if (NR_board[i][j] == 1):
                possible_points_of_no_return.append((i, j))

    random_point_of_no_return = choice(possible_points_of_no_return)

    print "\nPoint of no return chosen: " + str(random_point_of_no_return)

    random_point_of_no_return_paths_list = get_paths_list(random_point_of_no_return[0], random_point_of_no_return[1], distance_map, heat_map)
    print "\nAll Paths List for point of no return chosen:"
    print_distance_path_map(random_point_of_no_return_paths_list)

    random_point_of_no_return_indep_paths = get_indep_paths(random_point_of_no_return[0], random_point_of_no_return[1], distance_map, heat_map)
    print "\nALL Indep Path pairs for point of no return chosen:"
    print_indep_path_pairs(random_point_of_no_return_indep_paths)
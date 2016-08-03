from GamePiece import *
from random import randint
from random import choice

obstacle_piece = GamePiece(False, False, False, False, isObstacle=True)

game_piece_choices_dict = {
    1 : GamePiece(True, True, False, False),
    2 : GamePiece(True, False, True, False), # vertical piece
    3 : GamePiece(True, False, False, True),
    4 : GamePiece(False, True, True, False), 
    5 : GamePiece(False, True, False, True), # horizontal piece
    6 : GamePiece(False, False, True, True)
}

source_choices_dict = {
    1 : GamePiece(True, False, False, False, isSource=True),
    2 : GamePiece(False, True, False, False, isSource=True),
    3 : GamePiece(False, False, True, False, isSource=True),
    4 : GamePiece(False, False, False, True, isSource=True)
}

sink_choices_dict = {
    1 : GamePiece(True, False, False, False, isSink=True),
    2 : GamePiece(False, True, False, False, isSink=True),
    3 : GamePiece(False, False, True, False, isSink=True),
    4 : GamePiece(False, False, False, True, isSink=True)
}

""" auto_add_piece_to_matrix(piece_matrix, piece)
    Description: Assumes that the matrix has one source, no sink, and the path
    up to this point is valid. Adds the incoming piece to the current end of 
    the current path.
"""
def auto_add_piece_to_matrix(piece_matrix, piece):
    
    (open_piece_location, open_piece_source_direction) = get_open_piece_location_and_flow_direction(piece_matrix)
    # add the new piece
    if (piece.has_opening(open_piece_source_direction)):
        piece_matrix[open_piece_location[0]][open_piece_location[1]] = piece
        return True
    else:
        print ("Cannot add piece: Piece doesn't fit current path:")
        print piece
        return False


""" draw_path(piece_matrix)
    Description: prints a path of the piece matrix given (+ returns null);
    the piece matrix gives the row and column location of each of the 
    pieces
"""
def draw_path(piece_matrix):
    for piece_row in piece_matrix:
        # for each column printed
        for i in range(3): 
            print_row = ""
            # for each of the pieces in the row
            for j in range(len(piece_row)):
                if (piece_row[j] != None):
                    piece_rep = piece_row[j].get_visual_representation()
                    print_row += piece_rep[i]
                else: 
                    print_row += "      "
            print (print_row)

""" generate_random_map(num_rows, num_columns, min_path_length)
    Description: generates a random map with the specified number of rows and 
    columns, randomness is introduced by the locations of the source and sink
"""
def generate_random_map(num_rows, num_columns, min_path_length, num_obstacles):
    output_map = [[None for j in range(num_columns)] for i in range(num_rows)]
    distance_map = [[100 for j in range(num_columns)] for i in range(num_rows)]

    entire_map_requirements_met = False

    while (not entire_map_requirements_met):
    
        output_map = [[None for j in range(num_columns)] for i in range(num_rows)]

        distance_map_requirements_met = False

        while (not distance_map_requirements_met):
            # reset the distance map
            distance_map = [[100 for j in range(num_columns)] for i in range(num_rows)]

            # choose a random location for the sink
            sink_row = randint(0, num_rows - 1)
            sink_column = randint(0, num_columns - 1)

            # choose unique locations for each of the obstacles
            obstacle_locations = []
            found_obstacle_locations = False
            while (not found_obstacle_locations):
                # select a random location
                rand_location = (randint(0, num_rows - 1), randint(0, num_columns - 1))

                # check if that space is already occupied
                isSpaceOccupied = False
                if ((sink_row, sink_column) == rand_location):
                    isSpaceOccupied = True
                for obstacle_location in obstacle_locations:
                    if (obstacle_location == rand_location):
                        isSpaceOccupied = True

                # check if it's directly blocking the sink
                # above
                if (rand_location[0] - 1 >= 0):
                    if (sink_row == (rand_location[0] - 1) and sink_column == rand_location[1]):
                        isSpaceOccupied = True
                # right
                if (rand_location[1] + 1 < num_columns):
                    if (sink_row == rand_location[0] and sink_column == (rand_location[1] + 1)):
                        isSpaceOccupied = True
                # below
                if (rand_location[0] + 1 < num_rows):
                    if (sink_row == (rand_location[0] + 1) and sink_column == rand_location[1]):
                        isSpaceOccupied = True
                # left
                if (rand_location[1] - 1 >= 0):
                    if (sink_row == rand_location[0] and sink_column == (rand_location[1] - 1)):
                        isSpaceOccupied = True

                # if it's not occupied, add it to the obstacle list
                if (not isSpaceOccupied):
                    obstacle_locations.append(rand_location)

                # stop if we have a full obstacle location list
                if (len(obstacle_locations) == num_obstacles):
                    found_obstacle_locations = True

            # fill out the distance map
            distance_map[sink_row][sink_column] = 0
            for obstacle_location in obstacle_locations:
                distance_map[obstacle_location[0]][obstacle_location[1]] = -1 
            changes_being_made = True
            while (changes_being_made):
                changes_being_made = False
                for i in range(len(distance_map)):
                    for j in range(len(distance_map[0])):
                        # above
                        if (i - 1 >= 0):
                            if ((distance_map[i - 1][j] + 1 < distance_map[i][j]) and distance_map[i - 1][j] != -1):
                                distance_map[i][j] = distance_map[i - 1][j] + 1
                                changes_being_made = True
                        # left
                        if (j + 1 < num_columns):
                            if ((distance_map[i][j + 1] + 1 < distance_map[i][j]) and distance_map[i][j + 1] != -1):
                                distance_map[i][j] = distance_map[i][j + 1] + 1
                                changes_being_made = True
                        # bottom
                        if (i + 1 < num_rows):
                            if ((distance_map[i + 1][j] + 1 < distance_map[i][j]) and distance_map[i + 1][j] != -1):
                                distance_map[i][j] = distance_map[i + 1][j] + 1
                                changes_being_made = True
                        # left
                        if (j - 1 >= 0):
                            if ((distance_map[i][j - 1] + 1 < distance_map[i][j]) and distance_map[i][j - 1] != -1):
                                distance_map[i][j] = distance_map[i][j - 1] + 1
                                changes_being_made = True

            for i in range(len(distance_map)):
                for j in range(len(distance_map[0])):
                    if (distance_map[i][j] == (min_path_length + 1)):
                        distance_map_requirements_met = True
                        break

        possible_source_locations = []
        for i in range(len(distance_map)):
            for j in range(len(distance_map[0])):
                if (distance_map[i][j] == (min_path_length + 1)):
                    possible_source_locations.append((i, j))

        chosen_sink_location = (sink_row, sink_column)
        chosen_source_location = choice(possible_source_locations)

        # now that we have source and sink locations, get them orientations, and put them in
        # check all 4 neighbors for the direction of the shortest path

        sink_neighbors = get_neighbors(distance_map, chosen_sink_location, 1)
        source_neighbors = get_neighbors(distance_map, chosen_source_location, min_path_length)

        sink_options = []
        source_options = []

        for sink_neighbor in sink_neighbors:
            # top
            if (sink_neighbor[0] == (chosen_sink_location[0] - 1) and sink_neighbor[1] == chosen_sink_location[1]):
                sink_options.append(sink_choices_dict[1])
            # right
            if (sink_neighbor[0] == chosen_sink_location[0] and sink_neighbor[1] == (chosen_sink_location[1] + 1)):
                sink_options.append(sink_choices_dict[2])
            # bottom
            if (sink_neighbor[0] == (chosen_sink_location[0] + 1) and sink_neighbor[1] == chosen_sink_location[1]):
                sink_options.append(sink_choices_dict[3])
            #left
            if (sink_neighbor[0] == chosen_sink_location[0] and sink_neighbor[1] == (chosen_sink_location[1] - 1)):
                sink_options.append(sink_choices_dict[4])

        for source_neighbor in source_neighbors:
            # top
            if (source_neighbor[0] == (chosen_source_location[0] - 1) and source_neighbor[1] == chosen_source_location[1]):
                source_options.append(source_choices_dict[1])
            # right
            if (source_neighbor[0] == chosen_source_location[0] and source_neighbor[1] == (chosen_source_location[1] + 1)):
                source_options.append(source_choices_dict[2])
            # bottom
            if (source_neighbor[0] == (chosen_source_location[0] + 1) and source_neighbor[1] == chosen_source_location[1]):
                source_options.append(source_choices_dict[3])
            #left
            if (source_neighbor[0] == chosen_source_location[0] and source_neighbor[1] == (chosen_source_location[1] - 1)):
                source_options.append(source_choices_dict[4])

        # put the obstacles in place
        for obstacle_location in obstacle_locations:
            output_map[obstacle_location[0]][obstacle_location[1]] = obstacle_piece

        # put the source in place
        output_map[chosen_source_location[0]][chosen_source_location[1]] = choice(source_options)

        # put the sink in place (not facing an obstacle ideally)
        # also ensure that each sink has at least 2 possible end pieces 
        bad_sinks = []
        for i in range(len(sink_options)):
            if sink_options[i].top and output_map[chosen_sink_location[0] - 1][chosen_sink_location[1]] != None:
                if output_map[chosen_sink_location[0] - 1][chosen_sink_location[1]].isObstacle:
                    bad_sinks.append(sink_options[i])
            elif sink_options[i].right and output_map[chosen_sink_location[0]][chosen_sink_location[1] + 1] != None:
                if output_map[chosen_sink_location[0]][chosen_sink_location[1] + 1].isObstacle:
                    bad_sinks.append(sink_options[i])
            elif sink_options[i].bottom and output_map[chosen_sink_location[0] + 1][chosen_sink_location[1]] != None:
                if output_map[chosen_sink_location[0] + 1][chosen_sink_location[1]].isObstacle:
                    bad_sinks.append(sink_options[i])
            elif sink_options[i].left and output_map[chosen_sink_location[0]][chosen_sink_location[1] - 1] != None:
                if output_map[chosen_sink_location[0]][chosen_sink_location[1] - 1].isObstacle:
                    bad_sinks.append(sink_options[i])
        
        good_sinks = []
        for sink_option in sink_options:
            if sink_option not in bad_sinks:
                good_sinks.append(sink_option)

        if (len(good_sinks) > 0):
            output_map[chosen_sink_location[0]][chosen_sink_location[1]] = choice(good_sinks)
            # get the updated distance map and make sure that our source --> sink still has the minimum path
            updated_distance_map = get_current_distance_map(output_map)
            # get the location of the piece location next to the source
            source_piece = output_map[chosen_source_location[0]][chosen_source_location[1]]
            if (source_piece.top):
                piece_following_source_location = (chosen_source_location[0] - 1, chosen_source_location[1])
            elif (source_piece.right):
                piece_following_source_location = (chosen_source_location[0], chosen_source_location[1] + 1)
            elif (source_piece.bottom):
                piece_following_source_location = (chosen_source_location[0] + 1, chosen_source_location[1])
            else: 
                piece_following_source_location = (chosen_source_location[0], chosen_source_location[1] - 1)

            # ensure that the sink is surrounded by at least 2 options for departure from it
            reverse_distance_map = get_current_distance_map(output_map, True)
            sink_has_2_piece_options = False
            # get_neighbors(matrix, my_position, constraint=None)
            sink_piece = output_map[chosen_sink_location[0]][chosen_sink_location[1]]
            if (sink_piece.top):
                piece_next_to_sink_location = (chosen_sink_location[0] - 1, chosen_sink_location[1])
            elif (sink_piece.right):
                piece_next_to_sink_location = (chosen_sink_location[0], chosen_sink_location[1] + 1)
            elif (sink_piece.bottom):
                piece_next_to_sink_location = (chosen_sink_location[0] + 1, chosen_sink_location[1])
            else: 
                piece_next_to_sink_location = (chosen_sink_location[0], chosen_sink_location[1] - 1)

            min_path_neighbors = get_neighbors(reverse_distance_map, piece_next_to_sink_location, (min_path_length - 2))
            
            if (updated_distance_map[piece_following_source_location[0]][piece_following_source_location[1]] == (min_path_length - 1)
                and len(min_path_neighbors) >= 2):
                entire_map_requirements_met = True
        else:
            output_map[chosen_sink_location[0]][chosen_sink_location[1]] = choice(sink_options)


    return output_map

""" get_current_distance_map(piece_matrix, reverse_map)
    Description: generate the current distance map based on the current piece matrix.
    Handles barriers and the directionality of the current open piece and sink. 
    The reverse_map flag, if true, returns the opposite of the non-reversed map
    where the sink and the source are flipped. 
"""
def get_current_distance_map(piece_matrix, reverse_map=False):
    # we're going to treat the sink as the piece next to the sink's opening
    # let's first get that location
    sink = None
    for i in range(len(piece_matrix)):
        for j in range(len(piece_matrix[0])):
            if piece_matrix[i][j] != None:
                if (piece_matrix[i][j].isSink and reverse_map == False):
                    sink = piece_matrix[i][j]
                    actual_sink_location = (i, j)
                    break
                    # if we're reversing this - we want to look for the source not the sink
                elif (piece_matrix[i][j].isSource and reverse_map == True):
                    sink = piece_matrix[i][j]
                    actual_sink_location = (i, j)
                    break
    if (sink == None):
        if (reverse_map == False):
            print "There is no sink in this matrix - cannot get distance map"
        else: 
            print "There is no source in this matrix - cannot get distance map"
        return
    if (sink.top):
        sink_location = (actual_sink_location[0] - 1, actual_sink_location[1])
    elif (sink.right):
        sink_location = (actual_sink_location[0], actual_sink_location[1] + 1)
    elif (sink.bottom):
        sink_location = (actual_sink_location[0] + 1, actual_sink_location[1])
    else:
        sink_location = (actual_sink_location[0], actual_sink_location[1] - 1)

    # print "Sink location: " + str (sink_location)

    num_rows = len(piece_matrix)
    num_columns = len(piece_matrix[0])
    distance_map = [[100 for j in range(num_columns)] for i in range(num_rows)]

    # set the sink's distance value to 0
    distance_map[sink_location[0]][sink_location[1]] = 0

    # set all other pieces that aren't the current open piece and the actual sink to -1 
    for i in range(len(piece_matrix)):
        for j in range(len(piece_matrix[0])):
            if (piece_matrix[i][j] != None):
                # if not ((i == sink_location[0] and j == sink_location[1]) or (i == open_piece_location[0] and j == open_piece_location[1])):
                if not (i == sink_location[0] and j == sink_location[1]):
                    distance_map[i][j] = -1
    changes_being_made = True
    while (changes_being_made):
        changes_being_made = False
        for i in range(len(distance_map)):
            for j in range(len(distance_map[0])):
                # above
                if (i - 1 >= 0):
                    if ((distance_map[i - 1][j] + 1 < distance_map[i][j]) and distance_map[i - 1][j] != -1):
                        distance_map[i][j] = distance_map[i - 1][j] + 1
                        changes_being_made = True
                # left
                if (j + 1 < num_columns):
                    if ((distance_map[i][j + 1] + 1 < distance_map[i][j]) and distance_map[i][j + 1] != -1):
                        distance_map[i][j] = distance_map[i][j + 1] + 1
                        changes_being_made = True
                # bottom
                if (i + 1 < num_rows):
                    if ((distance_map[i + 1][j] + 1 < distance_map[i][j]) and distance_map[i + 1][j] != -1):
                        distance_map[i][j] = distance_map[i + 1][j] + 1
                        changes_being_made = True
                # left
                if (j - 1 >= 0):
                    if ((distance_map[i][j - 1] + 1 < distance_map[i][j]) and distance_map[i][j - 1] != -1):
                        distance_map[i][j] = distance_map[i][j - 1] + 1
                        changes_being_made = True

    return distance_map

""" get_current_heatmap(matrix)
    Description: Returns a distance map matrix of sorts where every space that
    is on a minimum path from source to sink is represented by a true value and
    every space not on that minimum path is represented by a false value (this
    includes the sink and sources themselves)
"""
def get_current_heatmap(matrix):
    # initialize the heatmap
    num_rows = len(matrix)
    num_columns = len(matrix[0])
    combined_distance_map = [[0 for j in range(num_columns)] for i in range(num_rows)]
    heatmap = [[False for j in range(num_columns)] for i in range(num_rows)]

    distance_map = get_current_distance_map(matrix)
    reverse_distance_map = get_current_distance_map(matrix, True)

    min_val = 100
    for i in range(num_rows):
        for j in range(num_columns):
            combined_distance_map[i][j] = distance_map[i][j] + reverse_distance_map[i][j]
            if (combined_distance_map[i][j] < min_val and combined_distance_map[i][j] > 0):
                min_val = combined_distance_map[i][j]

    for i in range(num_rows):
        for j in range (num_columns):
            if (combined_distance_map[i][j] == min_val):
                heatmap[i][j] = True

    return heatmap


""" get_neighbors(matrix, my_position, constraint=None)
    Description: Get all neighbors (top, right, left, bottom) of a particular 
    position in a matrix that hold to the input constraint. 
"""
def get_neighbors(matrix, my_position, constraint=None):

    num_rows = len(matrix)
    num_columns = len(matrix[0])

    neighbors = []

    # top
    if (my_position[0] - 1 >= 0):
        if (constraint != None):
            if (matrix[my_position[0] - 1][my_position[1]] == constraint):
                neighbors.append((my_position[0] - 1, my_position[1]))
        else: 
            neighbors.append((my_position[0] - 1, my_position[1]))
    # right
    if (my_position[1] + 1 < num_columns):
        if (constraint != None):
            if (matrix[my_position[0]][my_position[1] + 1] == constraint):
                neighbors.append((my_position[0], my_position[1] + 1))
        else:
            neighbors.append((my_position[0], my_position[1] + 1))
    # below
    if (my_position[0] + 1 < num_rows):
        if (constraint != None):
            if (matrix[my_position[0] + 1][my_position[1]] == constraint):
                neighbors.append((my_position[0] + 1, my_position[1]))
        else:
            neighbors.append((my_position[0] + 1, my_position[1]))
    # left
    if (my_position[1] - 1 >= 0):
        if (constraint != None):
            if (matrix[my_position[0]][my_position[1] - 1] == constraint):
                neighbors.append((my_position[0], my_position[1] - 1))
        else:
            neighbors.append((my_position[0], my_position[1] - 1))

    return neighbors


""" get_new_piece_flow_direction_and_location(old_piece_flow_output, old_piece_location)
    Description: Based on the old piece's location and flow output, 
    determine the next piece's location and flow input
"""
def get_new_piece_flow_direction_and_location(old_piece_flow_output, old_piece_location):
    new_piece_flow_direction = GamePiece.NONE
    new_piece_location = (-1, -1)
    if (old_piece_flow_output == GamePiece.TOP):
        new_piece_flow_direction = GamePiece.BOTTOM
        new_piece_location = (old_piece_location[0] - 1, old_piece_location[1])
    elif (old_piece_flow_output == GamePiece.BOTTOM):
        new_piece_flow_direction = GamePiece.TOP
        new_piece_location = (old_piece_location[0] + 1, old_piece_location[1])
    elif (old_piece_flow_output == GamePiece.RIGHT):
        new_piece_flow_direction = GamePiece.LEFT
        new_piece_location = (old_piece_location[0], old_piece_location[1] + 1)
    elif (old_piece_flow_output == GamePiece.LEFT):
        new_piece_flow_direction = GamePiece.RIGHT
        new_piece_location = (old_piece_location[0], old_piece_location[1] - 1)

    return (new_piece_flow_direction, new_piece_location)

""" get_open_piece_location_and_flow_direction(piece_matrix)
    Description: Get the piece location and flow direction of the next piece 
    in the path from source to sink
"""
def get_open_piece_location_and_flow_direction(piece_matrix):
    num_rows = len(piece_matrix)
    num_columns = len(piece_matrix[0])

    # find the source
    source_locations = []
    for i in range(num_rows):
        for j in range(num_columns):
            if (piece_matrix[i][j] != None):
                if (piece_matrix[i][j].is_sink_source() and piece_matrix[i][j].isSource):
                    source_locations.append((i, j))
    if (len(source_locations) != 1):
        print "Cannot add piece: " + str(len(source_locations)) + " number of sources/sinks"
        return False
    else: 
        source_location = source_locations[0]

    # traverse the path until we reach an empty point
    path_search = True
    current_piece = piece_matrix[source_location[0]][source_location[1]]
    current_piece_location = source_location
    prev_source_direction = GamePiece.NONE
    while (path_search):
        # end case - we've reached an opening
        if (current_piece == None):
            path_search = False

        # determine whether the piece fits the previous source direction
        elif (current_piece.has_opening(prev_source_direction)):
            current_piece_flow_output = current_piece.get_flow_output(prev_source_direction)
            (new_piece_flow_direction, new_piece_location) = get_new_piece_flow_direction_and_location(current_piece_flow_output, current_piece_location)
            if (new_piece_location[0] < 0 or new_piece_location[0] >= num_rows):
                print ("Cannot add piece: Flow of path has reached edge with piece:")
                print current_piece
                return False
            elif (new_piece_location[1] < 0 or new_piece_location[1] >= num_columns):
                print ("Cannot add piece: Flow of path has reached edge with piece:")
                print current_piece
                return False
            else: 
                # set the new source direction + next piece
                current_piece = piece_matrix[new_piece_location[0]][new_piece_location[1]]
                current_piece_location = new_piece_location
                prev_source_direction = new_piece_flow_direction
        else:
            print ("Cannot add piece: Piece doesn't fit in the path:")
            print current_piece
            return False

    return (current_piece_location, prev_source_direction)

""" get_valid_pieces(piece_matrix)
    Description: Gets all the possible valid and invalid pieces for the next 
    open spot on the path. Assumes a correct path so far. 
"""
def get_valid_and_invalid_pieces(piece_matrix):
    valid_pieces = []
    invalid_pieces = []

    (open_piece_location, open_piece_source_direction) = get_open_piece_location_and_flow_direction(piece_matrix)

    # check for the existance of a nearby sink (up, right, down, left)
    nearby_sink_location = (-1, -1)
    num_rows = len(piece_matrix)
    num_columns = len(piece_matrix[0])
    for i in range(3):
        for j in range(3):
            if ((i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 2) or (i == 2 and j == 1)):
                temp_piece_location = (open_piece_location[0] - 1 + i, open_piece_location[1] - 1 + j)
                # if the slot is in range
                if (temp_piece_location[0] >= 0 and temp_piece_location[0] < num_rows and temp_piece_location[1] >= 0 and temp_piece_location[1] < num_columns):
                    if (piece_matrix[temp_piece_location[0]][temp_piece_location[1]] != None):
                        if (piece_matrix[temp_piece_location[0]][temp_piece_location[1]].isSink):
                            nearby_sink_location = temp_piece_location

    # if there's a nearby sink
    if (nearby_sink_location != (-1, -1)):
        sink = piece_matrix[nearby_sink_location[0]][nearby_sink_location[1]]
        (new_piece_flow_direction, new_piece_location) = get_new_piece_flow_direction_and_location(sink.get_flow_output(GamePiece.NONE), nearby_sink_location)
        piece_constraints = [open_piece_source_direction, new_piece_flow_direction]
    else:
        piece_constraints = [open_piece_source_direction]

    return organize_pieces_from_constraints(piece_constraints)


""" is_valid_path()
    Description: return True if the path has a source, sink, and pieces that
    connect the source to the sink without any disconnected pieces; and False
    otherwise
"""
def is_valid_path(piece_matrix):
    num_rows = len(piece_matrix)
    num_columns = len(piece_matrix[0])
    piece_occupy = [[False for j in range(num_columns)] for i in range(num_rows)]

    # find the source and the sink
    source_and_sink = []
    for i in range(num_rows):
        for j in range(num_columns):
            if (piece_matrix[i][j] != None):
                if (piece_matrix[i][j].is_sink_source()):
                    source_and_sink.append((i, j))

    if (len(source_and_sink) != 2):
        print "Invalid path: Path does not include both a source and sink"
        return False

    # we'll treat the first entry in source_and_sink as the source and trace 
    # it's path to the sink
    path_search = True
    current_piece = piece_matrix[source_and_sink[0][0]][source_and_sink[0][1]]
    current_piece_location = source_and_sink[0]
    piece_occupy[source_and_sink[0][0]][source_and_sink[0][1]] = True
    prev_source_direction = GamePiece.NONE
    while (path_search):
        # end case - we've reached the sink 
        if (current_piece.is_sink_source() and current_piece_location == source_and_sink[1]):
            piece_occupy[current_piece_location[0]][current_piece_location[1]] = True
            path_search = False

        # determine whether the piece fits the previous source direction
        elif (current_piece != None and current_piece.has_opening(prev_source_direction)):
            current_piece_flow_output = current_piece.get_flow_output(prev_source_direction)
            (new_piece_flow_direction, new_piece_location) = get_new_piece_flow_direction_and_location(current_piece_flow_output, current_piece_location)
            if (new_piece_location[0] < 0 or new_piece_location[0] >= num_rows):
                print ("Invalid path: Flow of path has reached edge with piece:")
                print current_piece
                return False
            elif (new_piece_location[1] < 0 or new_piece_location[1] >= num_columns):
                print ("Invalid path: Flow of path has reached edge with piece:")
                print current_piece
                return False
            else: 
                # set the new source direction + next piece
                piece_occupy[current_piece_location[0]][current_piece_location[1]] = True
                current_piece = piece_matrix[new_piece_location[0]][new_piece_location[1]]
                current_piece_location = new_piece_location
                prev_source_direction = new_piece_flow_direction
        else:
            print ("Invalid path: Piece doesn't fit in the path:")
            print current_piece
            return False

    # check to see if there are any pieces in the matrix that weren't covered in the path
    for i in range(num_rows):
        for j in range(num_columns):
            if (piece_occupy == False and piece_matrix[i][j] != None):
                # if the piece is a barrier, we treat it as a valid piece in the space
                if (piece_matrix[i][j].isObstacle == False):
                    print "Invalid path: Piece in path that is not connected to the path:"
                    print piece_matrix[i][j]
                    return False

    return True

""" organize_pieces_from_constraints(constraints)
    Description: Returns 2 lists, one where pieces fit the constraints, the 
    other where the pieces don't fit the flow constraints. Handles 1 or 2 
    constraints.
"""
def organize_pieces_from_constraints(constraints):
    pieces_in = []
    pieces_out = []

    if (len(constraints) < 1 or len(constraints) > 2):
        print "Invalid number of constraints"
        return [[], []]
    elif (len(constraints) == 1):
        constraint = constraints[0]
        for key in game_piece_choices_dict:
            if (constraint == GamePiece.TOP):
                if (game_piece_choices_dict[key].top):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])
            if (constraint == GamePiece.RIGHT):
                if (game_piece_choices_dict[key].right):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])
            if (constraint == GamePiece.BOTTOM):
                if (game_piece_choices_dict[key].bottom):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])
            if (constraint == GamePiece.LEFT):
                if (game_piece_choices_dict[key].left):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])
    else: 
        constraint1 = constraints[0]
        constraint2 = constraints[1]
        for key in game_piece_choices_dict:
            if ((constraint1 == GamePiece.TOP or constraint2 == GamePiece.TOP) and (constraint1 == GamePiece.RIGHT or constraint2 == GamePiece.RIGHT)):
                if (game_piece_choices_dict[key].top and game_piece_choices_dict[key].right):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])
            elif ((constraint1 == GamePiece.TOP or constraint2 == GamePiece.TOP) and (constraint1 == GamePiece.BOTTOM or constraint2 == GamePiece.BOTTOM)): 
                if (game_piece_choices_dict[key].top and game_piece_choices_dict[key].bottom):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])  
            elif ((constraint1 == GamePiece.TOP or constraint2 == GamePiece.TOP) and (constraint1 == GamePiece.LEFT or constraint2 == GamePiece.LEFT)): 
                if (game_piece_choices_dict[key].top and game_piece_choices_dict[key].left):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key])     
            elif ((constraint1 == GamePiece.RIGHT or constraint2 == GamePiece.RIGHT) and (constraint1 == GamePiece.BOTTOM or constraint2 == GamePiece.BOTTOM)):
                if (game_piece_choices_dict[key].right and game_piece_choices_dict[key].bottom):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key]) 
            elif ((constraint1 == GamePiece.RIGHT or constraint2 == GamePiece.RIGHT) and (constraint1 == GamePiece.LEFT or constraint2 == GamePiece.LEFT)):  
                if (game_piece_choices_dict[key].right and game_piece_choices_dict[key].left):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key]) 
            elif ((constraint1 == GamePiece.BOTTOM or constraint2 == GamePiece.BOTTOM) and (constraint1 == GamePiece.LEFT or constraint2 == GamePiece.LEFT)): 
                if (game_piece_choices_dict[key].bottom and game_piece_choices_dict[key].left):
                    pieces_in.append(game_piece_choices_dict[key])
                else:
                    pieces_out.append(game_piece_choices_dict[key]) 

    return [pieces_in, pieces_out]

""" print_distance_path_map(input_map)
    Description: prints the input map with easy-to-read spacing
"""
def print_distance_path_map(input_map):
    for i in range(len(input_map)):
        row_str = "["
        for j in range(len(input_map[0])):
            if (input_map[i][j] >= 0 and input_map[i][j] < 10):
                row_str += "  " + str(input_map[i][j])
            elif (input_map[i][j] < 100):
                row_str += " " + str(input_map[i][j])
            else: 
                row_str += str(input_map[i][j])
            if (j < (len(input_map[0]) - 1)):
                row_str += ", "
        row_str += "]"
        print row_str





from GamePiece import *
from railroads_python_design_testing import *
from random import choice

def get_next_optimal_piece(piece_matrix):

    current_distance_map = get_current_distance_map(piece_matrix)

    (current_open_piece_location, input_flow_direction) = get_open_piece_location_and_flow_direction(piece_matrix)

    # get the direction the flow should go next (check all neighbors in the 
    # current distance map of the current open piece)
    current_row = current_open_piece_location[0]
    current_col = current_open_piece_location[1]
    output_flow_direction_options = []
    is_sink_neighbor = False
    sink_flow_direction = GamePiece.NONE
    # top
    if ((current_row - 1) >= 0):
        if (piece_matrix[current_row - 1][current_col] != None):
            if (piece_matrix[current_row - 1][current_col].isSink):
                is_sink_neighbor = True
                sink_flow_direction = GamePiece.TOP
        if (current_distance_map[current_row - 1][current_col] == (current_distance_map[current_row][current_col] - 1)):
            output_flow_direction_options.append(GamePiece.TOP)
    # right 
    if ((current_col + 1) < len(piece_matrix[0])):
        if (piece_matrix[current_row][current_col + 1] != None):
            if (piece_matrix[current_row][current_col + 1].isSink):
                is_sink_neighbor = True
                sink_flow_direction = GamePiece.RIGHT
        if (current_distance_map[current_row][current_col + 1] == (current_distance_map[current_row][current_col] - 1)):
            output_flow_direction_options.append(GamePiece.RIGHT)
    # bottom
    if ((current_row + 1) < len(piece_matrix)):
        if (piece_matrix[current_row + 1][current_col] != None):
            if (piece_matrix[current_row + 1][current_col].isSink):
                is_sink_neighbor = True
                sink_flow_direction = GamePiece.BOTTOM
        if (current_distance_map[current_row + 1][current_col] == (current_distance_map[current_row][current_col] - 1)):
            output_flow_direction_options.append(GamePiece.BOTTOM)
    # left
    if ((current_col - 1) >= 0):
        if (piece_matrix[current_row][current_col - 1] != None):
            if (piece_matrix[current_row][current_col - 1].isSink):
                is_sink_neighbor = True
                sink_flow_direction = GamePiece.LEFT
        if (current_distance_map[current_row][current_col - 1] == (current_distance_map[current_row][current_col] - 1)):
            output_flow_direction_options.append(GamePiece.LEFT)

    # if the sink is a neighbor, set the output flow direciton to the direction of the 
    # sink, otherwise choose randomly between output flow options if there are multiple 
    # options
    if (is_sink_neighbor):
        output_flow_direction = sink_flow_direction
    else: 
        output_flow_direction = choice(output_flow_direction_options)

    # select the game piece that matches the input/output flow directions
    if ((input_flow_direction == GamePiece.TOP and output_flow_direction == GamePiece.RIGHT) or 
        (input_flow_direction == GamePiece.RIGHT and output_flow_direction == GamePiece.TOP)):
        next_optimal_piece = game_piece_choices_dict[1]
    elif ((input_flow_direction == GamePiece.TOP and output_flow_direction == GamePiece.BOTTOM) or 
          (input_flow_direction == GamePiece.BOTTOM and output_flow_direction == GamePiece.TOP)):
        next_optimal_piece = game_piece_choices_dict[2]
    elif ((input_flow_direction == GamePiece.TOP and output_flow_direction == GamePiece.LEFT) or 
          (input_flow_direction == GamePiece.LEFT and output_flow_direction == GamePiece.TOP)):
        next_optimal_piece = game_piece_choices_dict[3]
    elif ((input_flow_direction == GamePiece.RIGHT and output_flow_direction == GamePiece.BOTTOM) or 
          (input_flow_direction == GamePiece.BOTTOM and output_flow_direction == GamePiece.RIGHT)):
        next_optimal_piece = game_piece_choices_dict[4]
    elif ((input_flow_direction == GamePiece.RIGHT and output_flow_direction == GamePiece.LEFT) or 
          (input_flow_direction == GamePiece.LEFT and output_flow_direction == GamePiece.RIGHT)):
        next_optimal_piece = game_piece_choices_dict[5]
    elif ((input_flow_direction == GamePiece.BOTTOM and output_flow_direction == GamePiece.LEFT) or 
          (input_flow_direction == GamePiece.LEFT and output_flow_direction == GamePiece.BOTTOM)):
        next_optimal_piece = game_piece_choices_dict[6]

    return next_optimal_piece

def execute_optimal_path(piece_matrix, min_path_length):
    for i in range(min_path_length):
        next_piece = get_next_optimal_piece(piece_matrix)
        auto_add_piece_to_matrix(piece_matrix, next_piece)
        draw_path(piece_matrix)
        print ('\n\n\n')

    print is_valid_path(piece_matrix)


if __name__ == "__main__":

    path_length = 9

    rand_map = generate_random_map(7, 7, path_length, 9)
    print "Original path: "
    draw_path(rand_map)

    execute_optimal_path(rand_map, path_length)




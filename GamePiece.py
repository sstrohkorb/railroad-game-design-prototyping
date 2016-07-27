class GamePiece: 

    NONE = -1
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self, top, right, bottom, left, isSource=False, isSink=False, isObstacle=False):
        self.top = top          # true - top open, false - top closed
        self.right = right
        self.bottom = bottom
        self.left = left
        self.isSource = isSource
        self.isSink = isSink
        self.isObstacle = isObstacle

    def __str__(self):
        [str_row_1, str_row_2, str_row_3] = self.get_visual_representation()
        return (str_row_1 + "\n" + str_row_2 + "\n" + str_row_3)

    """ get_flow_output(flow_input)
        Get the direction of flow output giving an input. This only applies to 
        piece that are not sinks and sources. 
    """
    def get_flow_output(self, flow_input):
        if (self.is_valid()):
            # get the 2 inputs/outputs
            inputs_outputs = []
            if (self.top):
                inputs_outputs.append(GamePiece.TOP)
            if (self.right):
                inputs_outputs.append(GamePiece.RIGHT)
            if (self.bottom):
                inputs_outputs.append(GamePiece.BOTTOM)
            if (self.left):
                inputs_outputs.append(GamePiece.LEFT)

            if flow_input in inputs_outputs:
                inputs_outputs.remove(flow_input)
                return inputs_outputs[0]
            else:
                return GamePiece.NONE
        elif (self.is_sink_source()):
            if (self.top):
                return GamePiece.TOP
            elif (self.right):
                return GamePiece.RIGHT
            elif (self.bottom):
                return GamePiece.BOTTOM
            elif (self.left):
                return GamePiece.LEFT
        else:
            return GamePiece.NONE

    """ get_visual_representation()
        Description: returns an array of strings, each of which is a visual 
        representaiton of a row of the piece; each 'row' should have 3 columns
        (string length of three); sources are denoted by stars to distinguish
        them from sinks
    """
    def get_visual_representation(self):
        # one string for each row
        str_row_1 = ""
        str_row_2 = ""
        str_row_3 = ""

        # column 1
        if (self.left):
            str_row_1 += "_"
            str_row_2 += "_"
        else:
            str_row_1 += " "
            str_row_2 += " "
        str_row_3 += " "

        # column 2
        if (self.top):
            str_row_1 += "|"
        else:
            str_row_1 += " "
        if(self.left and self.isSource):
            str_row_2 += "*"
        elif (self.left):
            str_row_2 += " "
        elif (self.isObstacle):
            str_row_2 += " "
        else:
            str_row_2 += "|"
        if (self.bottom):
            str_row_3 += "|"
        else:
            str_row_3 += " "

        #column 3
        if (self.top and self.isSource):
            str_row_1 += "*"
        elif (self.top):
            str_row_1 += " "
        elif (self.isObstacle):
            str_row_1 += " "
        else: 
            str_row_1 += "_"
        if (self.bottom and self.isSource):
            str_row_2 += "*"
        elif (self.bottom):
            str_row_2 += " "
        elif (self.isObstacle):
            str_row_2 += "x"
        else:
            str_row_2 += "_"
        str_row_3 += " "

        # column 4
        if (self.top):
            str_row_1 += "|"
        else:
            str_row_1 += " "
        if(self.right and self.isSource):
            str_row_2 += "*"
        elif (self.right):
            str_row_2 += " "
        elif (self.isObstacle):
            str_row_2 += "x"
        else:
            str_row_2 += "|"
        if (self.bottom):
            str_row_3 += "|"
        else:
            str_row_3 += " "

        # column 5
        if (self.right):
            str_row_1 += "_"
            str_row_2 += "_"
        else:
            str_row_1 += " "
            str_row_2 += " "
        str_row_3 += " "

        #column 6
        str_row_1 += " "
        str_row_2 += " "
        str_row_3 += " "

        return [str_row_1, str_row_2, str_row_3]

    """ has_opening(opening_location)
        Description: checks to see if the piece has an opening at the specified 
        location. If it's a source or sink, return true if the opening_location
        is NONE

    """
    def has_opening(self, opening_location):
        if (opening_location == GamePiece.TOP and self.top == True):
            return True
        elif (opening_location == GamePiece.RIGHT and self.right == True):
            return True
        elif (opening_location == GamePiece.BOTTOM and self.bottom == True):
            return True
        elif (opening_location == GamePiece.LEFT and self.left == True):
            return True
        elif (opening_location == GamePiece.NONE and self.is_sink_source()):
            return True
        else:
            return False

    """ is_valid()
        Description: returns true for valid pieces (pieces with 2 openings) and
        false otherwise 
    """
    def is_valid(self):
        if ((int(self.top) + int(self.right) + int(self.bottom) + int(self.left)) == 2):
            return True
        else: 
            return False

    def is_sink_source(self):
        if ((int(self.top) + int(self.right) + int(self.bottom) + int(self.left)) == 1):
            return True
        else: 
            return False



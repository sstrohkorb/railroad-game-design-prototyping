import copy

'''def get_children_locations(i, j, grid) where grid should be a distance map'''
def get_children_locations(i, j, grid):
    #i is the row, j is the column of the grid location (the "parent")
    num_rows = len(grid)
    num_columns = len(grid[0])
    child_list = []
    # entry above
    if (i - 1 >= 0):
        if ((grid[i - 1][j] + 1 == grid[i][j]) and grid[i - 1][j] != -1):
            child_list.append((i - 1, j))
    # entry to the right
    if (j + 1 < num_columns):
        if ((grid[i][j + 1] + 1 == grid[i][j]) and grid[i][j + 1] != -1):
            child_list.append((i, j + 1))
    # entry to the bottom
    if (i + 1 < num_rows):
        if ((grid[i + 1][j] + 1 == grid[i][j]) and grid[i + 1][j] != -1):
            child_list.append((i + 1, j))
    # entry to the left
    if (j - 1 >= 0):
        if ((grid[i][j - 1] + 1 == grid[i][j]) and grid[i][j - 1] != -1):
            child_list.append((i, j - 1))
    #below: extending child_list with entries of -2 if child_list does not have 4 children. most don't.
    # if len(child_list) != 4:
    # 	child_list.extend((4 - len(child_list)) * [-2])
    #function returns a list of child locations, so a list of TUPLES
    return child_list

'''class "Node" helps build a recursive tree object for the paths, which can be transversed to get list of all paths from a space'''
class Node(object):
    class_var = [] #class variable (as opposed to object variable) needed for computation below

    def __init__(self, info):
        self.info = info
        self.child1 = None
        self.child2 = None
        self.child3 = None
        self.child4 = None
               
    def build_tree(self, grid):
        children = get_children_locations(self.info[0], self.info[1], grid)
        # #child 1
        # if children[0] == -2:
        #     self.child1 = None
        # else:
        #     self.child1 = Node(children[0]).build_tree(grid)
        # #child 2
        # if children[1] == -2:
        #     self.child2 = None
        # else:
        #     self.child2 = Node(children[1]).build_tree(grid)
        # #child 3
        # if children[2] == -2:
        #     self.child3 = None
        # else:
        #     self.child3 = Node(children[2]).build_tree(grid)
        # #child 4
        # if children[3] == -2:
        #     self.child4 = None
        # else:
        #     self.child4 = Node(children[3]).build_tree(grid)

        for i in range(len(children)):
            if (i == 0):
                self.child1 = Node(children[i]).build_tree(grid)
            elif (i == 1):
                self.child2 = Node(children[i]).build_tree(grid)
            elif (i == 2):
                self.child3 = Node(children[i]).build_tree(grid)
            elif (i == 3):
                self.child4 = Node(children[i]).build_tree(grid)

        return self
    
    def is_leaf(self):
        if self.child1 is None and self.child2 is None:
            return True
        else:
            return False
    
    def class_var_init(self):
        Node.class_var = []
    
    '''traverses graph and gives us information for every path. however, output is not in format we want.'''
    def preorder(self): 
        if self is not None:
            Node.class_var.append(self.info)
            if self.is_leaf() == True:
                Node.class_var.append("BREAK")
            if self.child1 is not None:
                self.child1.preorder()
            if self.child2 is not None:
                self.child2.preorder()
            if self.child3 is not None:
                self.child3.preorder()
            if self.child4 is not None:
                self.child4.preorder()
        return Node.class_var

    '''get_path_matrix takes the output of tree traversal function 'preorder' and cleans it up into path_matrix'''
    def get_path_matrix(self): 
        self.class_var_init() 
        traversal_list = self.preorder() #get the output of 'preorder'
        #below: get indexs where "BREAK" occurs so we know how to splice list
        break_indexs = []
        traversal_list_enum = list(enumerate(traversal_list))
        for i in traversal_list_enum:
            if i[1] == 'BREAK':
                break_indexs.append(i[0])
        break_indexs.sort()
        #chop_list is the 'preorder' output formatted into a list of path ending sequences
        chop_list = [] 
        for i in range(len(break_indexs)):
            if i == 0:
                start = 0
            else:
            	start = (break_indexs[(i-1)]) + 1
            end = break_indexs[i]
            chunk = traversal_list[start:end]
            chop_list.append(chunk)
        #indexs_of_chops_list[i] is list of indexs of 'chop_list' which affect value of path_matrix[i]
        indexs_of_chops_list = [] 
        for i in range(len(chop_list)):
            val_list = []
            lenval = len(chop_list[i])
            for h in range(i-1, -1, -1):
                if len(chop_list[h]) > lenval:
                       val_list.append(h)
                       lenval = len(chop_list[h])
            val_list.insert(0, i)
            val_list.sort(reverse = True)
            indexs_of_chops_list.append(val_list)
        #below secion puts 'chops' together to form correct path matrix
        path_matrix = len(chop_list) * [len(chop_list[0]) * [0]] #initializing path matrix at right size
        for i in range(len(indexs_of_chops_list)): 
            ending = []
            for j in range(len(indexs_of_chops_list[i])):
                if j == 0:
                    ending = chop_list[((indexs_of_chops_list[i])[j])]
                elif (j != 0):
                    new = chop_list[((indexs_of_chops_list[i])[j])]
                    ending = new[:(len(new)-len(ending))] + ending
            path_matrix[i] = ending
        #empty out class_var and return the complete path_matrix
        self.class_var_init()
        return path_matrix     
'''For your attention: Node class ENDS here. functions below are not bound to Node Class'''

'''function get_paths_list is outside of class "Node". It makes use of the class to get the path matrix, and outputs the 
    list of paths, but you do not have to "know about" the class to use the function. Returns path_matrix'''
def get_paths_list(i, j, grid, heatmap): 
    if heatmap[i][j] == 1:
        x = Node((i,j))
        tree = x.build_tree(grid)
        path_matrix = tree.get_path_matrix()
        return path_matrix   
    else:
        #print('Not a valid space. The (i,j) you chose does not fall on any minimum path from start to finish.')
        return None 

''' given lists a and b, function tells you if they intersect, but does not check first and last element, 
    because those always intersect in our path_matrix. Returns True or False'''
def do_lists_intersect(a, b):
	val = False
	#if (type(a) is list) and (type(a[0]) is tuple) and (type(b) is list) and (type(b[0]) is tuple):
	intersect_indexs = []
	for i in range(1, (len(a) - 1)):
		if a[i] == b[i]:
			val = True
			intersect_indexs.append(i)
	return val
	#else:
		#print "TYPE ERROR IN LIST INTERSECTION TEST"
		#return None

'''returns a list. each element is a 2-tuple of two rows (actually 'paths') in path_matrix that do not intersect.'''
def get_indep_paths(i, j, grid, heatmap):
    path_matrix = get_paths_list(i, j, grid, heatmap)
    index_pairs_of_indep_paths = []
    indep_paths = []
    #index_pairs_of_intersecting_paths = [] 
    for i in range(len(path_matrix)):
        current = path_matrix[i]
        for j in range((i + 1), len(path_matrix)):
            test = path_matrix[j]
            if do_lists_intersect(current, test) == False:
                indep_paths.append((current, test))
                index_pairs_of_indep_paths.append([i,j])
            else:
                #index_pairs_of_intersecting_paths.append([i,j])
                pass
    return indep_paths

'''tests if the point i,j is a point of no return'''
def is_point_of_NR(i, j, grid, heatmap):
	indep_paths_list = get_indep_paths(i, j, grid, heatmap)
	if len(indep_paths_list) >= 1:
		return True
	else:
		return False

'''returns a board with the points of no return labeled 1, all else labeled 0'''
def get_NR_board(grid, heatmap):
    nr_board = [ [ 0 for i in range(len(grid[0])) ] for j in range(len(grid)) ] #initializing nr_board
    nr_indexs = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if heatmap[i][j] == 1:
                if is_point_of_NR(i, j, grid, heatmap) is True:
                    nr_indexs.append((i,j))
    for i in nr_indexs:
        x = i[0]
        y = i[1]
        nr_board[x][y] = 1
    return nr_board

'''flow_direc takes in two ordered pairs, these ordered pairs being two spaces next to each other on a path, and 
   returns the flow from the first to second tuple'''
def flow_direc(tuple1, tuple2):
    y0, x0 = tuple1[0], tuple1[1]
    y1, x1 = tuple2[0], tuple2[1]
    flow = None
    if y1 == y0:
        if x1 - x0 == 1:
            flow = 'r'
        if x1 - x0 == -1:
            flow = 'l'
    elif x1 == x0:
        if y1 - y0 == 1:
            flow = 'd'
        if y1 - y0 == -1:
            flow = 'u'
    return flow

'''turns a path from list of locations to list of pieces'''
def get_piecelist_from_path(path):
    piecelist = []
    for i in range(1, len(path)-1):
        a0 = path[i -1]
        a1 = path[i]
        a2 = path[i + 1]
        piece = ''
        inflow = flow_direc(a1, a0)
        outflow = flow_direc(a1, a2)
        flowset = set([inflow, outflow])
        if flowset == set(['r', 'l']): piece = 'hz'
        if flowset == set(['r', 'u']): piece = 'NE'
        if flowset == set(['r', 'd']): piece = 'SE'
        if flowset == set(['u', 'l']): piece = 'NW'
        if flowset == set(['d', 'l']): piece = 'SW'
        if flowset == set(['u', 'd']): piece = 'vt'
        piecelist.append(piece)
    return piecelist

'''function below gets matrix of all paths from point to end, but this time the 
   elements in the paths are the game pieces played not the locations of the spaces'''
def get_piece_matrix(i, j, grid, heatmap):
    paths = get_paths_list(i, j, grid, heatmap)
    piece_matrix = [ [ 0 for i in range(len(paths[0])) ] for j in range(len(paths)) ] #initializing piece_matrix
    for i in range(len(paths)):
        pieceholder = get_piecelist_from_path(paths[i])
        piece_matrix[i] = copy.copy(pieceholder)
        pieceholder = []
    return piece_matrix

'''function below finds all pairs of paths, where the two paths have a different piece at every index'''
def get_strong_indep_paths_piecewise(i, j, grid, heatmap):
    piece_matrix = get_piece_matrix(i, j, grid, heatmap)
    index_pairs_of_indep_pieces = []
    indep_piece_lists = []
    #index_pairs_of_intersecting_paths = [] 
    for i in range(len(piece_matrix)):
        current = piece_matrix[i]
        for j in range((i + 1), len(piece_matrix)):
            test = piece_matrix[j]
            val = False
            for t in range(len(current)):
                if current[t] == test[t]: 
                    val = True
            if val is False:
                indep_piece_lists.append((current, test))
                index_pairs_of_indep_pieces.append([i,j])
    return indep_piece_lists             
            

'''function below finds all pairs of paths, where the two paths have a different final piece'''
def get_weak_indep_paths_piecewise(i, j, grid, heatmap):
    piece_matrix = get_piece_matrix(i, j, grid, heatmap)
    index_pairs_of_indep_pieces = []
    indep_piece_lists = []
    #index_pairs_of_intersecting_paths = [] 
    for i in range(len(piece_matrix)):
        current = piece_matrix[i]
        for j in range((i + 1), len(piece_matrix)):
            test = piece_matrix[j]
            val = False
            if current[-1] == test[-1]: 
                val = True
            if val is False:
                indep_piece_lists.append((current, test))
                index_pairs_of_indep_pieces.append([i,j])
    return indep_piece_lists

#BELOW IS FUNCTION MOVED FROM OTHER FILE "get_path_map"
'''
def get_path_map(distance_grid):
    #initialize path_map to all 1's
    path_map = [[1 for i in range(len(distance_grid))] for i in range(len(distance_grid[0]))]
    changes_being_made = True
    while (changes_being_made):
        changes_being_made = False
        #iterating over all matrix entries
        for i in range(len(path_map)):
            for j in range(len(path_map[0])):
                childlist = get_children_locations(i,j,distance_grid)
                #path_map parent value is equal to sum of path_map childs values
                # Sarah: this following statement is unnecessary
                if (1 <= len(childlist) and len(childlist) <= 4):       # Sarah: Originally (1 <= len(childlist) =< 4) - wrong
                    #val equals sum of child values
                    val = 0
                    for z in childlist:
                    	one = z[0]
                    	two = z[1]
                    	val = val + path_map[one][two]
                    if path_map[i][j] != val:
                    	path_map[i][j] = val
                    	changes_being_made = True
    #function returns array path_map with now the correct values
    return path_map
    #is it a problem that the "sink" is a 1 instead of a 0 in the path_map?
'''



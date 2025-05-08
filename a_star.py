import numpy as np
from copy import deepcopy

class AStar:


    def __init__(self, binary_map):

        #  convert map from dataframe into iterable matrix
        self.binary_map = binary_map

        #  define start and end points
        self.flags = [255, -255]



    #  this method updates the instance updates the global_score_map class variable, which characterizes each map cell
    @classmethod
    def update_global_score_map(cls, global_score_map):
        cls.global_score_map=global_score_map



    #  build kernel that isolates the cells immediately surrounding the focus cell
    def get_kernel_coords(self, cell:tuple):

        #  input cell is the focus cell's index coordinates (row, col)

        top_left = (cell[0]-1, cell[-1]-1)
        top = (cell[0]-1, cell[-1])
        top_right = (cell[0]-1, cell[-1]+1)


        left = (cell[0], cell[-1]-1)
        center = (cell[0], cell[-1])
        right = (cell[0], cell[-1]+1)

        
        bottom_left = (cell[0]+1, cell[-1]-1)
        bottom = (cell[0]+1, cell[-1])
        bottom_right = (cell[0]+1, cell[-1]+1)

        
        kernel = [
            [top_left, top, top_right],
            [left, center, right],
            [bottom_left, bottom, bottom_right]
        ]

        return kernel
    


    def init_score_map(self):

        #  g: score from starting cell
        #  h: score from destination cell
        #  f = g + h

        score_map=deepcopy(self.binary_map)

        #  iterate through each cell index
        for row_idx, row in enumerate(self.binary_map):
            for col_idx, val in enumerate(row):


                cell_score = dict(
                    explored=False,
                    global_coord = (row_idx, col_idx),
                    cell_val=val,
                    g = 0, 
                    h = 0,
                    f = 0
                    )
                            
                score_map[row_idx][col_idx]=cell_score

        return score_map



    #  characterize binary map flags
    def get_flag_indices(self):

        flag_indices=dict()

        #  iterate through each cell index
        for row_idx, row in enumerate(self.binary_map):
            for col_idx, col_val in enumerate(row):

                #  check the current cell for a flag value
                for flag in self.flags:
                    if col_val==flag:
                        flag_indices[flag]=(row_idx,col_idx)

        return flag_indices
    


    @staticmethod
    def get_euclidean_distance(point_1:tuple, point_2:tuple):

        euclid_dist = np.sqrt((point_1[0]-point_2[0])**2+(point_1[-1]-point_2[-1])**2)

        return euclid_dist
    


    #  distance to origin cell
    def get_g_score(self, current_pos:tuple, focus_cell_pos:tuple):

        focus_cell_g_score = self.global_score_map[focus_cell_pos[0]][focus_cell_pos[-1]]['g']

        point_1 = current_pos
        point_2 = focus_cell_pos

        #  calculate the equclidean distance between the current position index coords and the origin index coords
        euclid_distance = self.get_euclidean_distance(point_1, point_2)

        #  calculate the g_score
        g_score = int(euclid_distance*10)+focus_cell_g_score
        
        return g_score



    #  distance to end cell
    def get_h_score(self, current_pos:tuple, flag_indices:dict):
        #  flag indices are the index coordinates of the flags in the binary map, input as a tuple in the form of (row, col)

        point_1 = current_pos
        point_2 = flag_indices[-255]

        #  calculate the equclidean distance between the current position index coords and the destination index coords
        euclid_distance = self.get_euclidean_distance(point_1, point_2)

        #  calculate the h_score
        h_score = int(euclid_distance*10)
        
        return h_score

    

    #  isolate only kernel cells on global map
    def get_kernel_cells(self, kernel_coords):

        kernel_scores = []
        for row in kernel_coords:

            row_data = []
            for coord in row:
                val = self.global_score_map[coord[0]][coord[-1]]
                row_data.append(val)

            kernel_scores.append(row_data)

        return kernel_scores



    def get_kernel_min(self, kernel):

        min_coord = [0, 0]
        min_val = kernel[min_coord[0]][min_coord[-1]]['f']

        for row_idx, row in enumerate(kernel):
            for col_idx, col in enumerate(row):


                cell_val=col['cell_val']

                #  ignore obstacle cells
                if cell_val==1:
                    continue

                #  skip the focus_cell in kernel
                if row_idx ==1 and col_idx==1:
                    continue


                #  cell_score
                score = col['f']
                if score<min_val:
                    min_coord=[row_idx, col_idx]
                    min_val=score

        return min_coord
    


# --- DEV TOOLS ---

    def get_isolated_key_view(self,dict_key):

        isolated_data = []
        for row in self.global_score_map:
            row_data = [col[dict_key] for col in row]
            isolated_data.append(row_data)

        return isolated_data
    

    @staticmethod
    def view_score_matrix(kernel):

        kernel_scores = []

        for row_idx, row in enumerate(kernel):
            row_scores=[]

            for col_idx, col in enumerate(row):

                score = col['f']
                row_scores.append(score)


            kernel_scores.append(row_scores)

        return kernel_scores
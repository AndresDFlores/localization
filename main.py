import pandas as pd
from a_star import *


# import obstacle map

#  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
for sheet_num in [9]:

    print(f'SHEET{sheet_num}')
    
    #  load map
    map = pd.read_excel(r'map.xlsx', sheet_name=f'Sheet{sheet_num}')
    map_dims = map.shape



    #  initialize class
    binary_map = [map.iloc[idx].tolist() for idx in range(map.shape[0])]
    a_star_class = AStar(binary_map)


    # interpret global map and identify key locations
    flag_indices = a_star_class.get_flag_indices()  # 255: origin | -255: destination


    #  init global score map (MAY DELETE)
    global_score_map = a_star_class.init_score_map()
    a_star_class.update_global_score_map(global_score_map)


    #  initialize variables
    arrived_at_destination = False
    iter = 0

    focus_cell = flag_indices[255]  # this is the start cell index coordinate



    #  ---  ALGORITHM  ---
    while True:
    # while iter<2:


        print('\n')

    
        #  'close' the focus cell
        a_star_class.closed_cells.append(focus_cell)
        a_star_class.global_score_map[focus_cell[0]][focus_cell[-1]]['cell_open'] = False

        
        #  confirm that the focus cell is either open (0) or destination (-255)
        focus_cell_val = a_star_class.binary_map[focus_cell[0]][focus_cell[-1]]
        

        #  break out of algorithm if focus_cell is the destination flag
        if focus_cell_val == -255:
            summary=f'\nARRIVED AT {focus_cell} IN {iter} STEPS\n\n'
            print(summary)
            break


        print(f'\nITER: {iter}')
        print(f'FOCUS: {focus_cell}')
        print('\n')


        #  relate the nxn cost kernel to the global map cells' coordinates
        kernel_coords = a_star_class.get_kernel_coords(cell=focus_cell)


        #  --- iterate through kernel
        for kernel_row_idx, kernel_row in enumerate(kernel_coords):
            for kernel_col_idx, _ in enumerate(kernel_row):

                print('\n')

                #  get global map cell coordinates associated from kernel cell
                global_map_coord = kernel_coords[kernel_row_idx][kernel_col_idx]


                #  get global map cell value (0, -1, 255, -255) for kernel cells
                global_map_cell = a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]
                global_map_cell_val = global_map_cell['cell_val']


                #  distance from neighbor cell to origin cell
                g_score = a_star_class.get_g_score(
                    current_pos=global_map_coord, 
                    focus_cell_pos=focus_cell)
                

                #  distance from neighbor cell to destination cell
                h_score = a_star_class.get_h_score(
                    current_pos=global_map_coord, 
                    flag_indices=flag_indices)
                
                
                #  f = g+h
                f_score = g_score+h_score


                #  demo view - DELETE
                print(f'\tKernel Coord: {global_map_coord}')
                print(f'\tCell Value: {global_map_cell_val}')
                print(f'\tG: {g_score}')
                print(f'\tH: {h_score}')
                print(f'\tF: {f_score}')
                

                #  skip cell if it was previously explored and it already had a lower g_score
                if global_map_cell['cell_explored']:

                    g_prior = a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]['g']
                    if g_prior<-g_score:
                        continue


                #  record kernel_scores in dictionary
                a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]['cell_explored']=True
                a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]['kernel_parent_global_coord']=focus_cell
                a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]['g']=g_score
                a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]['h']=h_score
                a_star_class.global_score_map[global_map_coord[0]][global_map_coord[-1]]['f']=f_score
                

        #  --- identify the next focus kernel

        # isolate only kernel cells on global map
        kernel_global_cells = a_star_class.get_kernel_cells(kernel_coords)

        # save the kernel of explored cells built around the focus cell
        a_star_class.global_score_map[focus_cell[0]][focus_cell[-1]]['kernel_neighbors'] = kernel_global_cells

        # identify kernel cell with the min F score
        kernel_min_score_cell = a_star_class.get_kernel_min(kernel=kernel_global_cells)

        # relate kernel min F cell coord to the global coord
        focus_cell = kernel_global_cells[kernel_min_score_cell[0]][kernel_min_score_cell[-1]]['cell_global_coord']

        # increment iter
        iter+=1


    #  ---  dev visualizations
    print('\n')


    #  --- get miniumum score from open and explored cells
    isolated_data = []
    for row in a_star_class.global_score_map:

        row_data=[]
        for col in row:
            if col['cell_open']==True and col['cell_explored']==True:
                row_data.append(col['f'])
            else:
                row_data.append(None)

        isolated_data.append(row_data)

    print(pd.DataFrame(isolated_data))



    # #  ---  display a dict key in matrix
    # isolated_data_key = a_star_class.get_isolated_key_view(dict_key='f')
    # print(pd.DataFrame(isolated_data_key))



    # #  --- plot path
    # a_star_class.plot_map_path(title=summary)
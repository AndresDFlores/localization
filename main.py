import pandas as pd
from a_star import *


# import obstacle map

#  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
for sheet_num in [0]:

    print(f'SHEET{sheet_num}')
    
    #  load map
    map = pd.read_excel(r'maps.xlsx', sheet_name=f'Sheet{sheet_num}')
    map_dims = map.shape



    #  initialize class
    binary_map = [map.iloc[idx].tolist() for idx in range(map.shape[0])]
    a_star_class = AStar(binary_map)


    # interpret global map and identify key locations
    a_star_class.get_flag_indices()  # 255: origin | -255: destination


    #  init global score map (MAY DELETE)
    global_score_map = a_star_class.init_score_map()
    a_star_class.update_global_score_map(global_score_map)


    #  initialize variables
    arrived_at_destination = False
    iter = 0

    focus_cell = a_star_class.flag_indices[255]  # this is the start cell index coordinate



    #  ---  ALGORITHM  ---
    while True:

        print('\n')

    
        #  'close' the focus cell
        a_star_class.global_score_map[focus_cell[0]][focus_cell[-1]]['cell_open'] = False

        
        #  confirm that the focus cell is either open (0) or destination (-255)
        focus_cell_val = global_score_map[focus_cell[0]][focus_cell[-1]]['cell_val']
        

        #  break out of algorithm if focus_cell is the destination flag
        if focus_cell_val == -255:
            break


        print(f'\nITER: {iter}')
        print(f'FOCUS: {focus_cell}')
        print('\n')


        #  relate the nxn cost kernel to the global map cells' coordinates
        kernel_coords = a_star_class.get_kernel_coords(cell=focus_cell)
        print(kernel_coords)


        #  --- iterate through kernel
        for kernel_row_idx, kernel_row in enumerate(kernel_coords):
            for kernel_col_idx, _ in enumerate(kernel_row):

                print('\n')

                #  get global map cell coordinates associated from kernel cell
                global_cell_coord = kernel_coords[kernel_row_idx][kernel_col_idx]


                #  get global map cell value (0, -1, 255, -255) for kernel cells
                global_map_cell = a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]
                global_map_cell_val = global_map_cell['cell_val']


                #  skip inaccessible cells from scoring
                if global_map_cell_val==1:
                    continue


                #  distance from neighbor cell to origin cell
                g_score = a_star_class.get_g_score(
                    current_pos=global_cell_coord, 
                    focus_cell_pos=focus_cell)
                

                #  distance from neighbor cell to destination cell
                h_score = a_star_class.get_h_score(
                    current_pos=global_cell_coord, 
                    flag_indices=a_star_class.flag_indices)
                
                
                #  f = g+h
                f_score = g_score+h_score


                #  demo view - DELETE
                print(f'\tKernel Coord: {global_cell_coord}')
                print(f'\tCell Value: {global_map_cell_val}')
                print(f'\tG: {g_score}')
                print(f'\tH: {h_score}')
                print(f'\tF: {f_score}')
                

                #  skip cell if it is already closed
                if global_map_cell['cell_open'] is False:
                    continue


                #  skip cell if it was previously explored and it already had a lower g_score
                if global_map_cell['cell_explored']:

                    g_prior = a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]['g']
                    if g_prior<=g_score:
                        continue


                #  record kernel_scores in dictionary
                a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]['cell_explored']=True
                a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]['kernel_parent_global_coord']=focus_cell
                a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]['g']=g_score
                a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]['h']=h_score
                a_star_class.global_score_map[global_cell_coord[0]][global_cell_coord[-1]]['f']=f_score



        #  --- identify the next focus kernel

        #  isolate only kernel cells on global map
        kernel_global_cells = a_star_class.get_kernel_cells(kernel_coords)

        #  save the kernel of explored cells built around the focus cell
        a_star_class.global_score_map[focus_cell[0]][focus_cell[-1]]['kernel_neighbors'] = kernel_global_cells


        #  update open cells queue
        a_star_class.update_open_list()


        #  identify open cell on global map with the min F score
        next_cell = a_star_class.get_open_cells_min()
        score = next_cell['f']
        focus_cell = next_cell['cell_global_coord']


        #  increment iter
        iter+=1



    #  get final path
    a_star_class.get_final_path()


    #  --- DEV plot path

    df = a_star_class.get_isolated_key_view(dict_key='h')
    df = pd.DataFrame(df)
    df.to_excel('h.xlsx')

    df = a_star_class.get_isolated_key_view(dict_key='g')
    df = pd.DataFrame(df)
    df.to_excel('g.xlsx')

    df = a_star_class.get_isolated_key_view(dict_key='f')
    df = pd.DataFrame(df)
    df.to_excel('f.xlsx')

    df = a_star_class.get_isolated_key_view(dict_key='cell_global_coord')
    df = pd.DataFrame(df)
    df.to_excel('coords.xlsx')

    summary=f'\nARRIVED AT {a_star_class.final_path[-1]} IN {len(a_star_class.final_path)-1} STEPS\n\n'
    a_star_class.plot_map_path(title=summary)

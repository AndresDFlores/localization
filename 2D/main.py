import pandas as pd
from trilateration_localization import *


df = pd.read_excel('coords.xlsx')


for row_idx, row in df.iterrows():

    trilat_localization_class = TrilaterationLocalization(iter=row_idx)

    (r1, a1, b1) = (
        df['dist1'][row_idx],
        df['anchor1_x'][row_idx],
        df['anchor1_y'][row_idx]
    )

    (r2, a2, b2) = (
        df['dist2'][row_idx],
        df['anchor2_x'][row_idx],
        df['anchor2_y'][row_idx]
    )

    (r3, a3, b3) = (
        df['dist3'][row_idx],
        df['anchor3_x'][row_idx],
        df['anchor3_y'][row_idx]
    )

    anchor_defs = [
        (r1, a1, b1), 
        (r2, a2, b2), 
        (r3, a3, b3)
    ]


    trilat_localization_class.main(anchor_defs, title=row_idx)
    
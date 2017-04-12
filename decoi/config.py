import copy

### config for 153xx

people_num = 35

row_length = 6
col_length = 6

seat_seed = []
for row in range(row_length):
    for col in range(col_length):
        seat_seed = seat_seed + [(row, col)]
seat_seed.remove((5,0))
seat_seed = seat_seed


## cheat of class members

def cheat_dict(seat_to, seat_from):
    return {"seat_to":copy.copy(seat_to), "seat_from":copy.copy(seat_from)}

front = [(0,1),(0,2),(0,3),(0,4)]
fronter = [(1,0)]

side = [(2,0),(3,0),(2,5),(3,5)]
sider = [(1,5)]


#candidate

cheat_list = [
    cheat_dict(front, fronter),
    cheat_dict(side, sider),
    ]

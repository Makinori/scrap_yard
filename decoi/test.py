import random
import copy
from config import *
import gui as gui

### seats



### next seat
       
def next_seat_list (seat_seed, cheat_rule_list):
    seats_dict = []
    ago_seats = copy.copy(seat_seed)
    next_seats = copy.copy(seat_seed)

    # cheat

    for cheat in cheat_rule_list:
        # select to whom and where
        for to_whom in cheat['seat_from']:
            if(cheat["seat_to"]!=[]):
                # relocation to seat
                seat = random.choice(cheat["seat_to"])
                cheat["seat_to"].remove(seat)

                if (to_whom in ago_seats and seat in next_seats):
                    seats_dict = seats_dict + [{'ago':to_whom, 'next':seat}]
                    
                    ago_seats.remove(to_whom)
                    next_seats.remove(seat)
                else :
                    print("cheat is ignored : ")
                
        
    # normal suffle
    random.shuffle(next_seats)
    next_seats = next_seats


    for i in range(len(next_seats)):
        seats_dict = seats_dict + [{'ago':ago_seats[i] ,'next':next_seats[i]}]

    return seats_dict
    

def print_seats(seats):
    for i in next_seats:
        print("%s -> %s " % (i["ago"], i["next"]))

     
### cheat




next_seats = next_seat_list(seat_seed, cheat_list)
#print_seats(next_seats)



app = gui.SeatsChangeApp(seats=next_seats)
app.mainloop()




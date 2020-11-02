
from functools import reduce
import math

kanji_file_path = "./kanji-list.txt"

kanji_f = open(kanji_file_path, mode="r")
kanji_text = kanji_f.read()
kanji_f.close()


def list_to_2_tuple (lis, current=[]):
    if len(lis)<2 :
        return current
    else :
        return list_to_2_tuple(lis[2:],
                               current+[tuple(lis[:2])])
                               

def split_kanji(text):
    flatt_list = list(map(lambda c: c.replace(" ", ""),
                          reduce(lambda a,b: a+b,
                                 map(lambda l: l.split("|"), text.split("\n")))))
    tuple_list = list_to_2_tuple(flatt_list)
    return tuple_list


num_col = 7

def generate_list(kanji_tuple_list):
    text = "| "
    for row in range(math.ceil(len(kanji_tuple_list)/num_col)):
        for col in range(num_col):
            try:
                tuple= kanji_tuple_list[row*num_col+col]
                # c = tuple[0] + " " + tuple[1]
                c = "　" + "  " + "　"
            except:
                c = "       "
            text += c + "|"
        text += "\n|"
    return text[:-2]
    

splits = split_kanji(kanji_text)
print(generate_list(splits))



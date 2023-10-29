import json
import math
from pathlib import Path


from data import JsonDict


# sample path 1: "../data/sample_car.json"
# sample path 2: "../data/sample_bike.json"
def check_collision(obj1, obj2, speed1, speed2):
    if len([a for a in obj1 if a is not None]) <= 2:
        return False
    # with open(Path(file1_path), "r") as f:
    #     # load json file into file
    #     file1 = [json.load(f, object_hook=JsonDict)]
    #
    # with open(Path(file2_path), "r") as f:
    #     file2 = [json.load(f, object_hook=JsonDict)]

    # add all (x, y) position into the objects
    # obj1 = []
    # obj2 = []
    # for i in range(0, len(file1[0])):
    #     obj1 += [[file1[0][i]['position']['x'], file1[0][i]['position']['y']]]
    #
    # for i in range(0, len(file2[0])):
    #     obj2 += [[file1[0][i]['position']['x'], file1[0][i]['position']['y']]]

    #find the last and second last(x, y)
    # last_pos1 = obj1[len(obj1) - 1]
    # last_pos2 = obj2[len(obj2) - 1]

    # sec_last_pos1 = obj1[len(obj1) - 2]
    # sec_last_pos2 = obj2[len(obj2) - 2]

    # speed_last1 = [file1[0][len(file1[0]) - 1]['speed']['x'], file1[0][len(file1[0]) - 1]['speed']['y']]
    # speed_last2 = [file2[0][len(file1[0]) - 1]['speed']['x'], file2[0][len(file1[0]) - 1]['speed']['y']]
    # predict_pos1 = [last_pos1[0] + file1[0][len(file1[0]) - 1]['speed']['x'], last_pos1[1] + file1[0][len(file1[0]) - 1]['speed']['y']]

    speed_last1 = speed1
    speed_last2 = speed2

    vector1 = [obj1[0][-1]  - obj1[0][-2], obj1[1][-1]  - obj1[1][-2]]
    vector2 = [obj2[0][-1]  - obj2[0][-2], obj2[1][-1] - obj2[1][-2] ]

    # what 1 degree of latitude/longitude equal in meter
    convert = 111320
    # roughly convert latitude/longitude into meter
    vector1m = [vector1[0] * convert, vector1[1] * convert]
    vector2m = [vector2[0] * convert, vector2[1] * convert]

    # find unit vector of the last vector and times it with the speed vector
    unit_vector1 = [vector1m[0] / math.sqrt(vector1[0] ** 2 + vector1[1] ** 2), vector1m[1] / math.sqrt(vector1[0] ** 2 + vector1m[1] ** 2)]
    unit_vector2 = [vector2m[0] / math.sqrt(vector2[0] ** 2 + vector2[1] ** 2), vector2[1] / math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)]

    unit_vector1 = [unit_vector1[0] * speed_last1[0][0], unit_vector1[1] * speed_last1[1][0]]
    unit_vector2 = [unit_vector2[0] * speed_last2[0][0], unit_vector2[1] * speed_last2[1][0]]
    # add unit vectors to the last position vector
    vector1f = [vector1m[0] + unit_vector1[0], vector1m[1] + unit_vector1[1]]
    vector2f = [vector2m[0] + unit_vector2[0], vector2m[1] + unit_vector2[1]]

    # find the distance by distance formula
    distance = math.sqrt((vector2f[0] - vector1f[0]) ** 2 + (vector2f[1] - vector1f[0]) ** 2)
    if distance <= 2:
        collision = True
    else:
        collision = False
    return collision

# def main():
#     file1_path = "../data/sample_car.json"
#     file2_path = "../data/sample_bike.json"
#     collision = check_collision(file1_path, file2_path)
#     print(collision)
#
# main()









from data import parse_data
from prediction import Prediction
if __name__ == "__main__":
    print("start")
    car, map1 = parse_data('data/sample_car.json', 'data/sample_map.json')
    a = Prediction()
    a.update_engager(car)
    a.predict()
    print(a)


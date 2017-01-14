# coding=utf-8
import math

from app.common.constants import MAX_KM, KEROSENE_PRICE

# do not add dependency to CommercialPlane here, otherwise cyclic dependency
from app.common.target_strings import SUPERSONICS_MODELS_HTML, COMMERCIAL_MODELS_HTML, JETS_MODELS_HTML

COEFFICIENT = 0.8


def get_plane_value(new_plane_value, km, kerosene_qty):
    value = (MAX_KM - km) / float(MAX_KM) * new_plane_value
    value += kerosene_qty * KEROSENE_PRICE
    return int(value)


def duration_mission(distance, speed):
    return math.ceil(distance / float(speed))


def calculate_total_consumption_one_way(duration, conso_per_hour, passengers_nb, staff_nb):
    #TODO improve calculation
    # formula is flight_hours * (consumption_per_hour + 3*(passengers_nb+staff))*3/2
    # replacing time by distance/speed
    return duration * (conso_per_hour + 3 * (passengers_nb + staff_nb))


def calculate_real_autonomy_one_way(speed, kerosene_capacity, conso_per_hour, passengers_nb, staff_nb):
    max_duration = 0
    while calculate_total_consumption_one_way(max_duration, conso_per_hour, passengers_nb,
                                              staff_nb) * 3/2.0 < COEFFICIENT * kerosene_capacity:
        max_duration += 1
    return (max_duration - 1) * speed


def calculate_autonomy_with_stopover(speed, kerosene_capacity, conso_per_hour, passengers_nb, staff_nb):
    max_duration = 0
    while calculate_total_consumption_one_way(max_duration, conso_per_hour, passengers_nb,
                                              staff_nb) < COEFFICIENT * kerosene_capacity:
        max_duration += 1
    return (max_duration - 1) * speed

def is_supersonic(string_model):
    return string_model in SUPERSONICS_MODELS_HTML


def is_jet(string_model):
    return string_model in JETS_MODELS_HTML


def is_regular_plane(string_model):
    return string_model in COMMERCIAL_MODELS_HTML


if __name__ == '__main__':
    passengers_nb = 19
    staff_nb = 4

    plane_list = [
        {
            "name": "DS 7X",
            "speed": 922,
            "kerosene_capacity": 18050,
            "conso_per_hour": 1510},
        {
            "name": "GS 550",
            "speed": 904,
            "kerosene_capacity": 24000,
            "conso_per_hour": 1735},
        {
            "name": "CC",
            "speed": 2250,
            "kerosene_capacity": 119500,
            "conso_per_hour": 25625},
    ]

    for plane in plane_list:
        autonomy = calculate_real_autonomy_one_way(plane['speed'], plane['kerosene_capacity'], plane['conso_per_hour'], passengers_nb, staff_nb)
        autonomy2 = calculate_autonomy_with_stopover(plane['speed'], plane['kerosene_capacity'], plane['conso_per_hour'], passengers_nb, staff_nb)
        print("{}: {}".format(plane['name'], autonomy))
        print("{}: {}".format(plane['name'], autonomy2))


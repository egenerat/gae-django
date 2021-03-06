# -*- coding: utf-8 -*-

from app.planes.plane_maintainer import PlaneMaintainer


class PlaneGarage(object):
    def __init__(self, plane_list, airport):
        self.plane_list = plane_list
        self.airport = airport
        self.ready_planes = None
        self.refresh_needed = False

    def prepare_all_planes(self):
        temp_ready_planes = []
        for i in self.plane_list:
            plane_maintainer = PlaneMaintainer(i, self.airport)
            is_ready = plane_maintainer.prepare_plane()
            self.refresh_needed = self.refresh_needed or plane_maintainer.refresh_needed
            if is_ready:
                temp_ready_planes.append(i)
        self.ready_planes = temp_ready_planes

    def get_engines_needed_nb(self):
        result = {}
        for i in self.plane_list:
            if i.engines_to_be_changed():
                if i.replacement_engines_type in result:
                    result[i.replacement_engines_type] += i.engines_nb
                else:
                    result[i.replacement_engines_type] = i.engines_nb
        return result

    def get_kerosene_quantity_needed(self):
        result = 0
        for i in self.plane_list:
            if not i.is_fuel_full():
                result += i.fuel_capacity - i.kerosene
        return result

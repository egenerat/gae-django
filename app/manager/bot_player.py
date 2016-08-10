# coding=utf-8

from app.airport.airport_builder import build_airport
from app.airport.airport_checker import AirportChecker
from app.common.logger import logger
from app.common.http_methods import get_request
from app.common.target_urls import STAFF_PAGE, AIRPORT_PAGE, MISSION_DASHBOARD, PLANES_PAGE
from app.missions.missionparser import get_ongoing_missions, subtract
from app.parsers.planes_parser import build_planes_from_html
from app.planes.plane_garage import PlaneGarage
from app.planes.planes_util2 import split_planes_list_by_type
from fm.mission_handler import accept_all_missions


class BotPlayer(object):
    def __init__(self, missions):
        self.airport = self.build_airport()
        self.planes = self.build_planes()
        self.ongoing_missions = self.get_ongoing_missions()
        self.missions = missions
        logger.info('Airport {}'.format(self.airport.airport_name))

    def build_airport(self):
        staff_page = get_request(STAFF_PAGE)
        airport_page = get_request(AIRPORT_PAGE)
        return build_airport(airport_page, staff_page)

    def build_planes(self):
        html_page = get_request(PLANES_PAGE)
        planes_list = build_planes_from_html(html_page)
        sorted_planes = split_planes_list_by_type(planes_list)
        return sorted_planes

    def get_ongoing_missions(self):
        dashboard = get_request(MISSION_DASHBOARD)
        return get_ongoing_missions(dashboard)

    @property
    def usable_planes(self):
        return self.planes['commercial_ready_planes'] + self.planes['supersonic_ready_planes'] + self.planes[
            'jet_ready_planes']

    @property
    def maintenance_needed_planes(self):
        # should be improved to select only planes with status I
        temp = self.planes['commercial_planes'] + self.planes['supersonic_planes'] + self.planes[
            'jet_planes']
        return [plane for plane in temp if plane.required_maintenance or plane.endlife]

    def launch_missions(self):
        mission_list = self.missions
        ongoing_missions = self.ongoing_missions
        mission_list = subtract(mission_list, ongoing_missions)
        checker = AirportChecker(self.airport, self.planes)
        checker.fix()

        # be careful, also send planes to maintainance with status A
        garage = PlaneGarage(self.usable_planes + self.maintenance_needed_planes, self.airport)
        # garage.get_kerosene_quantity_needed()
        # garage.get_engines_needed_nb()
        # TODO reparse after buying new planes
        garage.prepare_all_planes()
        accept_all_missions(mission_list, garage.ready_planes)

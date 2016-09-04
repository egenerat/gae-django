# coding=utf-8

from app.airport.airports_methods import get_other_airports_id, filter_airports, switch_to_airport
from app.common.logger import logger
from app.manager.bot_player import BotPlayer
from fm.databases.database_django import db_get_ordered_missions_multi_type
from fm.mission_handler import are_missions_expired, parse_all_missions


class MultiAirportBot(object):
    def __init__(self):
        self.missions = self.get_missions()

    def start(self):
        other_airports = get_other_airports_id()
        other_airports = filter_airports(other_airports)
        # TODO mock
        # other_airports = ['122791']
        for airport_id in other_airports:
            switch_to_airport(airport_id)
            BotPlayer(self.missions).launch_missions()
            #
            # current_airport = Airport()
            # set_airport(current_airport)
            # current_airport.check()

    # TODO
    def get_missions(self):
        db_missions = db_get_ordered_missions_multi_type(210, '-reputation_per_hour')
        if len(db_missions) < 200 or are_missions_expired(db_missions):
            logger.warning('Refresh missions')
            parse_all_missions()
            db_missions = db_get_ordered_missions_multi_type(210, '-reputation_per_hour')
        return db_missions

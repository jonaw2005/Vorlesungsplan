# -*- coding: utf-8 -*-

'''
@author: codingWithJo   on the examples given by the Amazon Developer Console

@description: 
    This Alexa skill, "Vorlesungsplan," is designed to provide users with information about their lecture schedules. 
    It interacts with a timetable system to fetch and process lecture data, allowing users to inquire about the start 
    times of lectures for specific days or the next day. The skill uses the Alexa Skills Kit SDK for Python and 
    implements various intent handlers to manage user requests.
    Key Features:
    - Fetches and processes lecture schedule data from a specified URL.
    - Provides the start time of lectures for a specific day or the next day.
    - Handles user interactions using custom intents like "TomorrowIntent" and "DayIntent."
    - Includes error handling and debugging support for seamless user experience.
    The skill is built using the handler classes approach in the Alexa Skills Kit SDK, ensuring modularity and 
    maintainability. It leverages web scraping techniques to extract and organize timetable data, making it 
    accessible and user-friendly for Alexa users.

@updates: will probably be extended with more features in the future (e.g. more intents, more data, etc.)

@note: skills.json is required for the skill to work properly, it contains the interaction model for the skill and is deleted due to privacy reasons

@date: 19.03.2025
'''

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



#
#
#
class Timetable:

    def get_date(self):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        day = tomorrow.day
        month = tomorrow.month
        year = tomorrow.year

        return [day, month, year]

    def getHTML(self):
        date_list = self.get_date()
        day = date_list[0]
        month = date_list[1]
        year = date_list[2]
        
        url = "PASTE URL TO RAPLA HERE"

        # Send an HTTP GET request to the URL
        response = requests.get(url)
        html_content = response.text

        return html_content

    def extract_table_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        blocks = soup.find_all(class_="week_block")

        list_of_lists = []

        for block in blocks:
            data_final = ""
            data_list = []
            for x in block.findAll(string=True):
                data = str(x).strip()
                data_list.append(data)
                data_final = data_final + " | " + data

            list_of_lists.append(data_list)

        return list_of_lists

    def getUsefull(self, list_of_lists):

        list_of_final_lists = []

        for data_list in list_of_lists:

            title = data_list[1]

            person_index = data_list.index("Personen:")

            prof = data_list[person_index + 2]

            room_index = self.getRoomIndex(data_list)

            room_raw = data_list[room_index].split(", ")
            room = room_raw[0]

            time_raw = data_list[4]
            time_raw_list = time_raw.split(" ")

            if not time_raw_list.__contains__("wöchentlich"):
                dayname = time_raw_list[0]
                date = time_raw_list[1]
                time_pair = time_raw_list[2]
                time_pair_list = time_pair.split("-")
                # print(time_pair_list)
                start = time_pair_list[0]
                end = time_pair_list[1]
            else:
                dayname = time_raw_list[0]

                time_pair = time_raw_list[1]

                time_pair_list = time_pair.split("-")
                # print(time_pair_list)
                start = time_pair_list[0]
                end = time_pair_list[1]

            final_list = []
            final_list.append(title)
            final_list.append(dayname)
            final_list.append(start)
            final_list.append(end)
            final_list.append(prof)
            final_list.append(room)
            list_of_final_lists.append(final_list)
            # print(final_list)

        return list_of_final_lists

    def getRoomIndex(self, data_list):

        index = 0
        room = ""
        for x in data_list:
            if ", Hörsaal" in x:

                if len(x.split(",")) == 2:
                    index = data_list.index(x)
                    room = x
                    break

        return index

    def sortByDay(self, data_list):

        days_in_order = ['Mo', 'Di', 'Mi', 'Do', 'Fr']

        sorted_timetable = sorted(data_list, key=lambda x: days_in_order.index(x[1]))
        return sorted_timetable

    def sortByTime(self, data_list: list):
        sorted_list = []
        old_temp_list = []

        for x in data_list:
            if x in old_temp_list:
                old_temp_list = []
                continue
            templist = []
            index1 = data_list.index(x)

            if index1 == len(data_list) - 1:
                templist.append(x)
                sorted_list.append(templist)
                break

            if x[1] == data_list[index1 + 1][1]:
                start1 = x[2].split(":")[0]
                start2 = data_list[index1 + 1][2].split(":")[0]

                if int(start1) > int(start2):
                    templist.append(data_list[index1 + 1])
                    templist.append(x)
                elif int(start1) < int(start2):
                    templist.append(x)
                    templist.append(data_list[index1 + 1])
            else:
                templist.append(x)
            sorted_list.append(templist)

        return sorted_list

    def beautify(self, sorted_list):

        temp_list = []

        # normal len == 6

        for x in sorted_list:

            if type(x) is list:
                if len(x) == 6:
                    temp_list.append(x)

                else:
                    for y in x:
                        if type(y) is list:
                            if len(y) == 6:
                                if not y in temp_list:
                                    temp_list.append(y)
                            else:

                                for z in y:
                                    if type(z) is list:
                                        if len(z) == 6:
                                            if not z in temp_list:
                                                temp_list.append(z)

        return temp_list

    def getWeekData(self):
        date_list = self.get_date()
        html = self.getHTML()
        ex_data = self.extract_table_data(html)
        usefull = self.getUsefull(ex_data)
        sorted_by_day = self.sortByDay(usefull)
        sorted_by_time = self.sortByTime(sorted_by_day)
        weekData = self.beautify(sorted_by_time)

        return weekData

    def startTomorrow(self):
        weekData = self.getWeekData()

        today = datetime.today().strftime("%A")

        presentday = datetime.now()
        tomorrow = presentday + timedelta(1)

        tomorrow = tomorrow.strftime("%A")

        short = tomorrow[:2]

        if short == "Tu": short = "Di"
        if short == "We": short = "Mi"
        if short == "Th": short = "Do"

        for x in weekData:
            if short in x:
                return x[2]
                
    def start_Day(self, day):
        
        days_mapping = {
            "mo": "Mo",
            "di": "Di",
            "mi": "Mi",
            "do": "Do",
            "fr": "Fr"
        }
        day = days_mapping.get(day[:2].lower(), day.capitalize())
        
        weekData = self.getWeekData()
        
        for x in weekData:
            if day in x:
                return x[2]
#
#
#

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        
        speak_output = "Der Skill Vorlesungsplan wurde gestartet"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        logger.debug("Exception handle")
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class TomorrowIntentHandler(AbstractRequestHandler):
    """Handler for Tomorrow Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("TomorrowIntent")(handler_input)

    def handle(self, handler_input):
        
        t = Timetable()
        startTomorrow = t.startTomorrow()
        
        speak_output = f"Morgen fängt die Vorlesung um {startTomorrow} Uhr an" 
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class DayIntentHandler(AbstractRequestHandler):
    """Handler for Day Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DayIntent")(handler_input)
            
    def handle(self, handler_input):
        
        day = ask_utils.get_slot(handler_input, 'Tag').value
        
        t = Timetable()
        startTime = t.start_Day(day)

        speak_output = f"Am {day} fängt die Vorlesung um {startTime} Uhr an" 
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TomorrowIntentHandler())
sb.add_request_handler(DayIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
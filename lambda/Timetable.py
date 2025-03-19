# -*- coding: utf-8 -*-

'''
@author: codingWithJo
@description: This class is used to get the timetable for the requested day from the Rapla website of the University.
It uses the BeautifulSoup library to parse the HTML content of the website and extract the relevant information.

@usage:
1. Create an object of the class Timetable
2. Call the method getWeekData() to get the timetable for the whole week in json format
3. Call the method startTomorrow() to get the first lecture of the next day
4. Call the method start_Day(day) to get the first lecture of the requested day

@note: The URL of the Rapla website has to be pasted in the getHTML() method
@note: The HTML content maybe has to be filtered an other way, depending on the structure of the website
@note: To work not all of the requirements in requirements.txt are needed

@date: 19.03.2025
'''


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



class Timetable:

    def get_date(self):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        day = tomorrow.day
        month = tomorrow.month
        year = tomorrow.year

        return [day, month, year]

    def getHTML(self, date_list):
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
        blocks = soup.find_all(class_="week_block")  # , recursive=False)

        list_of_lists = []

        for block in blocks:
            data_final = ""
            data_list = []
            for x in block.findAll(string=True):
                data = str(x).strip()
                data_list.append(data)
                data_final = data_final + " | " + data

            # print(len(data_list))
            # print("4: ", data_list[4])
            # print("1: ", data_list[1])
            # print("43: ", data_list[43])
            # print("48: ", data_list[48])
            # print(data_final)
            list_of_lists.append(data_list)

        return list_of_lists

    def getUsefull(self, list_of_lists):

        list_of_final_lists = []

        # print(len(list_of_lists))
        for data_list in list_of_lists:

            title = data_list[1]

            person_index = data_list.index("Personen:")
            # print(person_index)
            # print(data_list[person_index+2])

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

                # print(title)
            # print(title)
            # final_list = {title, dayname, start, end, prof, room}
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
                    # print(x)
                    break

        return index

    def sortByDay(self, data_list):

        days_in_order = ['Mo', 'Di', 'Mi', 'Do', 'Fr']

        sorted_timetable = sorted(data_list, key=lambda x: days_in_order.index(x[1]))
        # print(sorted_timetable)
        return sorted_timetable

    def sortByTime(self, data_list: list):
        # print(type(data_list))
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

        # print(sorted_list)
        return sorted_list

    def beautify(self, sorted_list):

        temp_list = []

        # normal len == 6

        for x in sorted_list:

            if type(x) is list:
                # print("x",len(x))
                if len(x) == 6:
                    temp_list.append(x)

                else:
                    for y in x:
                        if type(y) is list:
                            # print("y",len(y))
                            if len(y) == 6:
                                if not y in temp_list:
                                    temp_list.append(y)
                            else:

                                for z in y:
                                    if type(z) is list:
                                        # print("z",len(z))
                                        if len(z) == 6:
                                            if not z in temp_list:
                                                temp_list.append(z)
                                        # print("wtf")
                                        '''
                                    else:
                                        temp_list.append([y])
                        else:
                            temp_list.append([x])
            else:
                #
                print("wtf2")
        '''
        #print(temp_list)
        return temp_list

    def getWeekData(self):
        date_list = self.get_date()
        html = self.getHTML(date_list)
        ex_data = self.extract_table_data(html)
        usefull = self.getUsefull(ex_data)
        #print(html)
        sorted_by_day = self.sortByDay(usefull)
        sorted_by_time = self.sortByTime(sorted_by_day)
        weekData = self.beautify(sorted_by_time)

        return weekData

    def startTomorrow(self):
        weekData = self.getWeekData()
        #print(weekData)
        today = datetime.today().strftime("%A")

        presentday = datetime.now()  # or presentday = datetime.today()

        # Get Yesterday

        # Get Tomorrow
        tomorrow = presentday + timedelta(1)

        # strftime() is to format date according to
        # the need by converting them to string

        tomorrow = tomorrow.strftime("%A")

        short = tomorrow[:2]

        if short == "Tu": short = "Di"
        if short == "We": short = "Mi"
        if short == "Th": short = "Do"

        for x in weekData:
            if short in x:
                return x[2]


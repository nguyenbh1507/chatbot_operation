import json
from dateutil.parser import parse
import datetime
from user_request import UserRequest
from convert_vietnamese import convert

class QueryFlight(object):
    def __init__(self):
        self.data = self.initialize_data()
        # self.result = None

    @staticmethod
    def initialize_data():
        with open("data/flight_database.json", "r", encoding="utf-8") as f:
            data = json.load(f)['Flight']
            return data

    @staticmethod
    def format_date(json_date):
        str_raw = f"{json_date['day']} {json_date['month']} {json_date['year']}  {json_date['hour']}:{json_date['min']}"
        datetime_object = datetime.datetime.strptime(str_raw, '%d %m %Y %H:%M')
        return datetime_object

    def get_flight_by_place(self, org_city, des_city):
        temp = []
        for item in self.data:
            if item["org_city"] == org_city and item["des_city"] == des_city:
                temp.append(item)
        self.data = temp

    def get_flight_by_budget(self, budget):
        temp = []
        for item in self.data:
            if item["ticket_price"]["Normal"] <= budget:
                temp.append(item)
        self.data = temp

    def get_flight_by_date(self, exact_date):
        temp = []
        exact_date = parse(exact_date)
        for item in self.data:
            departure = self.format_date(item["departure"])
            rule = [
                exact_date.day == departure.day,
                exact_date.month == departure.month,
                exact_date.year == departure.year
            ]
            if all(rule):
                temp.append(item)
        
        self.data = temp

    def get_flight_from_date_to_date(self, str_date=None, end_date=None):
        temp = []

        for item in self.data:
            arrival = self.format_date(item["arrival"])
            departure = self.format_date(item["departure"])
            if end_date is None and str_date:
                if str_date < departure:
                    temp.append(item)
            elif end_date and str_date:
                if str_date < departure and end_date > arrival:
                    temp.append(item)
            elif str_date is None and end_date:
                if end_date > arrival:
                    temp.append(item)
            else:
                continue

        self.data = temp

    def get_flight_by_user_request(self, user_request):
        exact_date = user_request.get_str_date
        org_city, des_city = user_request.get_place
        budget = user_request.get_budget

        self.get_flight_by_place(org_city, des_city)
        self.get_flight_by_date(exact_date)
        self.get_flight_by_budget(budget)

    def check_user_request(self):
        temp = []
        for item in self.data:
            if item['available_seat'] > 1:
                temp.append(item)

        if temp is not None:
            self.data = temp
            return True
        else: return False

    @property
    def get_result(self):
        return self.data

    def reset(self):
        self.data = self.initialize_data()



if __name__ == "__main__":
    queyr = QueryFlight()

    queyr.get_flight_by_place("sai gon", "ha noi")
    # queyr.get_flight_by_date(str_date="dec 2018")
    # queyr.get_flight_by_budget(1240000)
    print(queyr.get_result)
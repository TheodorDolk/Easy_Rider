import json
import re
from collections import Counter
from datetime import datetime
import time

def json_load():
    json_string = input()
    return json.loads(json_string)


class BusData:
    def __init__(self, json_objects):
        self.json_objects = json_objects

    # Step 2/6
    def name_type_time_fixer(self):
        stop_name_errors = 0
        stop_type_errors = 0
        a_time_errors = 0

        # patterns
        stop_name_pattern = re.compile('[A-Z][a-z]* ([A-Z][a-z]*)* ?(Road|Avenue|Boulevard|Street)')
        stop_type_pattern = re.compile(r'\b[SOF]\b|^$')
        a_time_pattern = re.compile(r"\b(?:0[0-9]|1[0-9]|2[0-3]):[0-5]\d\b")
        for dict_obj in self.json_objects:
            for key in dict_obj:
                value = dict_obj[key]

                # Stop name: Name of current stop, Type: String, Format: [name] [suffix]
                if key == "stop_name":
                    if isinstance(value, str):
                        if not stop_name_pattern.fullmatch(value):
                            stop_name_errors += 1
                            continue
                    else:
                        stop_name_errors += 1
                        continue
                    print(value)

                # Stop type: Character, Format: S or O or F
                elif key == "stop_type":
                    if isinstance(value, str):
                        if not stop_type_pattern.match(value):
                            stop_type_errors += 1
                    else:
                        stop_type_errors += 1

                # Arrival time: String, Format: 24 hour date, HH:MM
                elif key == "a_time":
                    if len(value) != 5:
                        a_time_errors += 1
                    elif isinstance(value, str):
                        if not a_time_pattern.match(value):
                            a_time_errors += 1
                    else:
                        a_time_errors += 1

        print(f"Format validation: {stop_name_errors + stop_type_errors + a_time_errors} errors")
        print(f"stop_name: {stop_name_errors}")
        print(f"stop_type: {stop_type_errors}")
        print(f"a_time: {a_time_errors}")

    # Step 3/6
    def count_bus_stops(self):
        bus_count_counter = Counter()
        for dict_obj in self.json_objects:
            for key in dict_obj:
                value = str(dict_obj[key])
                if key == "bus_id":
                    if value in bus_count_counter:
                        bus_count_counter[value] += 1
                    else:
                        bus_count_counter[value] = 1
        print("Line names and number of stops:")
        for bus_item in bus_count_counter.items():
            print(f"bus_id: {bus_item[0]}, stops: {bus_item[1]}")

    # Step 4/6
    def get_bus_dict(self):
        bus_dict = {}
        for dict_obj in self.json_objects:
            for key in dict_obj:
                if key == "bus_id":
                    id_number = str(dict_obj[key])
                    if id_number not in bus_dict.keys():
                        bus_dict[id_number] = []
                if key == "stop_name":
                    stop_name = dict_obj[key]
                if key == "stop_type":
                    stop_type = dict_obj[key]
                    bus_dict[id_number].append((stop_type, stop_name))
        for bus in bus_dict:
            if not bus_dict[bus][0][0] == "S":
                print(f"There is no start or end stop for the line: {bus}.")
                exit()
            if not bus_dict[bus][-1][0] == "F":
                print(f"There is no start or end stop for the line: {bus}.")
                exit()
        start_stops = set()
        transfer_stops = set()
        finish_stops = set()
        transfer_stops_counter = Counter()
        finish_stops_counter = Counter()
        for bus_number in bus_dict:
            for stop in bus_dict[bus_number]:
                if stop[0] == "S":
                    start_stops.add(stop[1])
                if stop[0] == "F":
                    finish_stops.add(stop[1])
                    finish_stops_counter[stop[1]] += 1

        for bus_number in bus_dict:
            for stop in bus_dict[bus_number]:
                if stop[0] == "O" or stop[0] == "":
                    if stop[1] in start_stops or stop[1] in transfer_stops or stop[1] in finish_stops:
                        transfer_stops.add(stop[1])
                    else:
                        transfer_stops_counter[stop[1]] += 1

        for item in transfer_stops_counter.items():
            if item[1] > 1:
                transfer_stops.add(item[0])
        for item in finish_stops_counter.items():

            if item[1] > 1:
                transfer_stops.add(item[0])
        print(f"Start stops: {len(start_stops)} {sorted(start_stops)}")
        print(f"Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}")
        print(f"Finish stops: {len(finish_stops)} {sorted(finish_stops)}")


def main():
    json_objects = json_load()
    bus_data = BusData(json_objects)
    start_time = time.time()
    bus_data.time_check()
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")


if __name__ == "__main__":
    main()

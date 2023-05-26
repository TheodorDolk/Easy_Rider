import json
import re
from collections import Counter


def json_load():
    json_string = input("")
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


def main():
    json_objects = json_load()
    bus_data = BusData(json_objects)
    bus_data.count_bus_stops()


if __name__ == "__main__":
    main()

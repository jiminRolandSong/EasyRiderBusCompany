from datetime import datetime
import json
import re

jsondicts = input()
pydicts = json.loads(jsondicts)

error_dict = {
    # "bus_id": 0,
    # "stop_id": 0,
    "stop_name": 0,
    # "next_stop": 0,
    "stop_type": 0,
    "a_time": 0
}


def stop_nameChecker(name):
    check = re.match(r'[A-Z](\w|\s[A-Z])* (Road|Avenue|Street|Boulevard)$', name)
    if not check:
        error_dict["stop_name"] += 1
    return ""


def stop_typeChecker(text):
    check = re.match(r'^[SOF]?$', text)
    if not check:
        error_dict["stop_type"] += 1
    return ""


def a_timeChecker(name):
    check = re.match(r'^([0-1]\d|2[0-4]):([0-5]\d)$', name)
    if not check:
        error_dict["a_time"] += 1
    return ""


def errorChecker():
    for dict in pydicts:
        for key in error_dict:
            if key == "stop_name":
                stop_nameChecker(dict[key])
            if key == "stop_type":
                stop_typeChecker(dict[key])
            if key == "a_time":
                a_timeChecker(dict[key])


def errorPrinter():
    total = 0
    for key in error_dict:
        total += error_dict[key]
    print("Format validation: {} errors".format(total))
    for key, value in error_dict.items():
        print("{}: {}".format(key, value))


# errorChecker()
# errorPrinter()

class bus_stop:
    def __init__(self, name, type):
        self.name = name
        self.type = type

def transferchecker():
    stops = {}
    transfers = []
    for dict in pydicts:
        name = dict["stop_name"]
        if name in stops:
            stops[name] += 1
        else:
            stops[name] = 1
    for key in stops:
        if stops[key] >= 2:
            transfers.append(key)
    return transfers
def stopchecker(buses):
    for key in buses:
        types = []
        for t in buses[key]:
            types.append(t.type)
        if "S" not in types or "F" not in types:
            print("There is no start or end stop for the line: {}".format(key))
            return False
    return True


def typechecker(buses):
    stops = {"Start stops": [], "Transfer stops": [], "Finish stops": []}
    for id in buses:
        for t in buses[id]:
            if t.type == "S" and t.name not in stops["Start stops"]:
                stops["Start stops"].append(t.name)
            if t.type == "F" and t.name not in stops["Finish stops"]:
                stops["Finish stops"].append(t.name)
    stops["Transfer stops"] = transferchecker()
    for stop in stops:
        print("{}: {} {}".format(stop, len(set(stops[stop])), sorted(stops[stop])))


def busstop():
    buses = {}
    for dict in pydicts:
        id = str(dict["bus_id"])
        stop_name = dict["stop_name"]
        stop_type = dict["stop_type"]
        if id in buses:
            buses[id] += [bus_stop(stop_name, stop_type)]
        else:
            buses[id] = [bus_stop(stop_name, stop_type)]
    check = stopchecker(buses)
    if(check):
        typechecker(buses)


#busstop()
# Task 5
def timetester(buses):
    okay = True
    for id in buses:
        for n in range(0,len(buses[id]) - 1):
            if buses[id][n][2] == "F":
                break
            if datetime.strptime(buses[id][n][1], "%H:%M").time() > datetime.strptime(buses[id][n + 1][1], "%H:%M").time() :
                print("bus_id line {}: wrong time on station {}".format(id, buses[id][n + 1][0]))
                okay = False
                break
    return okay
def time():
    buses = {}
    for dict in pydicts:
        id = str(dict["bus_id"])
        stop_name = dict["stop_name"]
        stop_type = dict["stop_type"]
        a_time = dict["a_time"]
        if id in buses:
            buses[id].append([stop_name, a_time, stop_type])
        else:
            buses[id] = [[stop_name, a_time, stop_type]]
    print("Arrival time test:")
    check = timetester(buses)
    if check:
        print("OK")
# time()


#task6
def demandtest(stops, on_demand):
    print("On demand stops test: ")
    okay = True
    wrong = []
    for stop in stops:
        for name in stops[stop]:
            print(name, on_demand)
            if name in on_demand:
                okay = False
                wrong.append(name)
    if okay:
        print("OK")
    else:
        print("Wrong stop type: {}".format(sorted(wrong)))
def demand_checker():
    buses = {}
    for dict in pydicts:
        id = str(dict["bus_id"])
        stop_name = dict["stop_name"]
        stop_type = dict["stop_type"]
        if id in buses:
            buses[id] += [bus_stop(stop_name, stop_type)]
        else:
            buses[id] = [bus_stop(stop_name, stop_type)]
    stops = {"Start stops": [], "Transfer stops": [], "Finish stops": []}
    on_demand = []
    for id in buses:
        for t in buses[id]:
            if t.type == "S" and t.name not in stops["Start stops"]:
                stops["Start stops"].append(t.name)
            if t.type == "F" and t.name not in stops["Finish stops"]:
                stops["Finish stops"].append(t.name)
            if t.type == "O":
                on_demand.append(t.name)
    stops["Transfer stops"] = transferchecker()
    demandtest(stops, on_demand)
demand_checker()
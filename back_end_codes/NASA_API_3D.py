import requests
from datetime import date, timedelta, datetime
import os
import json
# "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='499'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='2006-01-01'&STOP_TIME='2006-01-20'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'"


def get_API_data(Planet_name, date_import, asteroid = False):
    if date_import == "today":
        date_import = date.today()
    else:
        date_import = datetime.strptime(date_import, "%Y-%m-%d").date()
    date_import = str(date_import)
    
    # Get this py file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(f"{script_dir}", "API_data_folder")
    json_path = os.path.join(script_dir, "API_data_folder", "Planets_data.json")
    API_data = {}
    Planet_data = {}

    if not os.path.isdir(f"{script_dir}/API_data_folder"):
        # Create API folder
        json_path = os.path.join(script_dir, "API_data_folder", "Planets_data.json")
        os.makedirs(folder_path, exist_ok=True)
        print("API data folder created")
    
    if not os.path.exists(json_path):
        # Create Json fine
        API_data["Ephem_data"] = retrieve_Ephemeris_data(Planet_name, date_import)
        if asteroid == False:
            API_data["GM_data"] = retrieve_GM_data(Planet_name)
        Planet_data_from_file = {}
        Planet_data_from_file[date_import] = {}
        Planet_data_from_file[date_import][Planet_name] = {}
        Planet_data_from_file[date_import][Planet_name]["Ephemerides"] = API_data["Ephem_data"]
        if asteroid == False:
            Planet_data_from_file[date_import][Planet_name]["GM"] = API_data["GM_data"]
        with open(json_path, "w") as file:
            json.dump(Planet_data_from_file, file, indent = 2)
            print(f"Got {Planet_name} data from API")
        return API_data

    with open(json_path, "r") as file:
        # Check for data in json
        Planet_data_from_file = json.load(file)
        key_data = Planet_data_from_file.keys()
            
    if date_import not in key_data:
        API_data["Ephem_data"] = retrieve_Ephemeris_data(Planet_name, date_import)
        if asteroid == False:
            API_data["GM_data"] = retrieve_GM_data(Planet_name)
        Planet_data_from_file[date_import] = {}
        Planet_data_from_file[date_import][Planet_name] = {}
        Planet_data_from_file[date_import][Planet_name]["Ephemerides"] = API_data["Ephem_data"]
        if asteroid == False:
            Planet_data_from_file[date_import][Planet_name]["GM"] = API_data["GM_data"]
        with open(json_path, "w") as file:
            json.dump(Planet_data_from_file, file, indent = 2)
        print(f"Got {Planet_name} data from API")
        return API_data
    
    key_Planet_name = Planet_data_from_file[date_import].keys()

    if Planet_name not in key_Planet_name:
        API_data["Ephem_data"] = retrieve_Ephemeris_data(Planet_name, date_import)
        if asteroid == False:
            API_data["GM_data"] = retrieve_GM_data(Planet_name)
        Planet_data_from_file[date_import][Planet_name] = {}
        Planet_data_from_file[date_import][Planet_name]["Ephemerides"] = API_data["Ephem_data"]
        if asteroid == False:
            Planet_data_from_file[date_import][Planet_name]["GM"] = API_data["GM_data"]
        with open(json_path, "w") as file:
            json.dump(Planet_data_from_file, file, indent = 2)
        print(f"Got {Planet_name} data from API")
        return API_data
    
    API_data["Ephem_data"] = Planet_data_from_file[date_import][Planet_name]["Ephemerides"]
    if asteroid == False:
        API_data["GM_data"] = Planet_data_from_file[date_import][Planet_name]["GM"]
    print(f"Got {Planet_name} data from JSON file")
    return API_data


# Not used
def Planet_data_dict(Planet_name, date_import, Planet_data, asteroid = False):
    API_data = {}
    API_data["Ephem_data"] = retrieve_Ephemeris_data(Planet_name, date_import)
    if asteroid == False:
      API_data["GM_data"] = retrieve_GM_data(Planet_name)
    Planet_data[date_import][Planet_name]["Ephemerides"] = API_data["Ephem_data"]
    if asteroid == False:
        Planet_data[date_import][Planet_name]["GM"] = API_data["GM_data"]
    return Planet_data, API_data


# Get ephemerides fun
def retrieve_Ephemeris_data(Planet_name, date):
    AU = 149597870700 / 1000 #km
    content = Call_API_data(Ephem_API_key_construction(Planet_name, date))

    # Check for wrong name
    if "No matches found" in content["result"]:
        raise NameError(f"""\n!!!Error: Asteroid/comet named "{Planet_name}" NOT found in NASA database!!!""")
    if "Number of matches" in content["result"]:
        print(f"""\n!!!Error: Asteroid/comet named "{Planet_name}" WAS found in NASA database, but there are more than 1 objects with this name!!!
If you sure that "{Planet_name}" is the correct name, use the ID of the object insted of the name.
You can find the ID from the API result here.""")
        input("\nPrint smth to see the API result: ")
        raise NameError(f"{content["result"]}")

    
    start_index_1 = str.index(content["result"], "$$SOE")
    finish_index_1 = str.index(content["result"], "$$EOE")
    result = []
    keys = ["X", "Y", "Z", "VX", "VY", "VZ", "LT"]
    keys_index = []

    for key in keys:
        keys_index.append(str.index(content["result"], key, start_index_1, finish_index_1))

    for i in range(len(keys_index) - 1):
        result.append(content["result"][keys_index[i]:keys_index[i+1]])

    result_digits = {}
    for i in range(len(result)):
        _ = ""
        for j in result[i]:
            if j.isdigit() or j in ['.', 'E', '+', '-']:
                _ = _ + j
        result_digits[keys[i]] = float(_)
        if i == 0 or i == 1 or i == 2:
            result_digits[keys[i]] = result_digits[keys[i]] / AU
    return result_digits


# Get GM fun
def retrieve_GM_data(Planet_name):
    content = Call_API_data(GM_API_key_construction(Planet_name))
    start_index = str.index(content["result"], "GM")
    text = ""

    while text != "=":
        text = content["result"][start_index]
        start_index += 1

    start_index = start_index + 1
    result = ""

    while content["result"][start_index].isdigit() or content["result"][start_index] in ['.']:
        result = result + content["result"][start_index]
        start_index += 1
    return float(result)


# API itself
def Call_API_data(API_key):
    response = requests.get(f"{API_key}")
    content = response.json()
    return content


def Ephem_API_key_construction(Planet_name, date_import):

    Planet_name = Planet_name.strip().upper()

    Planets_dict = {"MERCURY": "199", "VENUS":  "299", "EARTH":  "399", "MARS":    "499",
                    "JUPITER": "599", "SATURN": "699", "URANUS": "799", "NEPTUNE": "899", "PLUTO": "999"}
    
    if date_import == "today":
        date_import = date.today()
    else:
        date_import = datetime.strptime(date_import, "%Y-%m-%d").date()

    next_date = date_import + timedelta(days=1)
    COMMAND_API = ""
    if Planet_name in Planets_dict:
        COMMAND_API = Planets_dict[Planet_name]
    else:
        COMMAND_API = f"{Planet_name}"

    API_key_ephem = "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&" \
    f"COMMAND='{COMMAND_API}'&" \
    "OBJ_DATA='YES'&" \
    "MAKE_EPHEM='YES'&" \
    "EPHEM_TYPE='VECTOR'&" \
    "CENTER='@sun'&" \
    f"START_TIME='{date_import}'&" \
    f"STOP_TIME='{next_date}'&" \
    "STEP_SIZE='1 mo'&" \
    "QUANTITIES='2'"
    return API_key_ephem

# https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='399%3B'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='VECTOR'&CENTER='500@399'&START_TIME='2020-01-01'&STOP_TIME='2020-01-02'&STEP_SIZE='1 mo'&QUANTITIES='2'
def GM_API_key_construction(Planet_name):
    Planet_name = Planet_name.strip().lower()

    Planets_dict = {"mercury": "199", "venus":  "299", "earth":  "399", "mars":    "499",
                    "jupiter": "599", "saturn": "699", "uranus": "799", "neptune": "899", "pluto": "999"}
    COMMAND_API = ""
    if Planet_name in Planets_dict:
        COMMAND_API = Planets_dict[Planet_name]
    else:
        COMMAND_API = f"{Planet_name}"

    API_key_GM = "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&" \
    f"COMMAND='{COMMAND_API}'&" \
    "OBJ_DATA='YES'&" \
    "MAKE_EPHEM='NO'&" \
    "QUANTITIES='2'"
    return API_key_GM


def main():
    print("NASA API module - main")
    # API_test_key = "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='C/2025 N1'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='VECTOR'&CENTER='@sun'&START_TIME='2025-11-01'&STOP_TIME='2025-11-02'&STEP_SIZE='1 mo'&QUANTITIES='2'"
    date_main = "2010-01-01"
    name_main = "Atlas"
    content = Call_API_data(Ephem_API_key_construction(name_main, date_main))
    print(content["result"])
    # print(get_API_data(name_main, date_main, asteroid = True))


if __name__ == "__main__":
    main()

import json
import pprint

with open("stops.json") as f:
    data = json.load(f)

stops = {}
for stop in data["stops"]:
    stop_id = stop["global_stop_id"]
    stops[stop_id] = {
        "name": stop["stop_name"],
        "lat": stop["stop_lat"],
        "lon": stop["stop_lon"],
        "raw_id": stop["raw_stop_id"]
    }

with open("stations.py", "w") as f:
    f.write("stations = ")
    f.write(pprint.pformat(stops))
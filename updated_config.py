import sys
import json

config_filename = sys.argv[1]
updates_filename = sys.argv[2]

def update(path, dict_obj, new_value):
    keys = path.split('.')
    last_key = keys.pop()
    current = dict_obj
    for key in keys:
        current = current[key]
    current[last_key] = new_value

with open(config_filename) as conf_file:
    json_conf = json.load(conf_file)

with open(updates_filename) as changes_file:
    for line in changes_file:
        left, right = line.split('": "', 1)
        path = left[1:]
        change_value = right[:-1]

        update(path, json_conf, change_value)
print(json_conf)

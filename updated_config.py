import sys
import json
import re

config_filename = sys.argv[1]
updates_filename = sys.argv[2]

def update(path, dict_obj, new_value):
    keys = path.split('.')
    last_key = keys.pop()
    current = dict_obj

    for key in keys:
        # Check if "key" has array indexing at its end
        if(key[-1] == ']'):
            # Get literal part to the left of first opening square bracket
            literal_part = key.split('[', 1)[0]
            current = current[literal_part]

            # Regular expression to find all array indices
            # That is, integers enclosed in square brackets, like [2]
            indices = re.findall(r'\[([^]]*)\]', key)

            for idx in indices:
                current = current[int(idx)]
        else:
            current = current[key]
    # Check if "last_key" has array indexing at its end
    if(last_key[-1] == ']'):
        # Get literal part to the left of first opening square bracket
        literal_part = last_key.split('[', 1)[0]
        current = current[literal_part]

        # Regular expression to find all array indices
        # That is, integers enclosed in square brackets, like [2]
        indices = re.findall(r'\[([^]]*)\]', last_key)
        last_index = indices.pop()

        for idx in indices:
            current = current[int(idx)]
        current[int(last_index)] = new_value
    else:
        current[last_key] = new_value

with open(config_filename) as conf_file:
    json_conf = json.load(conf_file)

with open(updates_filename) as changes_file:
    for line in changes_file:
        left, right = line.split('": ', 1)
        path = left[1:]
        change_value = right[:-1]

        update(path, json_conf, change_value)
print(json_conf)

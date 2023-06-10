import sys
import json
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)

config_filename = sys.argv[1]
updates_filename = sys.argv[2]

WRITE_TO_FILE = False
if len(sys.argv) > 3:
    output_filename = sys.argv[3]
    WRITE_TO_FILE = True

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
    for line_number, line in enumerate(changes_file):
        left, right = line.split('": ', 1)
        path = left[1:]
        change_value = json.loads(right[:-1])

        try:
            update(path, json_conf, change_value)
            logger.debug(f"operation {line_number} succeeded!")
        except:
            logger.warning(f"operation {line_number} failed...")

if WRITE_TO_FILE:
    with open(output_filename, 'w') as output:
        json.dump(json_conf, output)
else:
    print(json_conf)

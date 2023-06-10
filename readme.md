Configuration editor
--------------------
This is a simple configuration editor script in Python using JSON objects.
The script takes as input a config file and the changes to be applied to it.
Each line of the changes file contains a different transformation/update.
Here is a update example:

	"path.to[3].change : new_value"
This "path" is basically a list of keys and array indexes.
`new_value` can be any JSON object, as long as it fits into the same line.

Usage
-----

Simply run the script with these arguments:
 - The first argument is the original configuration file.
 - The second is the filename of the changes to be applied.
 - The third is optional. It is the output filename. If it is not provided, the output is simply printed (Standard output). This can be problematic since the logging is currently done in STDOUT.

Here's an example:

	python updated_config.py config.json changes.txt

Or:

	python updated_config.py 2config.json broken_changes.txt new_conf.json

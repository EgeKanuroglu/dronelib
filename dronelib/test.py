import json

# JSON file
f = open('params.json', "r")

# Reading from file
data = json.loads(f.read())

# Iterating through the json
# list
print(data)
print(type(data))
print(data["cam_index"])
# Closing file
f.close()

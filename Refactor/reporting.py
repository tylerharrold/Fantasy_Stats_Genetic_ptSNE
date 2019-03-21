import json
# handles all reporting functions for project
def write_json(target_directory , filename , **data):
    with open(str(target_directory / filename) , 'w') as outfile:
        json.dump(data , outfile)

import json
import random
import data
def get_data_of_random_attraction(region_id, number=3):
    upper_limit = len(data[ragion_id][category_id]) - 1
    whole_text = 0
    for i in range(number):
        whlole_text += data[region_id]["attraction"][random.randint(0, upper_limit)]
    return whole_text

description = {
        "type": "function",
        "function": {
            "name": "get_data_random_attraction",
            "description": "Use region_id, category_id, and number to retrieve the complete data of 3 random attractions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region_id": {
                        "type": "string",
                        "description": "Region name e.g. 동카름, 서카름",
                    },
                    "number": {
                        "type": "int",
                        "description": "The number of attractions to get information e.g. 2, 3",
                    },
                },
                "required": ["region_id", "category_id", "number"],
            },
        },
    }

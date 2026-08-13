import json
import os

MEMORY_FILE = "memory/user_memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def save_memory(user, key, value):
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    if user not in data:
        data[user] = {}

    data[user][key] = value

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_memory(user):
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    return data.get(user, {})
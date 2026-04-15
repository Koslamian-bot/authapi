def individual_fetch(todo) -> dict:
    return {
        "id" : str(todo["_id"]),
        "name" : todo["name"],
        "description" : todo["description"],
        "completed" : todo["completed"]
    }

def group_fetch(todos) -> list:
    return [individual_fetch(todo) for todo in todos]

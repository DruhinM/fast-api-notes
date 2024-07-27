def noteEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "desc": item["desc"],
        "priority": item["priority"]
    }


def notesEntity(entity) -> list:
    return [noteEntity(item) for item in entity]

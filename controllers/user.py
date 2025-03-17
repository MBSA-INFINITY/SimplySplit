from db import user_details_collection
from flask import abort


def insert_user(user_details):
    user_id = user_details.get("user_id")
    if _ := user_details_collection.find_one({"user_id": user_id},{"_id": 0}):
        return user_id
    else:
        try:
            user_details_collection.insert_one(user_details)
        except Exception as e:
            abort({"message": str(e)})
    return user_id

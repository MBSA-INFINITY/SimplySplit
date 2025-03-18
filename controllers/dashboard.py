from db import user_details_collection, friends_list_collection, group_details_collection, group_members_details_collection
from collections import defaultdict
from flask import abort, redirect
import uuid

def add_new_friend(user_id, friend_user_id):
    if user := user_details_collection.find_one({"user_id": friend_user_id},{"_id": 0}):
        new_friend_details = {"user_id": user_id, "friend_user_id": friend_user_id}
        __new_friend_details = {"user_id": friend_user_id, "friend_user_id": user_id}
        friends_list_collection.insert_many([new_friend_details, __new_friend_details])
        return redirect("/dashboard")
    else:
        abort(500, {"message": f"No user with userID {friend_user_id}"})

def add_new_group(user_id, list_of_friends, group_name):
    group_id = str(uuid.uuid4())
    group_state = {str(user_id): 0}
    for friend_user_id in list_of_friends:
        group_state[str(friend_user_id)] = 0
    grp_details = {"group_id": group_id, "group_name": group_name, "group_state": group_state}
    group_details_collection.insert_one(grp_details)


def get_friends_list(user_id):
    all_friends = list(friends_list_collection.find({"user_id": user_id},{"_id": 0}))
    return all_friends

def get_group_list(user_id):
    pipeline = [
        {
        "$match": {
            "user_id": user_id
        }
    },
    {
        "$group": {
            "_id": "$group_id"
        }
    },
    {
        "$lookup": {
            "from": "group_details",
            "localField": "_id",
            "foreignField": "group_id",
            "as": "group_details"
        }
    }
]
    aggregation_data = list(group_members_details_collection.aggregate(pipeline))
    all_groups = []
    if len(aggregation_data) > 0:
        for data in aggregation_data:
            group_details = data.get("group_details")[0]
            details = {"group_id": group_details["group_id"], "group_name": group_details["group_name"]}
            all_groups.append(details)
    return all_groups

def get_group_name(group_id):
    if group_details := group_details_collection.find_one({"group_id": group_id},{"_id": 0}):
        return group_details.get("group_name"), group_details.get("group_state")
    else:
        abort(500, {"message": f"group with group_id {group_id} doesn't exist!"})

def get_group_members(group_id):
    if group_details := group_details_collection.find_one({"group_id": group_id}):
        return list(group_details.get("group_state").keys())
    else:
        abort(500, {"message": "Group doesn't exists!"})
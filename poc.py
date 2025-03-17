import os
import pymongo

ENVIRONMENT = os.environ["ENVIRONMENT"]
if ENVIRONMENT == "local":
    connection_string = "mongodb://localhost:27017"
    DB_NAME = "simplysplit"
else:    
    MONGO_CLUSTER = os.environ["MONGO_URI"]
    MONGO_USERNAME = os.environ["MONGO_USERNAME"]
    MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
    DB_NAME = os.environ["DB_NAME"]
    connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&ssl=true&ssl_cert_reqs=CERT_NONE&w=majority"


db_client = pymongo.MongoClient(connection_string)
db_client = db_client.get_database(DB_NAME)

user_details_collection = db_client['user_details']
friends_list_collection = db_client['friends_list']
group_details_collection = db_client['group_details']
group_members_details_collection = db_client['group_members_details']

data = group_details_collection.find_one({"group_id": "56023a6a-0ea9-48b1-a7d6-ccbf02366b30"},{"_id": 0})
print(data.get("group_state"))
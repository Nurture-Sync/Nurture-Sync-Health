from pymongo import MongoClient

# Set up MongoDB client
MONGO_URI = "mongodb+srv://community:NS123456@cluster0.smgpcp9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["community_db"]

# Retrieve all posts
def get_posts():
    return list(db.posts.find())

# Add a new post
def add_post(user_id, title, content):
    post = {"user_id": user_id, "title": title, "content": content}
    db.posts.insert_one(post)

# Retrieve all events
def get_events():
    return list(db.events.find())

# Add a new event
def add_event(title, date, description):
    event = {"title": title, "date": date, "description": description}
    db.events.insert_one(event)

# Retrieve all doctor queries for a specific forum type
def get_doctor_queries(forum_type="General"):
    return list(db.queries.find({"forum_type": forum_type}))

# Add a new doctor query, specifying the forum type
def add_doctor_query(user_id, question, forum_type="General"):
    query = {
        "user_id": user_id,
        "question": question,
        "forum_type": forum_type,
        "responses": []
    }
    db.queries.insert_one(query)

# Add a response from a doctor to a specific query
def add_doctor_response(query_id, doctor_id, response):
    db.queries.update_one(
        {"_id": query_id},
        {"$push": {"responses": {"doctor_id": doctor_id, "response": response}}}
    )

# Add a community response to a specific query
def add_community_response(query_id, responder_id, response):
    db.queries.update_one(
        {"_id": query_id},
        {"$push": {"responses": {"responder_id": responder_id, "response": response}}}
    )

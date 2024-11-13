from pymongo import MongoClient
from bson import ObjectId

# Set up MongoDB client
MONGO_URI = "mongodb+srv://community:NS123456@cluster0.smgpcp9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["community_db"]
collection = db["posts"]

def create_dummy_posts():
    sample_posts = [
        {"user_id": "user1", "title": "My Weight Loss Journey", "content": "Lost 20lbs over 6 months with balanced diet and exercise!", "image_url": "https://imgs.search.brave.com/htM3106bAAix3FOChUWjdZe4HfbMVBk1s2tJUAjMBI8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzLzI5LzUz/L2U5LzI5NTNlOTY4/ZDZlZDc4ZGE2NGNl/ZTQ3ODg3M2UzODQy/LmpwZw"},
        {"user_id": "doctor1", "title": "Thyroid Management Tips", "content": "Tips on managing thyroid with regular checkups and diet.", "image_url": "https://imgs.search.brave.com/7t0aaHy1ZzmtA9iRtptnkpz8xivr29RZj9LUW2AOUMQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/YWR2YW5jZWVyLmNv/bS9pbWFnZXMvYmxv/Zy9ibG9nLWZiNS5q/cGc"},
        {"user_id": "patient2", "title": "Managing Diabetes with a Diet Plan", "content": "I've controlled my sugar levels with this diet plan.", "image_url": "https://imgs.search.brave.com/CuBkQcSCR923T6vkAsGOAjYmdz9wPq7IT0ePyRsE4hU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzAyLzg1LzkxLzQ1/LzM2MF9GXzI4NTkx/NDU4NV80MlQ5QWYy/cWlhdEFPeWFKaUV0/Wmh3WVhxczRoTVVr/SC5qcGc"},
        {"user_id": "patient3", "title": "Yoga Mudras for Thyroid", "content": "Learn these yoga mudras to aid thyroid health.", "image_url": "https://imgs.search.brave.com/XgLZZ9bLEO5YefxLEheiAxtR2SoEn4ml1oFYGaS0Q_g/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/Zml0c3JpLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAyNC8w/Ni9Zb2dhLU11ZHJh/cy1mb3ItVGh5cm9p/ZC1Qcm9ibGVtcy0x/MDI0eDY4My5qcGc"},
        {"user_id": "doctor2", "title": "Diabetes-Friendly Recipes", "content": "Try these easy, healthy recipes to keep blood sugar in check.", "image_url": "https://imgs.search.brave.com/qn_1lsJQoCWHkk2v_QjZTjAAgc6m9hWwI3a_MPe8LOE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/ZWF0aW5nd2VsbC5j/b20vdGhtYi81TmJa/SnRTUF93Zm9KTXc3/QVBTOW1JTTBhcVk9/LzE1MDB4MC9maWx0/ZXJzOm5vX3Vwc2Nh/bGUoKTptYXhfYnl0/ZXMoMTUwMDAwKTpz/dHJpcF9pY2MoKS9j/aGlja2VuLWFuZC1z/cGluYWNoLXNraWxs/ZXQtY2Fzc2Vyb2xl/LWZvci10d28tNmJl/ZTUwYzg4YzRmNDU0/NDg1ODNjYjhmMmVm/ZDQ1MTEuanBn"},
        {"user_id": "patient4", "title": "Weight Loss Tips", "content": "Simple tips to boost weight loss journey.", "image_url": "https://imgs.search.brave.com/cPwxZDG_n-Ioi1EFQ0jhdfD7iVg60oshhjyqp0hqYws/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvNjU2/OTQ4NDIwL3Bob3Rv/L292ZXJ3ZWlnaHQu/anBnP3M9NjEyeDYx/MiZ3PTAmaz0yMCZj/PWZ6djU0VGhxWUtJ/Y2UzemVja0xJVHdv/QzZxWHB5cDlkQXZt/dzU0S2R0Vmc9"},
        {"user_id": "doctor3", "title": "Benefits of Yoga for Thyroid Health", "content": "Yoga can balance hormones and support thyroid function.", "image_url": "https://imgs.search.brave.com/2Vc3CWfmhR1IoTZfrNViNJCzD6DHwEEYTH3RfhJ6fn4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTM5/NTUwNDI1NS9waG90/by9hZnJpY2FuLW1h/bi1wcmFjdGljZS15/b2dhLWluLXRoZS1i/dXR0ZXJmbHktcG9z/aXRpb24taW4teW9n/YS1jbGFzcy5qcGc_/cz02MTJ4NjEyJnc9/MCZrPTIwJmM9Nmlk/anlydWJIWHItOGZ3/Y3RPNVQ1YW5ETnRx/RUZuYTJveGpUa09Z/VVNZWT0"},
        {"user_id": "patient5", "title": "Controlling Diabetes Naturally", "content": "Exercise and fiber-rich diet helped me.", "image_url": "https://imgs.search.brave.com/eGFfEGP7BaUif9ken1RGgcN2j2NSK676MQ7ijV4GJiY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWcu/bGIud2JtZHN0YXRp/Yy5jb20vdmltL2xp/dmUvd2VibWQvY29u/c3VtZXJfYXNzZXRz/L3NpdGVfaW1hZ2Vz/L3JlY29tbWVuZGVk/L3JlY29tbWVuZGVk/LWRpYWJldGVzLTIu/anBnP3Jlc2l6ZT01/MDBweDoqJm91dHB1/dC1xdWFsaXR5PTc1"},
        {"user_id": "doctor4", "title": "Effective Diet Plan for Thyroid", "content": "Avoid processed foods, add leafy greens and proteins.", "image_url": "https://imgs.search.brave.com/pZuWQlrR220X6doIeS_1QDl3iJWzeBhUR-liy7hm82w/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMuZXZlcnlkYXlo/ZWFsdGguY29tL2lt/YWdlcy9kaWFiZXRl/cy90eXBlLTItZGlh/YmV0ZXMvdGlwcy10/by1sb3dlci1ibG9v/ZC1zdWdhci1uYXR1/cmFsbHktMDktMTQ0/MHg4MTAuanBnP3Nm/dnJzbj1jMDNmZDA3/YV81"},
        
    ]
    # Insert posts and handle potential errors
    try:
        collection.insert_many(sample_posts)
        print("Dummy posts added to the database.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Verify insertion
    inserted_posts = collection.find()
    for post in inserted_posts:
        print(post)

# Run the function to add posts to the database
create_dummy_posts()
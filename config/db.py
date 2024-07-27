from pymongo import MongoClient

MONGO_URI = "mongodb+srv://user:3womVd6pvH6Lt46Z@notes.8kdkaxg.mongodb.net"
client = MongoClient(MONGO_URI)
conn = client.notes  # Assuming 'notes' is the database name
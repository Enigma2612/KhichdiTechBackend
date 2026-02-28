from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'srm_db')

class MongoDBConnection:
    def __init__(self, uri=MONGODB_URI, timeout=5000):
        """
        Initialize MongoDB connection
        
        Args:
            uri (str): MongoDB connection string
            timeout (int): Connection timeout in milliseconds
        """
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=timeout)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            print("✓ Connected to MongoDB successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        if not self.db:
            raise Exception("Not connected to MongoDB")
        return self.db[collection_name]
    
    def insert_one(self, collection_name, document):
        """Insert a single document"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id
    
    def insert_many(self, collection_name, documents):
        """Insert multiple documents"""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids
    
    def find_one(self, collection_name, query):
        """Find a single document"""
        collection = self.get_collection(collection_name)
        return collection.find_one(query)
    
    def find_many(self, collection_name, query=None, limit=0):
        """Find multiple documents"""
        collection = self.get_collection(collection_name)
        query = query or {}
        return list(collection.find(query).limit(limit))
    
    def update_one(self, collection_name, query, update_data):
        """Update a single document"""
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count
    
    def delete_one(self, collection_name, query):
        """Delete a single document"""
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result.deleted_count
    
    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")

# Global connection instance
db_connection = None

def get_db():
    """Get the global database connection"""
    global db_connection
    if db_connection is None:
        db_connection = MongoDBConnection()
    return db_connection

if __name__ == "__main__":
    # Example usage
    db = get_db()
    
    # # Insert a document
    # doc_id = db.insert_one('users', {'name': 'John Doe', 'email': 'john@example.com'})
    # print(f"Inserted document ID: {doc_id}")
    
    # # Find a document
    # user = db.find_one('users', {'name': 'John Doe'})
    # print(f"Found user: {user}")
    
    db.close()
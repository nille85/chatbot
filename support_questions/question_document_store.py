from pymongo import MongoClient
import datetime


class QuestionDocumentStore:
    def __init__(self, host, port, username, password, database_name, collection_name):
        self.connection_string = f"mongodb://{username}:{password}@{host}:{port}"
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    def disconnect(self):
        if self.client:
            self.client.close()

    def find_question(self, question):
        if self.collection is None:
            raise Exception("Database connection not initialized. Call connect() method first.")
        search_query = {"$text": {"$search": question}}
        results = self.collection.find(search_query)
        return list(results)

    def remove_all_questions(self):
        if self.collection is None:
            raise Exception("Database connection not initialized. Call connect() method first.")
        result = self.collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from the collection.")

    def insert_one_question(self, question, answer):
        if self.collection is None:
            raise Exception("Database connection not initialized. Call connect() method first.")

        data_to_insert = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.datetime.utcnow()
        }

        result = self.collection.insert_one(data_to_insert)

        if result.inserted_id:
            return result.inserted_id
        else:
            return None

    def insert_many_questions(self, entries):
        if self.collection is None:
            raise Exception("Database connection not initialized. Call connect() method first.")

        data_to_insert = []
        for entry in entries:
            entry["timestamp"] = datetime.datetime.utcnow()
            data_to_insert.append(entry)

        result = self.collection.insert_many(data_to_insert)

        if result.inserted_ids:
            return result.inserted_ids
        else:
            return []




from support_questions.question_document_store import QuestionDocumentStore
from support_questions.questions_vector_store import QuestionVectorStore, QuestionVectorStoreFactory
from langchain.chat_models import ChatOllama


class ConfigLoader:
    @staticmethod
    def load_from_file(tomlkit, config_file_path: str):
        with open(config_file_path, "r") as file:
                return tomlkit.load(file)

class Config:

    def __init__(self, config_data):
        self.config_data = config_data

    def create_question_document_store(self):
        mongo_config = self.config_data["mongodb"]
        return QuestionDocumentStore(
            mongo_config["host"],
            mongo_config["port"],
            mongo_config["username"],
            mongo_config["password"],
            mongo_config["database_name"] ,
            mongo_config["collection_name"]
            )

    def create_vector_store(self):
        qdrant_config = self.config_data["qdrant"]
        return QuestionVectorStoreFactory.create(qdrant_config["sentence_transformer_model"], qdrant_config["url"])

    def create_chat_ollama(self):
        ollama_config = self.config_data["ollama"]
        return ChatOllama(model="mistral", base_url = ollama_config["url"])



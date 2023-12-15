import json
from support_questions.question_document_store import QuestionDocumentStore
from support_questions.questions_vector_store import QuestionVectorStore


class QuestionStoreStartupManager:

    def __init__(self, question_store: QuestionDocumentStore, vector_store: QuestionVectorStore):
        self.question_store = question_store
        self.vector_store = vector_store

    def run(self, file_path: str):
        self.question_store.connect()
        self.question_store.remove_all_questions()
        support_question_documents = self._read_support_questions(file_path)
        self.question_store.insert_many_questions(support_question_documents)
        self.question_store.disconnect()

        support_questions = [support_question_document["question"] for support_question_document in support_question_documents]
        self.vector_store.store_question_vectors(support_questions)
        

   
    def _read_support_questions(self, file_path:str):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
        


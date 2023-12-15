from sentence_transformers import SentenceTransformer
from typing import List
from qdrant_client import models, QdrantClient
from qdrant_client.models import VectorParams, Distance




class QuestionVectorStore:

    def __init__(self, sentence_transformer: SentenceTransformer, qdrant_client: QdrantClient):
        self.sentence_transformer = sentence_transformer
        self.qdrant_client = qdrant_client
        self.collection_name = "support_questions"

    def store_question_vectors(self, questions : List [str]):
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.sentence_transformer.get_sentence_embedding_dimension(), distance=Distance.COSINE),
        )

        questions_payload = map(lambda question: {"question" : question}, questions)
        embeddings = self.sentence_transformer.encode(questions)
        self.qdrant_client.upload_collection(
            collection_name=self.collection_name,
            vectors=embeddings,
            payload= questions_payload,
            ids=None,  # Vector ids will be assigned automatically
            batch_size=10
        )

    def find_questions(self, question: str):
        question_vector = self.sentence_transformer.encode(question).tolist()
        search_result =self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=question_vector,
            score_threshold=0.5,
            query_filter=None,  # If you don't want any filters for now
            limit=3  # 5 the most closest results is enough
        )

        print(search_result)
    
        questions = [hit.payload["question"] for hit in search_result]
        return questions


class QuestionVectorStoreFactory:
    @staticmethod
    def create(model: str, url: str) -> QuestionVectorStore:
        model = SentenceTransformer(model) #768 dimensions
        #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') #384 dimensions
        qdrant_client = QdrantClient(url)
        return QuestionVectorStore(model, qdrant_client)






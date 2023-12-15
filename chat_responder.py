import random
from abc import ABC, abstractmethod

from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema.messages import AIMessage
from langchain.chat_models.base import BaseChatModel

from support_questions.question_document_store import QuestionDocumentStore
from support_questions.questions_vector_store import QuestionVectorStore

class ChatResponder(ABC):
    @abstractmethod
    def respond(self, message, chat_history):
       pass



class MistralChatResponder(ChatResponder):

    def __init__(self, model : BaseChatModel, prompt: ChatPromptTemplate):
        self.model = model
        self.prompt = prompt

    def respond(self, message, chat_history):
        runnable =   self.prompt | self.model | StrOutputParser()
        bot_message = ""
        for chunk in runnable.stream({"message": message}):
            bot_message += chunk
        chat_history.append((message, bot_message))
        self.prompt.messages.append(AIMessage(content=message))
        print("returning from respond")
        return "", chat_history

class MongoDBChatResponder(ChatResponder):
    def __init__(self, question_store : QuestionDocumentStore):
        self.question_store = question_store
        self.question_store.connect()

    def __del__(self):
        self.question_store.disconnect()

    def respond(self, message, chat_history):
        found_questions = self.question_store.find_question(message)
        bot_message = found_questions[0]["answer"] if found_questions else "I have no answer, ask another question"
        chat_history.append((message, bot_message))
        return "", chat_history


class MongoAndVectorChatResponder(ChatResponder):
    def __init__(self, question_store : QuestionDocumentStore, vector_store: QuestionVectorStore):
        self.question_store = question_store
        self.vector_store = vector_store
        self.question_store.connect()

    def __del__(self):
        self.question_store.disconnect()

    def respond(self, message, chat_history):
        questions = self.vector_store.find_questions(message)
        bot_answers = []
        for question in questions:
            found_questions = self.question_store.find_question(question)
            if found_questions:
                    bot_answers.append(found_questions[0]["answer"] )

        bot_message = "\n".join(bot_answers) if bot_answers else "I have no answer, ask another question please"
        chat_history.append((message, bot_message))
        return "", chat_history



class ChatResponderFactory:


    @staticmethod
    def createMistral(chat_ollama: ChatOllama) -> ChatResponder:
        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very talented customer support agent who provides accurate and eloquent answers to customer problems and issues",
            ),
            ("human", "{message}"),
        ]
        )
        return MistralChatResponder(chat_ollama, prompt)

    @staticmethod
    def createMongo(question_store: QuestionDocumentStore) -> ChatResponder:
        return MongoDBChatResponder(question_store)

    @staticmethod
    def createMongoAndVector(question_store: QuestionDocumentStore, vector_store: QuestionVectorStore) -> ChatResponder:
        return MongoAndVectorChatResponder(question_store, vector_store)


    
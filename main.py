import gradio as gr
from chat_responder import ChatResponderFactory, ChatResponder
import time
import tomlkit
from config.config import Config, ConfigLoader


from support_questions.startup_data_manager import QuestionStoreStartupManager


config = Config(ConfigLoader.load_from_file(tomlkit, "dev_config.toml"))

question_store = config.create_question_document_store()
vector_store = config.create_vector_store()
chat_ollama = config.create_chat_ollama()

startup_manager = QuestionStoreStartupManager(question_store, vector_store)
startup_manager.run("data/support_questions.json")



mistral_responder = ChatResponderFactory.createMistral(chat_ollama)
mongo_responder = ChatResponderFactory.createMongo(question_store)
mongo_and_vector_responder = ChatResponderFactory.createMongoAndVector(question_store, vector_store)


def create_chatbot(name: str, responder: ChatResponder):
    gr.Markdown(f"## {name} Assistant")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Message")
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(responder.respond, [msg, chatbot], [msg, chatbot])


with gr.Blocks() as demo:
    
    gr.Markdown("# AI Assistant")
    with gr.Tab("Mistral"):
        gr.Markdown("Only using data trained by Mistral model, based on the question that is asked")
        create_chatbot("Mistral", mistral_responder)
    with gr.Tab("Mongo"):
        gr.Markdown("Matching question asked with questions stored in the document database. Uses text-search to match the questions")
        create_chatbot("Mongo", mongo_responder)
    with gr.Tab("Mongo And Vector"):
        gr.Markdown("Uses sentence-transformer model to match the questions with a high similarity score in the document database. Returns the answers that contain a high similarity score.")
        create_chatbot("Mongo And Vector", mongo_and_vector_responder)
   

if __name__ == "__main__":
    demo.launch()
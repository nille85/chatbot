import unittest
from unittest.mock import Mock, patch
from config.config import Config  # Replace 'your_module' with the actual module name

class TestConfig(unittest.TestCase):
    def test_create_question_document_store(self):
        
        mock_config = {
            "mongodb": {
                "host": "fake",
                "port": "20",
                "username": "user",
                "password" : "pass",
                "database_name" : "customerSupport",
                "collection_name" : "questions"            }
        }

        # Create an instance of the Config class
        config = Config(mock_config)

        question_document_store = config.create_question_document_store()
        self.assertIsNotNone(question_document_store)
    

    # Similar tests can be written for create_vector_store and create_chat_ollama methods

if __name__ == '__main__':
    print("unit test")
    unittest.main()
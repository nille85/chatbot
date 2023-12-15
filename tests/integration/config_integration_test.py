import unittest
import tomlkit
from config.config import ConfigLoader

class IntegrationTestConfigLoader(unittest.TestCase):
    def test_load_from_file(self):
        # Define the path to your real configuration file
        real_config_file_path = "tests/fake.toml"

        # Use the actual ConfigLoader class to load the configuration
        loaded_config = ConfigLoader.load_from_file(tomlkit, real_config_file_path)

        # Perform assertions based on the structure and content of your real configuration
        self.assertIsNotNone(loaded_config)
        self.assertIsInstance(loaded_config, dict)
        self.assertIn("mongodb", loaded_config)
        self.assertIn("qdrant", loaded_config)
        self.assertIn("ollama", loaded_config)
        self.assertEqual(loaded_config["mongodb"]["host"], "fake")
      

if __name__ == '__main__':
    print("integration test")
    unittest.main()
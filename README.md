# Chatbot

This application is a demonstrator to showcase the different ways to implement a chatbot and their consequences:
* Only using data trained by the Mistral LLM. (Could also be GPT or another LLM)
* Only using MongoDB document store and using search to query matching questions
* Semantic-search using both MongoDB document store and Qdrant vector database


## Run Application

### Install Requirements
```
pip install requirements.txt
```


### Local Databases

MongoDB and Qdrant can be started and stopped using docker-compose command

spin up mongodb and qdrant:
```
docker-compose -f docker.compose.yml up
```

```
docker-compose -f docker.compose.yml down
```


#### Qdrant Vector Database
Access The Dashboard: `http://0.0.0.0:6333/dashboard`


#### MongoDB
Install the mongodb shell on Mac
```
brew install mongosh
```

*Creating an index to do partial search:*

Replace collection_name with your collection, now it is able to perform a text search on the question attribute.
```
db.your_collection_name.createIndex({ question: "text" })
```


### Mistral LLM
[Ollama](https://ollama.ai/)  is used to download and expose the the Mistral LLM model.

For the installation of Ollama and how to run models locally using Ollama can be found [here](https://github.com/jmorganca/ollama)

### Run The Application
```
python main.py
```



## Running Tests

Unit tests:
```
python -m unittest discover tests/unit -p "*test.py"
```

Integration tests:
```
python -m unittest discover tests/integration -p "*test.py"
```



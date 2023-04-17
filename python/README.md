To use this demo, you'll need an api.data.gov key, and it will need to be granted permissions for interacting with the pilot FAC data.

# Getting started

You should be able to clone this repository to your local machine.

```
git clone https://github.com/GSA-TTS/fac-dissemination-api-exploration
```

# Preparing the environment

You'll need to export two values, per the top-level README.

## Preparing the Python environment

You will need to create a virtual environment and install `pytest` and `requests`. 

```
python3 -m venv venv
source venv/bin/activate
pip install pytest requests
```

You may have other tools you like to use for managing Python environments. We're not opinionated in this regard.

# Running the code

You should first be able to run the unit tests.

```
pytest test_api.py
```

Then, you should be able to run the example queries:

```
python queries.py
```

# Going further

The API is provided by a tool called PostgREST. 

https://postgrest.org/

Per the top-level URL, you can compose new queries directly as URLs, or you can use the query-building/rendering code we created in `support.py`. 
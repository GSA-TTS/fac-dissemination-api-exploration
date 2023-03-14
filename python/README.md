To use this demo, you'll need an api.data.gov key, and it will need to be granted permissions for interacting with the pilot FAC data.

We are only working with a handful of Federal partners in exploring this API. We cannot accommodate any members of the public at this time.

# Getting started

We assume a Linux-like working environment. If you are on Windows, hopefully you can adapt these instructions to your environment.

First, you'll need to get an API key from api.data.gov. Sign up there. You will want to enter your Federal email address. You will receieve an automated reply with an API key.

Second, you'll need to write fac@gsa.gov *from the email address you just used* and ask us to authorize your API key. 

We'll reply when that is done. It's an entirely manual process, and it will likely take place in the AM of the day after you sent your email.

# Pull this repository

You should be able to clone this repository to your local machine.

```
git clone https://...
```

# Preparing the environment

You'll need to export two values.

One is the API URL, the other your API key.

export FAC_API_BASE="https://api.data.gov/TEST/audit-clearinghouse/v0/dissemination"
export API_GOV_KEY="... your API key goes here ..."

Those should be exported as environment variables in the shell you're using for this work.

## Preparing the Python environment

You will need to create a virtual environment and install pytest. 

```
python -m venv venv
source venv/bin/activate
pip install pytest requests
```

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

Query URLs need to be composed according to their documentation.


# 11x Gateway

## Service Description and Philosophy
This is a thin Flask application to generate FASTQ data and files, parse and analyze those files, and serve up the applicated aggregated data via a HTTP.

## Usage Instructions
Clone the repo, `cd` into it then...

`pip install -r requirements.txt` OR

`pip3 install -r requirements.txt` depending on your system

To generate mock FASTQ data and files:

`python generate_data.py`

To start the dev server on port 8000:

`python app.py`

To test:
`pytest`

## Proposed Next Steps
- Finish Dockerizing and composing
- Add Github Actions for linting, testing, building, deployment
- Identify further abstraction candidates
- Additional error handling
- Concurrentify and parallelize computationally heavy operations and move from Gateway to Mendel
- Algorithmic improvements and benchmarking
- Memory store (SQLite in this case, though I typically default to Postgres if I do not have additional specifications to go from) to eliminate processing the same underlying data upon every request
- Add ins, del, dup to `mutateSequence` function
- Parameterize some constants
- Change Gateway-Mendel communication protocol to gRPC
- Change file reads/writes to streams


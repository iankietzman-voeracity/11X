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
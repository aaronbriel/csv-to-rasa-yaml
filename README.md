# CSV to Rasa YAML Converter

Converts CSV containing responses and corresponding intents into Rasa compatible YAML file for NLU training. Also offers option to convert a Rasa YAML file into a CSV.

## Installation
Activate your virtual environment and run:
```
pip install -r requirements.txt
```

## Usage

Example (CSV to YAML):

```
python csv_to_rasa_yaml.py --csv-path 'path/to/yourfile.csv' --export-dir your_export_directory
```

Example (YAML to CSV):

```
python csv_to_rasa_yaml.py --file-path 'path/to/yourfile.yml' --export-dir your_export_directory --output-file-name output.csv --to-csv True
```

To see all available options run:

```
python csv_to_rasa_yaml.py --help
```
# CSV to Rasa YAML Converter

Converts CSV containing responses and corresponding intents into Rasa compatible YAML file for NLU training.

## Installation
Activate your virtual environment and run:
```
pip install -r requirements.txt
```

## Usage

Example:

```
python csv_to_rasa_yaml.py --csv-path 'path/to/yourfile.csv' --export-dir your_export_directory
```

To see all available options run:

```
python csv_to_rasa_yaml.py --help
```
# CSV to Rasa YAML Converter

Converts csv containing responses and corresponding intents into Rasa compatible yaml file for nlu training.

## Installation
Activate your virtual environment and run:
```
pip install requirements
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
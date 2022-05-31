# coding=utf-8
# Copyright 2022 Aaron Briel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import pandas as pd

@click.command()
@click.option('--csv-path', required=True, help='Full path to csv file.')
@click.option('--intent-column', default='intent', 
              help='Column header for intents (defaults to "intent").')
@click.option('--text-column', default='text', 
              help='Column header for texts (defaults to "text").')
@click.option('--rasa-version', default='3.0', 
              help='Rasa version (defaults to "3.0").')
@click.option('--export-dir', default='.', 
              help='Directory to export the yaml file to (defaults to current working directory).')
@click.option('--yaml-file-name', default='output.yml', 
              help='What to name exported yaml file (defaults to "output.yml").')
def convert(csv_path: str, 
            intent_column: str, 
            text_column: str, 
            rasa_version: str, 
            export_dir: str,
            yaml_file_name: str):
    """ Converts a CSV containing texts and corresponding intents into a Rasa compatible yaml file 
        and exports it to specified directory.

    Args:
        csv_path (str): Full path to csv file for conversion
        intent_column (str): Header name of intent column
        text_column (str): Header name of text column
        rasa_version (str): Rasa version
        export_dir (str): Directory to export the yaml file to
        yaml_file (str): What to name exported yaml file
    """    
    yaml_path = f'{export_dir}/{yaml_file_name}'
    yaml_file = open(yaml_path, "w")
    df = pd.read_csv(csv_path) 
            
    yaml_file.write(f"version: \"{rasa_version}\"\n") 
    yaml_file.write(f"nlu:\n")    
    
    intents = df[intent_column].unique().tolist()
    for intent in intents:
        yaml_file.write(f"  - intent: {intent}\n")
        yaml_file.write("    examples: >-\n")
        intent_texts = df[df[intent_column] == intent][text_column].tolist()
        for text in intent_texts:
            yaml_file.write(f"     - {text}\n")

    yaml_file.close()

if __name__ == '__main__':
    convert()

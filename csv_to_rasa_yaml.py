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

import csv
import os

import click
import pandas as pd
import yaml


class Converter(object):
    """ Converts a CSV containing texts and corresponding intents into a Rasa 
        compatible yaml 'intents' nlu file and exports it to specified directory.
        
        One also has the option to convert a Rasa 'intents' yaml file into a
        csv with 'text' and 'intent' columns for data analysis purposes.

    Args:
        file_path (str): Full path to csv or yaml file to be converted
        intent_column (str): Header name of intent column
        text_column (str): Header name of text column
        examples_column (str): YAML key for text examples
        rasa_version (str): Rasa version
        export_dir (str): Directory to export the yaml or csv file to
        output_file (str): What to name exported yaml or csv file
        to_csv (bool): Whether to convert yaml to csv
    """ 
    def __init__(
        self,
        file_path: str,
        intent_column: str = 'intent', 
        text_column: str = 'text', 
        examples_column: str = 'examples',
        rasa_version: str = '3.0', 
        export_dir: str = '.',
        output_file_name: str = 'output.yml'
    ):
        self.file_path = file_path
        self.intent_column = intent_column
        self.text_column = text_column
        self.examples_column = examples_column
        self.rasa_version = rasa_version
        self.export_dir = export_dir
        self.output_file_name = output_file_name

    def convert_csv_to_yaml(self, rasa_version:str = "3.0"):
        """ Converts CSV to Rasa compatible YAML
        
        Args:
            rasa_version (str): Rasa version
        """
        yaml_path = os.path.join(self.export_dir, self.output_file_name)
        df = pd.read_csv(self.file_path) 
        nlu = []

        intents = df[self.intent_column].unique().tolist()
        for intent in intents:
            sample = {}
            sample['intent'] = intent
            intent_texts = df[
                df[self.intent_column] == intent][self.text_column].tolist()

            sample['examples'] = intent_texts
            nlu.append(sample)

        yaml_dict = {
            'version': rasa_version,
            'nlu': nlu
        }   
        
        with open(yaml_path, 'w') as f:
            data = yaml.dump(yaml_dict, f, sort_keys=False) 
        
    def convert_yaml_to_csv(self):
        """ Converts Rasa intent YAML to CSV
        """
        with open(self.file_path) as file:
            documents = yaml.full_load(file)['nlu']

        csv_file_path = os.path.join(self.export_dir, self.output_file_name)
        with open(csv_file_path, 'w') as csv_file:
            wr = csv.writer(csv_file, lineterminator='\n')
            # Creating header for csv
            wr.writerow([self.text_column, self.intent_column])

            for item in documents:
                examples = item[self.examples_column].split('- ')
                # Removing empty values
                examples = list(filter(None, examples))
                for example in examples:
                    wr.writerow([example.strip(), item[self.intent_column]])
                    

@click.command()
@click.option('--file-path', required=True, 
              help='Full path to csv or yaml file to be converted.')
@click.option('--intent-column', default='intent', 
              help='Column header for intents (defaults to "intent").')
@click.option('--text-column', default='text', 
              help='Column header for texts (defaults to "text").')
@click.option('--examples-column', default='examples', 
              help='YAML key for text examples (defaults to "examples").')
@click.option('--rasa-version', default='3.0', 
              help='Rasa version (defaults to "3.0").')
@click.option('--export-dir', default='.', 
              help='Directory to export the yaml or csv file to \
                    (defaults to current working directory).')
@click.option('--output-file-name', default='output.yml', 
              help='What to name exported yaml or csv file \
                    (defaults to "output.yml").')
@click.option('--to-csv', default=False, 
              help='Whether to convert a yaml to a csv (defaults to False).')
def convert(file_path: str, 
            intent_column: str, 
            text_column: str, 
            examples_column: str,
            rasa_version: str, 
            export_dir: str,
            output_file_name: str,
            to_csv: bool):
    """ Instantiates a Converter object and calls the appropriate method 
        to either convert a csv to a yaml file or a yaml to a csv.

    Args:
        file_path (str): Full path to csv or yaml file to be converted
        intent_column (str): Header name of intent column
        text_column (str): Header name of text column
        examples_column (str): YAML key for text examples
        rasa_version (str): Rasa version
        export_dir (str): Directory to export the yaml or csv file to
        output_file (str): What to name exported yaml or csv file
    """ 
    converter = Converter(
        file_path,
        intent_column, 
        text_column, 
        examples_column,
        rasa_version, 
        export_dir,
        output_file_name
    )   
    
    converter.convert_yaml_to_csv() if to_csv \
        else converter.convert_csv_to_yaml()

if __name__ == '__main__':
    convert()

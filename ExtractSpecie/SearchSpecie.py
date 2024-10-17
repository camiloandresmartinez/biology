# Copyright (c) 2024 caanmasu
#
# Licensed under the MIT License. See the LICENSE file for more information.

import os
import json

class SearchSpecie():

    def __init__(self) -> None:
        self.data_folder = 'output'
        self.json_files = []

        self.name_id = 'taxonid'

        self.input_file_scientificnames = 'input_scientific_names.txt'
        self.sci_names_list = []

        self.output_file = 'output.txt'
        self.output_data = []

        self.data = {}

        self.user_output = {}

        self.load_input_sci_names()
        self.load_files_JSON()
        self.import_files_JSON()
        self.main()

    def load_files_JSON(self):
        for _, _, filenames in os.walk(self.data_folder):
            for file in filenames:
                if file.endswith('.json'):
                    self.json_files.append(os.path.join(self.data_folder, file))

    def import_files_JSON(self):
        for file in self.json_files:
            with open(file, 'r') as f:
                self.data[file] = json.load(f)

    def load_input_sci_names(self):
        if not os.path.exists(self.input_file_scientificnames):
            with open(self.input_file_scientificnames, 'w'):
                pass
            return

        with open(self.input_file_scientificnames, 'r') as f:
            content = f.read()
        self.sci_names_list = [name for name in content.split('\n') if name.strip()]

    def clean_output_file(self):
        with open(self.output_file, 'w'):
            pass

    def get_headers(self, data_dict):
        headers = []
        for column, _ in data_dict.items():
            headers.append(column)
        return headers

    def generate_output_file(self):
        with open(self.output_file, 'w') as f:
            f.writelines(self.output_data)

    def main(self):
        data_ids_path = os.path.join(self.data_folder, 'data_ids.json')
        data_specie_id_path = os.path.join(self.data_folder, 'data_specie_id.json')
        lower_case_dict = {key.lower(): value for key, value in self.data[data_specie_id_path].items()}

        self.clean_output_file()

        specie_id = 0
        for name in self.sci_names_list:
            name = name.lower().strip()
            if name in lower_case_dict:
                specie_id = lower_case_dict[name]
            else:
                print(f"No se encontró el taxonid asociado a este nombre científico: {name}")
                continue
            
            if specie_id in self.data[data_ids_path][self.name_id]:
                data = self.data[data_ids_path][self.name_id][specie_id].copy()
                if not self.output_data:
                    headers = self.get_headers(data)
                    self.output_data.append('\t'.join(headers)+'\n')
                self.output_data.append('\t'.join(map(str, data.values()))+'\n')
            else:
                print(f"No se encontró información con este nombre científico: {name}")
                continue

        self.generate_output_file()


SearchSpecie()
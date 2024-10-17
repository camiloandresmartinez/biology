# Copyright (c) 2024 caanmasu
#
# Licensed under the MIT License. See the LICENSE file for more information.

import os
import shutil
import logging
import json
from collections import defaultdict

class ProcessData():
    
    def __init__(self) -> None:
        
        self.input_folder = 'input'
        self.output_folder = 'output'
        self.handle_ext = {'txt': self.handle_txt, 'xlsx': self.handle_xlsx, 'csv': self.handle_csv}
        self.csv_delimiter = '|'

        self.data = {}

        self.data_ids_column_main = {}
        self.data_ids = {}

        self.data_specie_id_headers = []
        self.data_specie_id = {}

        self.log_filename = 'logs.log'

        self.setup_logging()
        self.clear_data()
        self.load_data()
        self.merged_data()
        self.export_data_JSON()

    def setup_logging(self):
        logging.basicConfig(filename=self.log_filename, level=logging.INFO)

    def clear_data(self):
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder)

    def load_data(self):
        for foldername, _, filenames in os.walk(self.input_folder):
            for file in filenames:
                ext = file.split('.')[-1]
                if ext in self.handle_ext:
                    self.handle_ext[ext](os.path.join(foldername, file))

    def merged_data(self):
        self.data_ids = defaultdict(dict)
        for file, column_id in self.data_ids_column_main.items():
            for data_row in self.data[file].values():
                id = data_row[column_id].strip('"')
                self.data_ids[column_id].setdefault(id, {}).update(data_row)

    def export_data_JSON(self):
        with open(os.path.join(self.output_folder, 'data_ids.json'), 'w') as f, open(os.path.join(self.output_folder, 'data_specie_id.json'), 'w') as f2:
            json.dump(self.data_ids, f, indent=4)
            json.dump(self.data_specie_id, f2, indent=4)

    def handle_txt(self):
        pass

    def handle_csv(self, file_path):
        self.data[file_path] = {}
        with open(file_path, encoding = 'utf-8') as file:

            headers = file.readline().strip().split(self.csv_delimiter)
            header_id = headers[0]

            self.data_ids_column_main.setdefault(file_path, header_id)

            for line in file:
                values = line.strip().split(self.csv_delimiter)
                row = dict(zip(headers, values))
                value_id = row[header_id].strip('"')
                for header, value in row.items():
                    if header == 'scientfiicname':
                        self.data_specie_id[value] = value_id
                    self.data[file_path][value_id] = row

    def handle_xlsx(self):
        pass

ProcessData()
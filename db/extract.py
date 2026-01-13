import pandas as pd
import os

class ExcelExtractor:

    def __init__(self, excel_file_path, output_folder):
        self.excel_file = excel_file_path
        self.output_folder = output_folder
        self.csv_paths = {}

        self.tabs_config = {
            'Pátios': {'filename': 'patios.csv', 'header': 0},
            'Terminais': {'filename': 'terminais.csv', 'header': [0, 1]},
            'Entre Pátios': {'filename': 'entre_patios.csv', 'header': [0, 1, 2]},
            'Entre Trechos': {'filename': 'trechos_fisicos.csv', 'header': [0, 1]} 
        }

    def _flatten_headers(self, df, header_config):
        if isinstance(header_config, list):
            new_columns = []
            for col_name in df.columns.values:
                parts = [str(c).strip() for c in col_name if "Unnamed" not in str(c)]
                clean_name = "_".join(parts)
                new_columns.append(clean_name)
            df.columns = new_columns
        return df

    def run(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        print(f"1. [EXTRACT] Lendo arquivo: {os.path.basename(self.excel_file)}...")

        for excel_tab, config in self.tabs_config.items():
            output_path = os.path.join(self.output_folder, config['filename'])

            try:
                df_temp = pd.read_excel(
                    self.excel_file, 
                    sheet_name=excel_tab, 
                    header=config['header'], 
                    engine='openpyxl'
                )

                df_temp = self._flatten_headers(df_temp, config['header'])
                df_temp = df_temp.dropna(how='all')

                df_temp.to_csv(output_path, index=False, sep=';', encoding='utf-8')

                key_name = config['filename'].replace('.csv', '')
                self.csv_paths[key_name] = output_path

            except ValueError:
                print(f"   [AVISO] Aba '{excel_tab}' não encontrada. Pulando.")
                continue

        return self.csv_paths
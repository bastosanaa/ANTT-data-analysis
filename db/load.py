import sqlite3
import pandas as pd
import os

class DataModeler:
    """
    Responsible for the LOAD step.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.map_concessao = {}
        self.map_mercadoria = {}

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def _create_dim_concessoes(self, df_base):
        print("   [MODELAGEM] Criando dimensão 'dim_concessoes'...")

        dim = df_base[['ferrovia', 'ano']].drop_duplicates().reset_index(drop=True)
        dim['id_concessao'] = dim.index + 1

        dim.to_sql('dim_concessoes', self.conn, if_exists='replace', index=False)

        self.map_concessao = dict(zip(dim['ferrovia'], dim['id_concessao']))

    def _create_dim_mercadorias(self, df_terminais):
        print("   [MODELAGEM] Criando dimensão 'dim_mercadorias'...")

        mercadorias = df_terminais['mercadoria'].unique()
        dim = pd.DataFrame(mercadorias, columns=['nome'])
        dim = dim.dropna().sort_values('nome').reset_index(drop=True)
        dim['id_mercadoria'] = dim.index + 1

        dim.to_sql('dim_mercadorias', self.conn, if_exists='replace', index=False)

        self.map_mercadoria = dict(zip(dim['nome'], dim['id_mercadoria']))

    def _create_dim_linhas(self, df_patios):
        print("   [MODELAGEM] Criando dimensão 'dim_linhas'...")

        linhas_unicas = df_patios['nome_linha_limpo'].dropna().unique()

        dim = pd.DataFrame(linhas_unicas, columns=['nome_linha'])
        dim = dim[dim['nome_linha'] != ''] # Garante que não tem linha vazia
        dim = dim.sort_values('nome_linha').reset_index(drop=True)
        dim['id_linha'] = dim.index + 1

        dim.to_sql('dim_linhas', self.conn, if_exists='replace', index=False)

        self.map_linhas = dict(zip(dim['nome_linha'], dim['id_linha']))

    def _load_fact_patios(self, df_spark):
        print("   [MODELAGEM] Salvando tabela 'patios'...")
        df = df_spark.toPandas()

        df['id_concessao'] = df['ferrovia'].map(self.map_concessao)

        if hasattr(self, 'map_linhas'):
            df['id_linha'] = df['nome_linha_limpo'].map(self.map_linhas)

        cols_drop = ['ferrovia', 'ano', 'linhas_de_referencia', 'nome_linha_limpo']
        df_final = df.drop(columns=cols_drop, errors='ignore')

        df_final.to_sql('patios', self.conn, if_exists='replace', index=False)

    def _load_fact_terminais(self, df_spark):

        print("   [MODELAGEM] Salvando tabela 'terminais'...")
        df = df_spark.toPandas()

        df['id_concessao'] = df['ferrovia'].map(self.map_concessao)
        df['id_mercadoria'] = df['mercadoria'].map(self.map_mercadoria)

        df_final = df.drop(columns=['ferrovia', 'ano', 'mercadoria'], errors='ignore')

        df_final.to_sql('terminais', self.conn, if_exists='replace', index=False)

    def _load_fact_trechos(self, df_spark):
        print("   [MODELAGEM] Salvando tabela 'trechos_fisicos'...")
        df = df_spark.toPandas()

        df['id_concessao'] = df['ferrovia'].map(self.map_concessao)

        df_final = df.drop(columns=['ferrovia', 'ano'], errors='ignore')

        df_final.to_sql('trechos_fisicos', self.conn, if_exists='replace', index=False)

    def run(self, dfs_spark):
        """
        Método principal que orquestra a carga.
        Recebe: Dicionário de DataFrames do Spark
        """
        self._connect()

        if 'patios' in dfs_spark:
            df_patios_pd = dfs_spark['patios'].toPandas()
            self._create_dim_concessoes(df_patios_pd)
            self._create_dim_linhas(df_patios_pd)

        if 'terminais' in dfs_spark:
            df_term = dfs_spark['terminais'].toPandas()
            self._create_dim_mercadorias(df_term)

        if 'patios' in dfs_spark:
            self._load_fact_patios(dfs_spark['patios'])

        if 'terminais' in dfs_spark:
            self._load_fact_terminais(dfs_spark['terminais'])

        if 'trechos_fisicos' in dfs_spark:
            self._load_fact_trechos(dfs_spark['trechos_fisicos'])

        self.conn.close()
        print(f"\nSUCESSO! Banco Relacional modelado em: {self.db_path}")

def load_data(dfs, db_path):
    modeler = DataModeler(db_path)
    modeler.run(dfs)

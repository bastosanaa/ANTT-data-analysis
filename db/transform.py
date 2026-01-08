import unicodedata
import re
from pyspark.sql.functions import col, split, regexp_replace, trim

class SparkTransformer:
    """
    Responsável pela limpeza, normalização e tipagem dos dados usando PySpark.
    """
    
    def __init__(self, spark_session):
        self.spark = spark_session
        self.cleaned_dfs = {} # Estado: Guarda os DataFrames prontos

    def _normalize_text(self, text):
        """Normaliza strings (remove acentos e caracteres especiais)"""
        if not text: return ""
        nfkd = unicodedata.normalize('NFKD', text)
        text = "".join([c for c in nfkd if not unicodedata.combining(c)])
        text = text.lower()
        text = re.sub(r'[().]', '', text)
        text = re.sub(r'[ /]', '_', text)
        return text

    def _clean_column_names(self, df):
        """Aplica a normalização em todas as colunas"""
        for column in df.columns:
            new_name = self._normalize_text(column)
            df = df.withColumnRenamed(column, new_name)
        return df

    def _process_trechos_fisicos(self, df):
        """Lógica de negócio específica para a tabela de trechos"""
        cols_faixa = [c for c in df.columns if 'faixa_km' in c]
        
        for c_faixa in cols_faixa:
            prefixo = c_faixa.replace('_faixa_km', '').replace('faixa_km', '')
            nome_inicio = f"{prefixo}_inicio_faixa"
            nome_fim = f"{prefixo}_fim_faixa"
            
            df = df.withColumn(nome_inicio, split(col(c_faixa), " à ").getItem(0))
            df = df.withColumn(nome_fim, split(col(c_faixa), " à ").getItem(1))
            
            df = df.withColumn(nome_inicio, regexp_replace(col(nome_inicio), ",", ".").cast("double"))
            df = df.withColumn(nome_fim, regexp_replace(col(nome_fim), ",", ".").cast("double"))

        for col_name in df.columns:
            if col_name in cols_faixa: continue
            
            keywords = ['vma', 'velocidade', 'carga', 'eixo', 'taxa', 'gabarito']
            if any(x in col_name for x in keywords):
                df = df.withColumn(col_name, regexp_replace(col(col_name), ",", ".").cast("double"))
                
        return df
    
    def _clean_line_name(self, df):
        """
        Remove a informação de quilometragem da coluna de linha.
        Ex: 'Santos - Jundiaí (km 86,062)' -> 'Santos - Jundiaí'
        """
        col_name = 'linhas_de_referencia'
        
        if col_name in df.columns:
            
            df = df.withColumn(
                'nome_linha_limpo', 
                regexp_replace(col(col_name), r"\s*\(km.*", "")
            )
            df = df.withColumn('nome_linha_limpo', trim(col('nome_linha_limpo')))
            
        return df

    def run(self, paths_dict):
        """Executa a transformação em todas as tabelas recebidas"""
        print("\n2. [TRANSFORM] Normalizando dados com PySpark...")
        
        for table_name, path in paths_dict.items():
            df = self.spark.read.csv(path, header=True, inferSchema=True, sep=';')
            
            df = self._clean_column_names(df)
            
            if "ferrovia" in df.columns:
                df = df.filter(col("ferrovia").isNotNull())

            if table_name == 'patios':
                df = self._clean_line_name(df)
                
            if table_name == 'trechos_fisicos':
                df = self._process_trechos_fisicos(df)

            self.cleaned_dfs[table_name] = df
            print(f"   -> Tabela '{table_name}' pronta: {df.count()} registros.")
            
        return self.cleaned_dfs
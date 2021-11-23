from pyspark.sql import SparkSession, functions as f

# funcao para traducao das colunas
def translate(col):
    if col == 'Title':
        return 'Titulo'
    elif col == 'Genre':
        return 'Genero'
    elif col == 'GenreLabels':
        return 'RotuloGenero'
    elif col == 'Premiere':
        return 'PreEstreia'
    elif col == 'Seasons':
        return 'Temporadas'
    elif col == 'SeasonsParsed':
        return 'TemporadasAnalisadas'
    elif col == 'EpisodesParsed':
        return 'EpisodiosAnalisados'
    elif col == 'Length':
        return 'Duracao'
    elif col == 'MinLength':
        return 'DuracaoMinima'
    elif col == 'MaxLength':
        return 'DuracaoMaxima'
    elif col == 'Status':
        return 'Status'
    elif col == 'Active':
        return 'Ativo'
    elif col == 'Table':
        return 'Tabela'
    elif col == 'Language':
        return 'Linguagem'
    else:
        return col

if __name__ == "__main__":
    spark = SparkSession.builder\
        .appName("HousePriceSolution")\
        .master("local[*]")\
        .getOrCreate()

    arquivo = spark.read.parquet('analise_pyspark/arquivos_entrada_pyspark/OriginaisNetflix.parquet')
    print("Amostra do arquivo extraido")
    arquivo.show(5)

    # ==== 1)
    for col in arquivo.columns:
        if col in ['Premiere', 'dt_inclusao']:
            arquivo = arquivo.withColumn(col, arquivo[col].cast('timestamp'))

    arquivo.dtypes

    # ==== 2)
    arquivo = arquivo.orderBy(arquivo["Genre"], arquivo["Active"].desc())
    
    print('Amostra de dados agrupados por genero e Ativo\n')
    arquivo[['Genre', 'Active']].show(5)

    # ==== 3)

    # removendo duplicatas
    arquivo.drop_duplicates()

    # renomeando registro TBA por a ser anunciado
    arquivo = arquivo.withColumn("Seasons",
                                f.when(arquivo.Seasons == 'TBA', 'a ser anunciado')\
                                .otherwise(arquivo.Seasons))

    # ==== 4)

    # Criando campo Data de Alteracao com a data atual
    arquivo = arquivo.withColumn("Data de Alteracao", f.current_date())

    # ==== 5)

    # aplicando a funcao translate nas colunas, atraves de uma list comprehension
    colunas_traduzidas = [translate(col) for col in arquivo.columns]

    arquivo = arquivo.toDF(*colunas_traduzidas)

    print('Amostra dos dados com colunas traduzidas')
    arquivo.show(5)

    # ==== 6)
    # testando arquivo atraves no prompt de comando atraves do
    # spark-submit analise_pyspark.py

    # ==== 7)

    # salvando csv com apenas um arquvio
    arquivo_to_save = arquivo[['Titulo', 'Genero', 'Temporadas', 'PreEstreia', 'Linguagem', 'Ativo', 'Status', 'dt_inclusao', 'Data de Alteracao']]
    print("Amostra dos dados a serem exportados")
    arquivo_to_save.show(5)

    arquivo_to_save.repartition(1)\
        .write\
        .option('delimiter', ';')\
        .option('header', True)\
        .mode('overwrite')\
        .csv('analise_pyspark/arquivos_saida_pyspark/OriginaisNetflixCSV')

    #spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a._", "s3.amazonaws.com")
    #arquivo.write.csv("s3a://")

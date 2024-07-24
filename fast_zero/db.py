from sqlalchemy import create_engine, text

# Substitua pelos seus detalhes de conexão
server = 'DESKTOP-8C7557M'  # ou o nome do seu servidor
database = 'funay'
driver = 'ODBC Driver 17 for SQL Server'

# Montar a string de conexão
connection_string = f'mssql+pyodbc://@{server}/{database}?driver={driver}&Trusted_Connection=yes'

# Criar o engine
engine = create_engine(connection_string)

# Testar a conexão
with engine.connect() as connection:
    result = connection.execute(text('SELECT @@version;'))
    for row in result:
        print(row)

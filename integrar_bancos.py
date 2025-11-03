import sqlite3

# Conectar ao banco principal (sefp.db)
conn1 = sqlite3.connect('sefp.db')
cursor1 = conn1.cursor()

# Conectar ao banco secundário (db)
conn2 = sqlite3.connect('db')
cursor2 = conn2.cursor()

# Listar todas as tabelas no banco secundário
cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor2.fetchall()

# Iterar sobre cada tabela do banco secundário
for table_name in tables:
    table_name = table_name[0]  # Nome da tabela
    print(f"Integrando tabela: {table_name}")

    # Obter a estrutura da tabela
    cursor2.execute(f"PRAGMA table_info({table_name})")
    columns = cursor2.fetchall()
    column_definitions = ", ".join([f"{col[1]} {col[2]}" for col in columns])

    # Criar a tabela no banco principal, se ainda não existir
    cursor1.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")

    # Copiar os dados da tabela
    cursor2.execute(f"SELECT * FROM {table_name}")
    rows = cursor2.fetchall()
    if rows:
        placeholders = ", ".join(["?" for _ in columns])
        cursor1.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)

# Salvar as alterações e fechar as conexões
conn1.commit()
conn1.close()
conn2.close()

print("Integração concluída com sucesso!")
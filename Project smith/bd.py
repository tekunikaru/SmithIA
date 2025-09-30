import mariadb
import csv

conn = mariadb.connect(
    user="root",
    host="127.0.0.1",
    port=3306,
    database="project_smith"
)
cur = conn.cursor()


with open("registros_maquinas.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Pular o cabeçalho
    for row in reader:
        cur.execute(
            "INSERT INTO medicoes (id_maquina, variavel, valor, timestamp) VALUES (?, ?, ?, ?)",
            (int(row[0]), row[1], float(row[2]), row[3])
        )

conn.commit()
conn.close()

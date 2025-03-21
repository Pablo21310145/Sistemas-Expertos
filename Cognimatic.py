

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:34:50 2025

@author: Aspire
"""

import sqlite3

# Conectar a la base de datos de Cognimatic (en este caso un ejemplo simple con SQLite)
conn = sqlite3.connect('cognimatic.db')
cursor = conn.cursor()

# Consultar datos relevantes
cursor.execute("SELECT * FROM conocimiento")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()


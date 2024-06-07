import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk

def connect_to_db(server, database, username, password):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return conn

def add_record():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        table = table_entry.get()
        data = {}

        for entry in entries:
            column, value = entry[0].get(), entry[1].get()
            if column and value:
                data[column] = value

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = conn.cursor()
        cursor.execute(sql, tuple(data.values()))
        conn.commit()
        messagebox.showinfo("Éxito", "Registro agregado exitosamente")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_records():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        table = table_entry.get()
        sql = f"SELECT * FROM {table}"
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in tree.get_children():
            tree.delete(row)

        columns = [column[0] for column in cursor.description]
        tree["columns"] = columns

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_record():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        table = table_entry.get()
        set_clauses = []
        values = []
        where_clause = None

        for entry in entries:
            column, value = entry[0].get(), entry[1].get()
            if column.lower() == 'id':
                where_clause = f"WHERE {column} = ?"
                values.append(value)
            else:
                set_clauses.append(f"{column} = ?")
                values.insert(0, value)

        set_clause = ", ".join(set_clauses)
        sql = f"UPDATE {table} SET {set_clause} {where_clause}"
        cursor = conn.cursor()
        cursor.execute(sql, tuple(values))
        conn.commit()
        messagebox.showinfo("Éxito", "Registro actualizado exitosamente")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_record():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        table = table_entry.get()
        record_id = record_id_entry.get()
        sql = f"DELETE FROM {table} WHERE id = ?"
        cursor = conn.cursor()
        cursor.execute(sql, (record_id,))
        conn.commit()
        messagebox.showinfo("Éxito", "Registro eliminado exitosamente")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def advanced_query():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        table = table_entry.get()
        filters = {}

        for entry in entries:
            column, value = entry[0].get(), entry[1].get()
            if column and value:
                filters[column] = value

        where_clauses = [f"{column} = ?" for column in filters]
        where_clause = " AND ".join(where_clauses)
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        cursor = conn.cursor()
        cursor.execute(sql, tuple(filters.values()))
        rows = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        columns = [column[0] for column in cursor.description]
        tree["columns"] = columns

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def sorted_query():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        table = table_entry.get()
        sort_column = sort_column_entry.get()
        sql = f"SELECT * FROM {table} ORDER BY {sort_column}"
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        columns = [column[0] for column in cursor.description]
        tree["columns"] = columns

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def join_query():
    try:
        conn = connect_to_db(server_entry.get(), db_entry.get(), user_entry.get(), password_entry.get())
        join_sql = join_sql_entry.get()
        cursor = conn.cursor()
        cursor.execute(join_sql)
        rows = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        columns = [column[0] for column in cursor.description]
        tree["columns"] = columns

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_entry_fields():
    frame = tk.Frame(root)
    frame.pack()

    column_label = tk.Label(frame, text="Columna:")
    column_label.pack(side=tk.LEFT)
    column_entry = tk.Entry(frame)
    column_entry.pack(side=tk.LEFT)

    value_label = tk.Label(frame, text="Valor:")
    value_label.pack(side=tk.LEFT)
    value_entry = tk.Entry(frame)
    value_entry.pack(side=tk.LEFT)

    entries.append((column_entry, value_entry))

root = tk.Tk()
root.title("Base de Datos SQL Server")

server_label = tk.Label(root, text="Servidor:")
server_label.pack()
server_entry = tk.Entry(root)
server_entry.pack()

db_label = tk.Label(root, text="Base de Datos:")
db_label.pack()
db_entry = tk.Entry(root)
db_entry.pack()

user_label = tk.Label(root, text="Usuario:")
user_label.pack()
user_entry = tk.Entry(root)
user_entry.pack()

password_label = tk.Label(root, text="Contraseña:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

table_label = tk.Label(root, text="Tabla:")
table_label.pack()
table_entry = tk.Entry(root)
table_entry.pack()

entries = []

add_column_button = tk.Button(root, text="Agregar Columna y Valor", command=add_entry_fields)
add_column_button.pack()

add_button = tk.Button(root, text="Agregar Registro", command=add_record)
add_button.pack()

show_button = tk.Button(root, text="Mostrar Registros", command=show_records)
show_button.pack()

update_button = tk.Button(root, text="Actualizar Registro", command=update_record)
update_button.pack()

delete_frame = tk.Frame(root)
delete_frame.pack()

record_id_label = tk.Label(delete_frame, text="ID del Registro a Eliminar:")
record_id_label.pack(side=tk.LEFT)
record_id_entry = tk.Entry(delete_frame)
record_id_entry.pack(side=tk.LEFT)

delete_button = tk.Button(root, text="Eliminar Registro", command=delete_record)
delete_button.pack()

# Consultas avanzadas
advanced_query_button = tk.Button(root, text="Consulta Avanzada", command=advanced_query)
advanced_query_button.pack()

# Consultas ordenadas
sort_column_label = tk.Label(root, text="Columna para Ordenar:")
sort_column_label.pack()
sort_column_entry = tk.Entry(root)
sort_column_entry.pack()

sorted_query_button = tk.Button(root, text="Consulta Ordenada", command=sorted_query)
sorted_query_button.pack()

# Consultas multitablas (joins)
join_sql_label = tk.Label(root, text="SQL para Join:")
join_sql_label.pack()
join_sql_entry = tk.Entry(root)
join_sql_entry.pack()

join_query_button = tk.Button(root, text="Consulta Multitabla", command=join_query)
join_query_button.pack()

tree = ttk.Treeview(root)
tree.pack()

root.mainloop()

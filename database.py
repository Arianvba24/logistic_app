import pandas as pd
import sqlite3


def query_list():
    connection = sqlite3.connect("products.db")


    try:

        query = "SELECT * FROM stock"

        db = pd.read_sql(query,con=connection)

        dblist= db.columns.to_list()

    except:

        pass

    connection.close()
    return dblist

def query_database(column,value):
    connection = sqlite3.connect("products.db")


    try:

        query = f"SELECT * FROM stock WHERE {column} LIKE '%{value}%'"

        db = pd.read_sql(query,con=connection)

        db= df.columns.to_list()

    except:

        pass

    connection.close()
    return db

def update_extract(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM stock WHERE ID = {code_value}")
        value = cursor.fetchall()

        # for value in values:
        #     print(value)

    except:
        pass

    connection.commit()
    connection.close()
    return value

def query_update(id,code_bar,product,brand,provider,quantity,date):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"UPDATE stock SET Codebar_ID = {code_bar},Product = '{product}',Brand = '{brand}',Provider = '{provider}',Quantity = {quantity},Date = '{date}' WHERE ID = {id};")
        # value = cursor.fetchall()

        # for value in values:
        #     print(value)

    except:
        pass




    connection.commit()
    connection.close()
    # return value

def query_delete(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM stock WHERE ID = {code_value};")
    

    except:
        pass

    connection.commit()
    connection.close()


def query_products_list():
    connection = sqlite3.connect("products.db")


    try:

        query = "SELECT * FROM products"

        db = pd.read_sql(query,con=connection)

        dblist= db.columns.to_list()

    except:

        pass

    connection.close()
    return dblist

def query_products(selected_column,filtered_value):
    connection = sqlite3.connect("products.db")


    try:

        query = f"SELECT * FROM products WHERE {selected_column} LIKE '%{filtered_value}%'"

        db = pd.read_sql(query,con=connection)

        

    except:

        pass

    connection.close()
    return db

def update_product_extract(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM products WHERE ID = {code_value}")
        value = cursor.fetchall()


    except:
        pass

    connection.commit()
    connection.close()
    return value


def query_product_update(id,code_bar,product,brand,provider):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"UPDATE products SET Codebar_ID = {code_bar},Product = '{product}',Brand = '{brand}',Provider = '{provider}' WHERE ID = {id};")
        # value = cursor.fetchall()

        # for value in values:
        #     print(value)

    except:
        pass

    connection.commit()
    connection.close()


def query_product_delete(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM products WHERE ID = {code_value};")
    

    except:
        pass

    connection.commit()
    connection.close()


def insert_product_value(codebar,product,brand,provider):
    connection = sqlite3.connect("products.db")
    try:
        cursor = connection.cursor()

        # cursor.execute(f"INSERT INTO products VALUES (null,{codebar},'{product}','{brand}','{provider}');")
        cursor.execute(f"INSERT INTO products VALUES (null,?,?,?,?);",(codebar,product,brand,provider))

    except:
        print("No se ha introducido el valor")
        print(f"{codebar},'{product}','{brand}','{provider}'")

    connection.commit()
    connection.close()



def insert_min_stock_value(codebar,product,brand,provider,op,ns,ss,ls):
    connection = sqlite3.connect("products.db")
    try:
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO min_stock VALUES (null,?,?,?,?,?,?,?,?);",(codebar,product,brand,provider,op,ns,ss,ls))

    except:
        pass

    connection.commit()
    connection.close()

def query_min_stock(selected_column,filtered_value):
    connection = sqlite3.connect("products.db")


    try:

        query = f"SELECT * FROM min_stock WHERE {selected_column} LIKE '%{filtered_value}%'"

        db = pd.read_sql(query,con=connection)

        

    except:

        pass

    connection.close()
    return db

def update_min_stock_extract(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM min_stock WHERE ID = {code_value}")
        value = cursor.fetchall()


    except:
        pass

    connection.commit()
    connection.close()
    return value

def query_min_stock_update(id_data,barcode,product,brand,provider,os,ns,ss,ls):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()
        print("hola")
        
        cursor.execute(f"UPDATE min_stock SET 'Optimus stock' = ?,'Normal stock' = ?, 'Safety stock' = ?,'Low stock' = ? WHERE ID = ?",(os,ns,ss,ls,id_data))
        # value = cursor.fetchall()

        # for value in values:
        #     print(value)

    except:
        pass
        # print(f"UPDATE min_stock SET 'Optimus stock' = ?,'Normal stock' = ?, 'Safety stock' = ?,'Low stock' = ? WHERE ID = ?"(os,ns,ss,ls,id_data))

    connection.commit()
    connection.close()

def query_min_stock_delete(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM min_stock WHERE Codebar_ID = {code_value};")
    

    except:
        pass

    connection.commit()
    connection.close()



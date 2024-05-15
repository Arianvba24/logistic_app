import sqlite3
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def create_stock_dataframe():
    connection = sqlite3.connect(r"C:\Users\Cash\streamlit_apps\testing2004\logistic_app\products.db")

    query = r"""
    SELECT stock.Product,stock.Brand,stock.Provider,sum(stock."Quantity") as "Total Stock",min_stock."Optimus stock",min_stock."Normal stock",min_stock."Safety stock",min_stock."Low stock"
    FROM stock
    LEFT JOIN min_stock
    ON stock.Codebar_ID = min_stock.Codebar_ID
    GROUP BY stock.Product
    ORDER by "Total Stock" DESC;

    """
    try:
        df = pd.read_sql(query,con=connection)
        
    except:
        pass

    connection.close()


    df

    def create_df(row):
        if row["Total Stock"] > (row["Normal stock"] + row["Safety stock"]+row["Low stock"]):
            return row["Total Stock"] - (row["Normal stock"] + row["Safety stock"]+row["Low stock"])
        else:
            return 0
        
    def create_df1(row):
        if row["OS"] == 0:
            value = row["Total Stock"] - (row["Safety stock"]+row["Low stock"])
        else:
            value = row["Normal stock"]
        
        if value < 0:
            return 0
        elif value == row["Normal stock"]:
            return value
        else:
            return row["Total Stock"] - (row["Safety stock"]+row["Low stock"])
        
    def create_df2(row):
        if row["NS"] == 0:
            value = row["Total Stock"] - row["Low stock"]
        else:
            value = row["Safety stock"]
        
        if value < 0:
            return 0
        elif value == row["Safety stock"]:
            return value
        else:
            return row["Total Stock"] - row["Low stock"]
            
    def create_df3(row):
        if row["SS"] == 0:
            return row["Total Stock"]
        else:
            return row["Low stock"]


    df["OS"] = df.apply(create_df,axis=1)
    df["NS"] = df.apply(create_df1,axis=1)
    df["SS"] = df.apply(create_df2,axis=1)
    df["LS"] = df.apply(create_df3,axis=1)
    dx = df.copy()
    columns = df.columns.to_list()[4:8]
    columns_name = {"OS": 'Optimus stock',"NS":'Normal stock', "SS" : 'Safety stock', "LS": 'Low stock'}
    dx.drop(columns = columns,inplace = True)
    dx.rename(columns = columns_name,inplace=True)
    dx = dx.sort_values(by="Total Stock",ascending=True)
    return dx

def create_chart(dx):
    

    fig = go.Figure()


    fig.add_trace(
        go.Bar(y = dx["Product"].values,
        x = dx["Optimus stock"].values,orientation= "h",name="Optimus stock",marker_color="#92D050"),
    )
    fig.add_trace(
        go.Bar(y = dx["Product"].values,
        x = dx["Normal stock"].values,orientation= "h",name="Normal stock",marker_color="#FFFF00"))

    fig.add_trace(
        go.Bar(y = dx["Product"].values,
        x = dx["Safety stock"].values,orientation= "h",name="Safety stock",marker_color="#FFC000"))

    fig.add_trace(
        go.Bar(y = dx["Product"].values,
        x = dx["Low stock"].values,orientation= "h",name="Low stock",marker_color="#FF0000"))


    fig.update_layout(
        title="Stock Comparison by Product",
        barmode="stack",  # Agrupa las barras
        xaxis_title="Stock Quantity",
        yaxis_title="Product",
        legend_title="Stock Type",
        height=800,  # Altura del gráfico
        width=800,
        legend_traceorder="grouped"# Anchura del gráfico
    )


    return fig



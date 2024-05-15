import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import cv2
from pyzbar.pyzbar import decode
import sqlite3
import datetime
import time
from streamlit_searchbox import st_searchbox
from database import *
from stock_analysis import *
from st_on_hover_tabs import on_hover_tabs


dt = datetime.datetime.now()
dp = f"{dt.year}-{dt.month:02d}-{dt.day:02d}"


# def BarcodeReader(image): 
#     # read the image in numpy array using cv2 
#     img = cv2.imread(image) 
       
#     # Decode the barcode image 
#     detectedBarcodes = decode(img) 
       
#     # If not detected then print the message 
#     if not detectedBarcodes: 
#         print("Barcode Not Detected or your barcode is blank/corrupted!") 
#     else: 
#         # Traverse through all the detected barcodes in image 
#         for barcode in detectedBarcodes:   
#             # Locate the barcode position in image 
#             (x, y, w, h) = barcode.rect 
#             # Put the rectangle in image to highlight the barcode 
#             cv2.rectangle(img, (x-10, y-10), 
#                           (x + w+10, y + h+10),  
#                           (255, 0, 0), 2) 
              
#             if barcode.data!="": 
#                 # Print the barcode data 
#                 return barcode.data
def code_extractor(image_file):

        if image_file is not None:
        # Leer la imagen utilizando OpenCV
            image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), 1)
            
        # Verificar si la imagen se cargó correctamente
            if image is not None:
                # st.image(image, caption="Imagen cargada", use_column_width=True)
                # st.write("hola")
                detectedBarcodes = decode(image)
        
                for barcode in detectedBarcodes:
                
                    # Locate the barcode position in image 
                    (x, y, w, h) = barcode.rect 
                    # Put the rectangle in image to highlight the barcode 
                    cv2.rectangle(image, (x-10, y-10), 
                                (x + w+10, y + h+10),  
                                (255, 0, 0), 2) 
                    
                    if barcode.data!="": 
                        # Print the barcode data 
                        return str(barcode.data.decode("utf-8"))
                if not detectedBarcodes: 
                    st.write("Barcode Not Detected or your barcode is blank/corrupted!") 
            else: 
                pass

        else:
            st.error("No se pudo cargar la imagen.")

# Code bar reader
def create_query(code_value):
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM products WHERE Codebar_ID = {code_value}")
        value = cursor.fetchall()

        # for value in values:
        #     print(value)

    except:
        pass

    connection.commit()
    connection.close()
    return value

def list_products():
    connection = sqlite3.connect("products.db")
    try:
        
        cursor = connection.cursor()

        query = f"SELECT * FROM products"

        # xp = cursor.fetchall()
        df = pd.read_sql(query,con=connection)
        # st.table(df)
        xp = df["Product"].values

        # for value in values:
        #     print(value)

    except:
        pass

    connection.commit()
    connection.close()
    return xp

def insert_data(barcode,product,brand,provider,quantity):
    connection = sqlite3.connect("products.db")
    fx_value = (barcode, product, brand, provider,quantity,dp)
    try:
        
        cursor = connection.cursor()

        cursor.execute("INSERT INTO stock VALUES (null,?,?,?,?,?,?)",fx_value)
    except:
        pass

    connection.commit()
    connection.close()

def look_up(code_value):
    connection = sqlite3.connect("products.db")
    try:
        code = code_value.strip()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM products WHERE Product = '{code}'")
        value = cursor.fetchall()

        # for value in values:
        #     print(value)

    except:
        pass

    connection.commit()
    connection.close()
    return value
    
def main():
    
    st.set_page_config(layout="wide")
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
    
    # menu = ["Code bar reader","Stock Analysis","Database","About"]
    # value = st.sidebar.selectbox("Menu",menu)
    with st.sidebar:
        value = on_hover_tabs(tabName=["Code bar reader","Stock Analysis","Database","About"], 
                         iconName=['dashboard', 'money', 'economy',""], default_choice=0)

    if value == "Code bar reader":

        st.title("Code bar reader")
        st.markdown("#### Upload the picture to analyze the following stock")
        image_file = st.file_uploader("Upload Image",type=["png","jpg","jpeg"])
     
        try:

            if image_file:
                code_value = code_extractor(image_file)
                st.title(code_value)
                final_value = create_query(code_value)
                if len(final_value) == 0:
                    st.warning("Non value detected")
                else:

                    tab1a,tab2a = st.tabs(["Stock entry","Stock out"])
                    with tab1a:

                        tab1,tab2 = st.tabs(["Code bar reader","Manual insertion"])
                        


                        

                        
                        with tab1:
                            with st.form("value"):
                                # col1,col2 = st.columns([8,5])
                                # with col1:
                                col1a,col2a,col3a = st.columns([2,4,4])
                                with col1a:

                                    barcode = st.text_input("ID", value = code_value,disabled=True)

                                with col2a:
                                    quantity = st.number_input("Insert quantity",1,1200)
                                # with col2a:

                                product = st.text_input("Product", value = final_value[0][2],disabled=True)
                                
                                # with col2a:
                                col1b,col2b = st.columns([3,5])
                                with col1b:

                                    brand = st.text_input("Brand", value = final_value[0][3],disabled=True)
                                with col2b:

                                    provider = st.text_input("Provider", value = final_value[0][4],disabled=True)




                                if st.form_submit_button("Submit data"):
                                    st.success("Product registed succesfully!")
                                    insert_data(barcode,product,brand,provider,quantity)

                        with tab2:
                            
                            product = st.selectbox("Product", list_products())
                            value_p = look_up(product)
                            
                            with st.form("value2"):
                                # col1,col2 = st.columns([8,5])
                                # with col1:
                                col1a,col2a,col3a = st.columns([2,4,4])
                                with col1a:

                                    barcode = st.text_input("ID", value = value_p[0][1],disabled=True)

                                with col2a:
                                    quantity = st.number_input("Insert quantity",1,1200)
                                # with col2a:

                                # product = st.text_input("Product", value = final_value[0][2])
                                # -------------------
                                

                                # -------------------
                                # product = st.selectbox("Product", list_products())
                                # st.dataframe(list_products())
                                
                                # with col2a:
                                col1b,col2b = st.columns([3,5])
                                with col1b:

                                    brand = st.text_input("Brand", value = value_p[0][3],disabled=True)
                                with col2b:

                                    provider = st.text_input("Provider", value = value_p[0][4],disabled=True)




                                if st.form_submit_button("Submit data"):
                                    st.success("Product registed succesfully!")
                                    insert_data(barcode,product,brand,provider,quantity)

                    with tab2a:

                        tab1,tab2 = st.tabs(["Code bar reader","Manual insertion"])
                        

                        final_value = create_query(code_value)
                        
                        with tab1:
                            with st.form("value4"):
                                # col1,col2 = st.columns([8,5])
                                # with col1:
                                col1a,col2a,col3a = st.columns([2,4,4])
                                with col1a:

                                    barcode = st.text_input("ID", value = code_value,disabled=True)

                                with col2a:
                                    quantity = st.number_input("Insert quantity",-20,-1,-2)
                                # with col2a:

                                product = st.text_input("Product", value = final_value[0][2],disabled=True)
                                
                                # with col2a:
                                col1b,col2b = st.columns([3,5])
                                with col1b:

                                    brand = st.text_input("Brand", value = final_value[0][3],disabled=True)
                                with col2b:

                                    provider = st.text_input("Provider", value = final_value[0][4],disabled=True)




                                if st.form_submit_button("Submit data"):
                                    st.success("Product registed succesfully!")
                                    insert_data(barcode,product,brand,provider,quantity)

                        with tab2:
                            
                            product = st.selectbox("Product", list_products(),key="box2")
                            value_p = look_up(product)
                            
                            with st.form("value7"):
                                # col1,col2 = st.columns([8,5])
                                # with col1:
                                col1a,col2a,col3a = st.columns([2,4,4])
                                with col1a:

                                    barcode = st.text_input("ID", value = value_p[0][1],disabled=True)

                                with col2a:
                                    quantity = st.number_input("Insert quantity",-20,-1,-1)
                                # with col2a:

                                # product = st.text_input("Product", value = final_value[0][2])
                                # -------------------
                                

                                # -------------------
                                # product = st.selectbox("Product", list_products())
                                # st.dataframe(list_products())
                                
                                # with col2a:
                                col1b,col2b = st.columns([3,5])
                                with col1b:

                                    brand = st.text_input("Brand", value = value_p[0][3],disabled=True)
                                with col2b:

                                    provider = st.text_input("Provider", value = value_p[0][4],disabled=True)




                                if st.form_submit_button("Submit data"):
                                    st.success("Product registed succesfully!")
                                    insert_data(barcode,product,brand,provider,quantity)
        except:
            pass

               
    if value == "Stock Analysis":
        st.title("Stock Analysis")
        col1,col2,col3 = st.columns([4,1,4])
        df = create_stock_dataframe()
        
        df_chart = create_chart(df.sort_values(by="Total Stock"))
        with col1:

            st.plotly_chart(df_chart)

        with col3:
            

            st.title(" ")
            st.markdown("Table with products")
            st.dataframe(df.sort_values(by="Total Stock",ascending=False))


    




    #Creating interactive database
    if value == "Database":
        st.title("Database")


        tab1,tab2 = st.tabs(["Stock","List of products"])

        with tab1:

            tab1a,tab2a,tab3a = st.tabs(["Search values","Update values","Delete values"])

            with tab1a:
                with st.form("Search value"):
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search value...")
                       
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_list() 
                        selected_column = st.selectbox("Column",query_list1)
                    
                    
                    values_b = st.form_submit_button("Filter")
                    if values_b:
                        df = query_database(selected_column,filtered_value)
                        st.dataframe(df)
                        # st.rerun()
            
            with tab2a:
                with st.form("Search and Update value"):
                    # st.write("food")
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search and Update")
                       
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_list() 
                        selected_column = st.selectbox("Column",query_list1)
                    
                    
                    # search_update_value_filter = True
                    if st.form_submit_button("Filter"):
                        
                        # global search_update_value_filter
                        # search_update_value_filter = not st.session_state["FormSubmitter:Search and Update value-Filter"]


                        df = query_database(selected_column,filtered_value)
                        st.dataframe(df)
                        
                

                # with st.form("Update value"):
                st.markdown("### Update value")
            

                
                
                col1a,col2a,col3a,col4a = st.columns([1,2,1,3])
                try:

                    with col1a:
                        
                        df = query_database(selected_column,filtered_value)
                        df_list= df.columns.to_list()
                        

                        id_data = st.text_input("ID",value=1)

                        final_value = update_extract(id_data)
                        # print(final_value)

                    with col2a:
                        barcode = st.text_input("Barcode",value = final_value[0][1],disabled=True)
                        

                    with col3a:
                        quantity = st.number_input("Insert quantity",1,1200)

                    with col4a:
                        date = st.date_input("Insert date")
                    # with col2a:

                    product = st.text_input("Product", value = final_value[0][2],disabled=True)
                    
                    # with col2a:
                    col1b,col2b = st.columns([3,5])
                    with col1b:

                        brand = st.text_input("Brand", value = final_value[0][3],disabled=True)
                    with col2b:

                        provider = st.text_input("Provider", value = final_value[0][4],disabled=True)
                except:
                    st.header("Non ID value added")
                    if "id_update" not in st.session_state:
                        st.session_state["id_update"] = True

                    else:
                        st.session_state["id_update"] = True
                

              
                if "counter" not in st.session_state:
                    st.session_state["counter"] = 1

                col1e,col2e = st.columns([0.50,0.7])
                with col1e:

                    xpl = st.button("Update")

                    # if xpl:
                    #     if st.session_state["id_update"] == True:
                    #         st.warning("Non ID detected")
                    #     else:
                    #         query_update(id_data,barcode,product,brand,provider,quantity,date)
                    #         for i in range(0,st.session_state["counter"]):
                    #             st.success("Value inserted!")

                    #         st.session_state["counter"] += 1

                if xpl:
                    if st.session_state["id_update"] == True:
                        st.warning("Non ID detected")
                    else:
                        query_update(id_data,barcode,product,brand,provider,quantity,date)
                        for i in range(0,st.session_state["counter"]):
                            st.success("Value updated!")

                        st.session_state["counter"] += 1


                            
                if "id_update" in st.session_state:
                    st.session_state["id_update"] = False

                        


                with col2e:
                    
                    xpk = st.button("Refresh All")



                if xpk:
                    # for i in range(0,st.session_state["counter"]):
                    st.success("Refreshed all forms!")
                    # st.session_state["FormSubmitter:Search and Update value-Filter"] = not st.session_state["FormSubmitter:Search and Update value-Filter"]

                    st.session_state["counter"] = 1
                

            with tab3a:
                with st.form("Search and Delete value"):
                    # st.write("food")
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search and Delete")
                       
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_list() 
                        selected_column = st.selectbox("Column",query_list1)
                    
                    
     
                    if st.form_submit_button("Filter"):
                        
            
                        df = query_database(selected_column,filtered_value)
                        st.dataframe(df)
                        
                

                # with st.form("Update value"):
                st.markdown("### Delete value")
            

                
                
                col1a,col2a,col3a,col4a = st.columns([1,2,1,3])
                try:

                    with col1a:
                        
                        df = query_database(selected_column,filtered_value)
                        df_list= df.columns.to_list()
                        

                        id_data = st.text_input("ID",value=1,key="009")

                        final_value = update_extract(id_data)
                        # print(final_value)

                    with col2a:
                        barcode = st.text_input("Barcode",value = final_value[0][1],disabled=True,key="010")
                        

                    with col3a:
                        quantity = st.number_input("Insert quantity",1,1200,key="0110",disabled=True)

                    with col4a:
                        date = st.date_input("Insert date",key="daiopd",disabled=True)
                    # with col2a:

                    product = st.text_input("Product", value = final_value[0][2],disabled=True,key="011")
                    
                    # with col2a:
                    col1d,col2d = st.columns([3,5])
                    with col1d:

                        brand = st.text_input("Brand", value = final_value[0][3],disabled=True,key="013")
                    with col2d:

                        provider = st.text_input("Provider", value = final_value[0][4],disabled=True,key="014")
                        if "id_value" not in st.session_state:
                            st.session_state["id_value"] = False
                except:
                    st.header("Non ID value added")
                    if "id_value" not in st.session_state:
                        st.session_state["id_value"] = True

                    else:
                        st.session_state["id_value"] = True
                
                

              
                if "del_counter" not in st.session_state:
                    st.session_state["del_counter"] = 1

                col1e,col2e = st.columns([0.50,0.7])
                with col1e:

                    xkl = st.button("Delete")
                        
                        
                        



                if xkl:
                    if st.session_state["id_value"] == True:
                        st.warning("ID value doesn't exist")

                    else:

                        
                        query_delete(id_data)
                    
                        for i in range(0,st.session_state["del_counter"]):
                            st.success("Value deleted!")

                        st.session_state["del_counter"] += 1


                with col2e:
                    
                    xpk = st.button("Refresh All",key="015")

                if xpk:
                    # for i in range(0,st.session_state["counter"]):
                    st.success("Refreshed all forms!")
                    # st.session_state["FormSubmitter:Search and Update value-Filter"] = not st.session_state["FormSubmitter:Search and Update value-Filter"]

                    st.session_state["del_counter"] = 1


         

                if "id_value" in st.session_state:

                    st.session_state["id_value"] = False

        with tab2:



            tab1aa,tab1a,tab2a,tab3a,tab4a = st.tabs(["Create product","Search product","Update products","Delete products","Security Stock"])

            with tab1aa:
                st.markdown("#### Create product")
                # col1a,col2a = st.columns([1,4])
                try:
                    
                    # with col1a:
                        
                    #     df = query_products(selected_column,filtered_value)
                    #     df_list= df.columns.to_list()
                        
                        

                    #     id_data = st.text_input("ID",value=1,key="01aaa")

                    #     final_value = update_product_extract(id_data)
                        

                    # with col2a:
                    barcode = st.text_input("Barcode",key="02aaa")
                        

                 

                    product = st.text_input("Product",key="05aaa")

                    
                    
                   
                    col1b,col2b = st.columns([3,5])
                    with col1b:

                        brand = st.text_input("Brand",key="06aaa")
                    with col2b:

                        provider = st.text_input("Provider",key="07aaa")
                        if "create_product" not in st.session_state:
                            st.session_state["create_product"] = False

                        else:
                            st.session_state["create_product"] = False
                except:
                    st.header("Non ID value added")
                    if "create_product" not in st.session_state:
                        st.session_state["create_product"] = True

                    else:
                        st.session_state["create_product"] = True


                
                if "counter" not in st.session_state:
                    st.session_state["counter"] = 1

                # if xjn:
                st.markdown("#### Stablish stock")

                col1ab,col2ab,col3ab,col4ab = st.columns([2,2,2,2])
                with col1ab:

                    max_stock = st.text_input("Max Stock/Optimus stock")

                with col2ab:
                    normal_stock = st.text_input("Normal stock")

                with col3ab:
                    safety_stock = st.text_input("Safety stock")

                with col4ab:
                    low_stock = st.text_input("Low stock")

                


                col1e,col2e = st.columns([0.50,0.7])
                with col1e:

                    # xpl1 = st.button("Update",key="021a")
                    xjn = st.button("Create product")


                if xjn:
                    if st.session_state["create_product"] == True:
                        st.warning("Non ID detected")
                    else:
                        insert_product_value(barcode,product,brand,provider)
                        insert_min_stock_value(barcode,product,brand,provider,max_stock,normal_stock,safety_stock,low_stock)
            
                        for i in range(0,st.session_state["counter"]):
                            st.success("Value updated!")

                        st.session_state["counter"] += 1


                            
                if "create_product" in st.session_state:
                    st.session_state["create_product"] = False

                with col2e:
                    
                    xpk = st.button("Refresh All",key="021aa")



                if xpk:
                    # for i in range(0,st.session_state["counter"]):
                    st.success("Refreshed all forms!")
                    # st.session_state["FormSubmitter:Search and Update value-Filter"] = not st.session_state["FormSubmitter:Search and Update value-Filter"]

                    st.session_state["counter"] = 1


            with tab1a:
                with st.form("Search product"):
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search product...")
                       
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_products_list()
                        selected_column = st.selectbox("Column",query_list1)
                    
                    
                    values_b = st.form_submit_button("Filter")
                    if values_b:
                        df = query_products(selected_column,filtered_value)
                        st.dataframe(df)
                        # st.rerun()
            
            with tab2a:
                with st.form("Search and Update product"):
                    # st.write("food")
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search and Update")
                       
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_products_list()
                        selected_column = st.selectbox("Column",query_list1)
                    
                    
                    # search_update_value_filter = True
                    if st.form_submit_button("Filter"):
                        
                        # global search_update_value_filter
                        # search_update_value_filter = not st.session_state["FormSubmitter:Search and Update value-Filter"]


                        df = query_products(selected_column,filtered_value)
                        st.dataframe(df)
                        
                

                # with st.form("Update value"):
                st.markdown("### Update value")
            

                
                
                col1a,col2a,col3a,col4a = st.columns([1,2,1,3])
                try:

                    with col1a:
                        
                        df = query_products(selected_column,filtered_value)
                        df_list= df.columns.to_list()
                        

                        id_data = st.text_input("ID",value=1,key="01a")

                        final_value = update_product_extract(id_data)
                        # print(final_value)

                    with col2a:
                        barcode = st.text_input("Barcode",value = final_value[0][1],disabled=True,key="02a")
                        

                    with col3a:
                        quantity = st.number_input("Insert quantity",1,1200,key="03a")

                    with col4a:
                        date = st.date_input("Insert date",key="04a")
                    # with col2a:

                    product = st.text_input("Product", value = final_value[0][2],key="05a")
                    
                    # with col2a:
                    col1b,col2b = st.columns([3,5])
                    with col1b:

                        brand = st.text_input("Brand", value = final_value[0][3],key="06a")
                    with col2b:

                        provider = st.text_input("Provider", value = final_value[0][4],key="07a")
                        if "id_product_update" not in st.session_state:
                            st.session_state["id_product_update"] = False

                        else:
                            st.session_state["id_product_update"] = False
                except:
                    st.header("Non ID value added")
                    if "id_product_update" not in st.session_state:
                        st.session_state["id_product_update"] = True

                    else:
                        st.session_state["id_product_update"] = True
                

              
                if "counter" not in st.session_state:
                    st.session_state["counter"] = 1

                col1e,col2e = st.columns([0.50,0.7])
                with col1e:

                    xpl1 = st.button("Update",key="021a")


                if xpl1:
                    if st.session_state["id_product_update"] == True:
                        st.warning("Non ID detected")
                    else:
                        query_product_update(id_data,barcode,product,brand,provider)
                        for i in range(0,st.session_state["counter"]):
                            st.success("Value updated!")

                        st.session_state["counter"] += 1


                            
                if "id_product_update" in st.session_state:
                    st.session_state["id_product_update"] = False

                        


                with col2e:
                    
                    xpk = st.button("Refresh All",key="021")



                if xpk:
                    # for i in range(0,st.session_state["counter"]):
                    st.success("Refreshed all forms!")
                    # st.session_state["FormSubmitter:Search and Update value-Filter"] = not st.session_state["FormSubmitter:Search and Update value-Filter"]

                    st.session_state["counter"] = 1
                

            with tab3a:
                with st.form("Search and Delete product"):
                    # st.write("food")
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search and Delete")
                       
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_products_list() 
                        selected_column = st.selectbox("Column",query_list1)
                    
                    
                    # search_update_value_filter = True
                    if st.form_submit_button("Filter"):
                        
                        # global search_update_value_filter
                        # search_update_value_filter = not st.session_state["FormSubmitter:Search and Update value-Filter"]


                        df = query_products(selected_column,filtered_value)
                        st.dataframe(df)
                        
                

                # with st.form("Update value"):
                st.markdown("### Delete value")
            

                
                
                col1a,col2a,col3a,col4a = st.columns([1,2,1,3])
                try:

                    with col1a:
                        
                        df = query_database(selected_column,filtered_value)
                        df_list= df.columns.to_list()
                        

                        id_data = st.text_input("ID",value=1,key="001b")

                        final_value = update_product_extract(id_data)
                        # print(final_value)

                    with col2a:
                        barcode = st.text_input("Barcode",value = final_value[0][1],disabled=True,key="002b")
                        

                    with col3a:
                        quantity = st.number_input("Insert quantity",1,1200,key="003b",disabled=True)

                    with col4a:
                        date = st.date_input("Insert date",key="00004b",disabled=True)
                    # with col2a:

                    product = st.text_input("Product", value = final_value[0][2],disabled=True,key="004b")
                    
                    # with col2a:
                    col1d,col2d = st.columns([3,5])
                    with col1d:

                        brand = st.text_input("Brand", value = final_value[0][3],disabled=True,key="005b")
                    with col2d:

                        provider = st.text_input("Provider", value = final_value[0][4],disabled=True,key="006b")
                        if "id_product_update" not in st.session_state:
                            st.session_state["id_product_update"] = False
                except:
                    st.header("Non ID value added")
                    if "id_product_update" not in st.session_state:
                        st.session_state["id_product_update"] = True

                    else:
                        st.session_state["id_product_update"] = True
                
                

              
                if "del_counter" not in st.session_state:
                    st.session_state["del_counter"] = 1

                col1e,col2e = st.columns([0.50,0.7])
                with col1e:

                    xkl = st.button("Delete",key="030b")
                        
                        
                        



                if xkl:
                    if st.session_state["id_product_update"] == True:
                        st.warning("ID value doesn't exist")

                    else:

                        
                        query_product_delete(id_data)
                        query_min_stock_delete(barcode)
                    
                        for i in range(0,st.session_state["del_counter"]):
                            st.success("Value deleted!")

                        st.session_state["del_counter"] += 1


                with col2e:
                    
                    xpk = st.button("Refresh All",key="035b")

                if xpk:
                    # for i in range(0,st.session_state["counter"]):
                    st.success("Refreshed all forms!")
                    # st.session_state["FormSubmitter:Search and Update value-Filter"] = not st.session_state["FormSubmitter:Search and Update value-Filter"]

                    st.session_state["del_counter"] = 1


         

                if "id_product_update" in st.session_state:

                    st.session_state["id_product_update"] = False


            with tab4a:
                
                st.markdown("#### Security Stock")
                with st.form("Search"):
                    col1,col2 = st.columns([4,2])
                    with col1:
                        st.markdown("### Search and stablish min stock")
                        
                     
                        filtered_value = st.text_input("Value")
                    with col2:
           
                        st.write(" ")
                        st.write(" ")
                        st.markdown("### ")
                       
                        query_list1 = query_products_list()
                        selected_column = st.selectbox("Column",query_list1)
                    
                    # stock_value = st.number_input("Min stock value",1)
                    
                    
                    values_b = st.form_submit_button("Filter")
                    if values_b:
                        df = query_min_stock(selected_column,filtered_value)
                        st.dataframe(df)

                st.markdown("### Update value")
            

                
                
                col1a,col2a,col3a,col4a = st.columns([1,2,1,3])
                try:

                    with col1a:
                        
                        df = query_products(selected_column,filtered_value)
                        df_list= df.columns.to_list()
                        

                        id_data = st.text_input("ID",value=1,key="01qa")

                        final_value = update_min_stock_extract(id_data)
                        # print(final_value)

                    with col2a:
                        barcode = st.text_input("Barcode",value = final_value[0][1],disabled=True,key="02qa")
                        

                    with col3a:
                        quantity = st.number_input("Insert quantity",1,1200,key="03aq",disabled=True)

                    with col4a:
                        pass
                        # date = st.date_input("Insert date",key="04aq",disabled=True)
                    # with col2a:

                    product = st.text_input("Product", value = final_value[0][2],key="05aq",disabled=True)
                    
                    # with col2a:
                    col1b,col2b = st.columns([3,5])
                    with col1b:

                        brand = st.text_input("Brand", value = final_value[0][3],key="06aq",disabled=True)
                    with col2b:

                        provider = st.text_input("Provider", value = final_value[0][4],key="07aq",disabled=True)
                        if "id_min_stock_update" not in st.session_state:
                            st.session_state["id_min_stock_update"] = False

                        else:
                            st.session_state["id_min_stock_update"] = False
                except:
                    st.header("Non ID value added")
                    if "id_min_stock_update" not in st.session_state:
                        st.session_state["id_min_stock_update"] = True

                    else:
                        st.session_state["id_min_stock_update"] = True
                

              
                if "counter" not in st.session_state:
                    st.session_state["counter"] = 1

                st.markdown("### Update stock patterns")

                col1ab,col2ab,col3ab,col4ab = st.columns([2,2,2,2])
                with col1ab:

                    max_stock = st.text_input("Max Stock/Optimus stock",value=final_value[0][5],key="0001qr")

                with col2ab:
                    normal_stock = st.text_input("Normal stock",value=final_value[0][6],key="0002qr")

                with col3ab:
                    safety_stock = st.text_input("Safety stock",value=final_value[0][7],key="0003qr")

                with col4ab:
                    low_stock = st.text_input("Low stock",value=final_value[0][8],key="0004qr")


                col1e,col2e = st.columns([0.50,0.7])
                with col1e:

                    xpl1 = st.button("Update",key="021aq")


                if xpl1:
                    if st.session_state["id_product_update"] == True:
                        st.warning("Non ID detected")
                    else:
                        query_min_stock_update(id_data,barcode,product,brand,provider,max_stock,normal_stock,safety_stock,low_stock)
                        for i in range(0,st.session_state["counter"]):
                            st.success("Value updated!")

                        st.session_state["counter"] += 1


                            
                if "id_product_update" in st.session_state:
                    st.session_state["id_product_update"] = False

                


                with col2e:
                    
                    xpk = st.button("Refresh All",key="021q")



                if xpk:
                    # for i in range(0,st.session_state["counter"]):
                    st.success("Refreshed all forms!")
                    # st.session_state["FormSubmitter:Search and Update value-Filter"] = not st.session_state["FormSubmitter:Search and Update value-Filter"]

                    st.session_state["counter"] = 1



             

                
                    
              
                    

                    
                













if __name__=="__main__":
    main()

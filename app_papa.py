# Librerías:
import pandas as pd
import numpy as np
import datetime
import streamlit as st
from st_aggrid import AgGrid

# obtener fecha actual:
fecha_actual = datetime.date.today()

# alistar dataframe:
df = pd.read_excel("EFEMERIDES.xlsx", nrows=123)
df = df.fillna(0)
df["day"] = df["day"].astype(str)
df["year"] = df["year"].astype(int)
df["year"] = df["year"].astype(str)
df["month"] = df["month"].astype(str)
df["Nacimiento"] = df["month"] + "/" + df["day"] + "/" + df["year"]
df["Nacimiento"] = pd.to_datetime(df["Nacimiento"])
df["Fecha_Actual"] = str(fecha_actual)
df["Fecha_Actual"] = pd.to_datetime(df["Fecha_Actual"])
df["Edad"] = round((df["Fecha_Actual"] - df["Nacimiento"]) / np.timedelta64(1, 'Y'), 0)
df["Edad"] = df["Edad"].astype(int)
df["MM-DD"] = df["Nacimiento"].dt.strftime('%m-%d')
df["MM-DD_actual"] = df["Fecha_Actual"].dt.strftime('%m-%d')

# generar tabla de últimos cumpleaños:
uc = df[df["MM-DD"] < df["MM-DD_actual"]].tail(10)[["NOMBRE", 
                                                   "Nacimiento", 
                                                   "Edad"]].reset_index(drop=True)[::-1]

# generar tabla proximos cumpleaños:
pc = df[df["MM-DD"] >= df["MM-DD_actual"]].head(10)[["NOMBRE", 
                                                    "Nacimiento", 
                                                    "Edad"]].reset_index(drop=True)

# Funciones:
@st.cache
def buscar_familiar(nombre):
    nombre = nombre.upper()
    temp_df = df[df["NOMBRE"].str.contains(nombre) == True]
    temp_df = temp_df[["NOMBRE", "MM-DD", "Nacimiento", "Edad", "FAMILIA.1"]]
    temp_df = temp_df.reset_index(drop=True)
    return temp_df

# imágenes:
globos = 'globos.jpg'
escudo = 'escudo.jpg'

# estructura de la app
st.title("Efemérides Familia Zambrano")
st.image(escudo, use_column_width = True)
st.header("Próximos Cumpleaños:")
AgGrid(pc)
st.image(globos, use_column_width = True)
st.header("Últimos Cumpleaños:")
AgGrid(uc)
st.header("Buscar Familiar:")
nombre = st.text_input("Buscar Familiar: ")
try:
    AgGrid(buscar_familiar(nombre))
except:
    test = 1 + 1

# -*- coding: utf-8 -*-
"""
Created on Tue May  2 22:02:19 2023

@author: Miguel_Perez_Diaz
"""

import pandas as pd


# ======= SUPER_A ===============


def eliminaComaYPunto(df):
    precios = df['precio']

    j = 0
    for precio in precios:

        df.loc[j, 'precio'] = int(
            precio.replace(",", "").replace(".", ""))/100

        j = j + 1

    return df

# conversion a entero df['Precio'].astype('Int64') 

# # === Comienzo de programa principal ===


archivos = ['superA_01.json', 'superA_02.json',
            'superA_03.json', 'superA_04.json', 'superA_05.json',
            'superA_06.json', 'superA_07.json', 'superA_08.json', 'superA_09.json']

flag = True
for archivo in archivos:
    if flag:
        df_merge = pd.read_json(archivo).dropna()
        flag = False
    else:
        df_aux = pd.read_json(archivo).dropna()
        df_merge = df_merge.merge(df_aux, how='outer')


# Alternativa utilizando .concat()
#for archivo in archivos:
#    if flag:
#        df_merge = pd.read_json(archivo).dropna()
#        flag = False
#    else:
#        df_aux = pd.read_json(archivo).dropna()
#        df_merge = pd.concat([df_merge,df_aux],ignore_index = True)




df = eliminaComaYPunto(df_merge)
df.columns = ['dia_hora_extraccion', 'descripcion', 'precio', 'categoria']

df.to_excel('resumenSuperA.xlsx', sheet_name="Demo", index=False)


# ***************************************************************************


# =========================== ATOMO =================================

# funcion que limpia el dato de precio y dato de categoria
def SeleccionaDigitosUtiles(df_atomo):

    precios = df_atomo['precio']

    i = 0
    for precio in precios:
        df_atomo.loc[i, 'precio'] = float(precio[-6:-3])
        i = i + 1

    categorias = df_atomo['categoria']

    k = 0
    for categoria in categorias:
        df_atomo.loc[k, 'categoria'] = categoria.partition("-")[-1]
        k = k + 1

    return df_atomo

# === Comienzo programa principal ===


archivos = ['atomo_01.json', 'atomo_02.json',
            'atomo_03.json', 'atomo_04.json', 'atomo_05.json',
            'atomo_06.json', 'atomo_07.json', 'atomo_08.json']

flag = True
for archivo in archivos:
    if flag:
        df_merge = pd.read_json(archivo).dropna()
        flag = False
    else:
        df_aux = pd.read_json(archivo).dropna()
        df_merge = df_merge.merge(df_aux, how='outer')

df_atomo = SeleccionaDigitosUtiles(df_merge)

df_atomo.to_excel('resumenAtomo.xlsx', sheet_name="Demo", index=False)


# ======================== SEGAL ======================


archivos = ['segal_01.json', 'segal_02.json',
            'segal_03.json', 'segal_04.json', 'segal_05.json',
            'segal_06.json', 'segal_07.json', 'segal_08.json', 'segal_09.json']

flag = True
for archivo in archivos:
    if flag:
        df_merge = pd.read_json(archivo).dropna()
        flag = False
    else:
        df_aux = pd.read_json(archivo).dropna()
        df_merge = df_merge.merge(df_aux, how='outer')

df_segal = eliminaComaYPunto(df_merge)
df_segal.to_excel('resumenSegal.xlsx', sheet_name="Demo", index=False)


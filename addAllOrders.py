#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import sys
import zipfile
import os
import requests
import re
import pandas as pd
import json
from df2gspread import df2gspread as d2g

nat_url = 'http://scn.naturacosmeticos.com.ar'
spreadsheet = '1R5LFCao9_DNH9CAldRi1whA0f4qvRTzLFnbuw0PACss'


with open("password.json",'r') as f:
    natura_pass = False
    natura_user = False
    
    datosUsuario = json.load(f)
    natura_user = datosUsuario["user"]
    natura_pass = datosUsuario["password"]


if natura_pass==False or natura_user==False:
    print("Error al parsear password.txt")
    exit()

s = requests.Session()
loginPayload = {
    "usuario":natura_user,
    "senha":natura_pass
}
data = {
  'code': natura_user,
  'pass': natura_pass,
  'return_url': ''
}
r1 = s.post('https://scn.naturacosmeticos.com.ar/Login_controller/validation', data=data)

params = (
    ('page', '1'),
    ('pageSize', '1'),  #trae solo el último item.
)
salida = s.get("https://scn.naturacosmeticos.com.ar/pedidos/ajax/orders/{}/0".format(natura_user),params=params).json()[0]
print(salida)
lastorder = salida['id']
cicloUltimaCompra = salida['cycle']

print("Última compra")
print(lastorder)
#Items pedido:

sg = s.get('https://scn.naturacosmeticos.com.ar/pedidos/items/{}/{}'.format(lastorder,lastorder))
tablaItems = pd.read_html(sg.text, attrs={'class': 'tabla-consultoria'})[0]

df = pd.DataFrame(tablaItems)
df.insert(1,"valorRev",[df["Código"][i] for i in df.index]) 
print(df)
#carga nuevo pedido en hoja de google spreadsheet
#TODO verificar que la hoja no exista para no sobreescribir.

#d2g.upload(df,spreadsheet,f"{cicloUltimaCompra}_{lastorder}")

r1.close()
s.close()

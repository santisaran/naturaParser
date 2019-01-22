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
from df2gspread import df2gspread as d2g

nat_url = 'http://scn.naturacosmeticos.com.ar'
spreadsheet = '1R5LFCao9_DNH9CAldRi1whA0f4qvRTzLFnbuw0PACss'


with open("password.txt",'r') as f:
	natura_pass = False
	natura_user = False
	while True:
		t = f.readline()
		if t!="":
			if t.startswith("usuario="):
				natura_user = t.split("=")[-1]
			elif t.startswith("pass="):
				natura_pass = t.split("=")[-1]
		else:
			break
	f.close()

if natura_pass==False or natura_user==False:
	print("Error al parsear password.txt")
	exit()

s = requests.Session()
loginPayload = {
	"usuario":natura_user,
	"senha":natura_pass
}
r1 = s.post("http://scn.naturacosmeticos.com.ar/index.php?option=com_geraweb&task=pessoa.loginAjax",params=loginPayload)
#f = open("salidanatLogin.html", 'w',encoding='utf8')
#f.write(r1.text)
#f.close()

sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/mis-pedidos")

tablaPedidos = pd.read_html(sg.text, attrs={'id': 'grid_pedido'})
codigoUltimaCompra = tablaPedidos[0]['Código'][0]
cicloUltimaCompra = tablaPedidos[0]['Ciclo'][0]

print("Última compra")
print(codigoUltimaCompra)
#Items pedido:
sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=itens_pedido&template=pedidos&&codpedido=%s"%codigoUltimaCompra)
tablaItems = pd.read_html(sg.text, attrs={'id': 'grid_itempedido'})[0]
df = pd.DataFrame(tablaItems)
df.insert(1,"valorRev",[df["Código"][i] for i in df.index]) 
print(df)
#carga nuevo pedido en hoja de google spreadsheet
#TODO verificar que la hoja no exista para no sobreescribir.
d2g.upload(df,spreadsheet,"%s"%cicloUltimaCompra)

#Hacer click en un pedido:
#sg = s.get("http://scn.naturacosmeticos.com.ar/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=pedido_abas&template=pedidos&codpedido=45107649")
#Tracking:
#sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=tracking_pedido&template=pedidos&&codpedido=45107649")

r1.close()
s.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import sys
import zipfile
import os
import requests
import re

nat_url = 'http://scn.naturacosmeticos.com.ar'

s = requests.Session()
loginPayload = {
	"usuario":"2552725",
	"senha":"P0ST1G0NA"
}
r1 = s.post("http://scn.naturacosmeticos.com.ar/index.php?option=com_geraweb&task=pessoa.loginAjax",params=loginPayload)
f = open("salidanatLogin.html", 'w',encoding='utf8')
f.write(r1.text)
f.close()

#sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/mis-pedidos")
#f = open("salidanat.html", 'w', encoding='utf8')
#f.write(sg.text)
#f.close()
#Items pedido:
sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=itens_pedido&template=pedidos&&codpedido=45107649")
#Hacer click en un pedido:
#sg = s.get("http://scn.naturacosmeticos.com.ar/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=pedido_abas&template=pedidos&codpedido=45107649")
#Tracking:
#sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=tracking_pedido&template=pedidos&&codpedido=45107649")

f = open("pedido.html", 'w', encoding='utf8')
f.write(sg.text)
f.close()

#Tracking:
#sg = s.get("http://scn.naturacosmeticos.com.ar/meu-negocio/index.php?option=com_geraweb&view=cnoconsultapedidos&layout=tracking_pedido&template=pedidos&&codpedido=45107649")

r1.close()
s.close()

# Codigo python
from fastapi import FastAPI, HTTPException # Importa propio  del framework FastAPI
from typing import List # Importa estandar de python para tipado
import asyncio # Importa estandar de python para asincronia

# CREACION DE LA APLICACION

app = FastAPI() # Objeto principal de la API (Intancia del framework)

#  BASE DE DATOS SIMULADA  

clientes = [] # Variable global tipo lista alamacenar clientes en memoria
contador_clientes = 0 # Variable global para contar clientes

# ENDOPINT RAIZ
@app.get("/") # Decroador propio de FastAPI para metodos GET 

# http exepcion ===> para crear una respuesta

def home(): # Funcion normal (no asincrona por simplicidad)
    return {"Mensaje": "API del Banco funcionando"}

"""
    - @app.get("/") -> Dwfine ruta
    - home() ---> funcion que reposnde
    Retorna JSON automaticamente
"""

# CREAR CLIENTE
@app.post("/clientes") # Decorador para metodo POST
async def crear_cliente(nombre: str): # Parametro recibido por query

    global contador_clientes # Indica que usaremos la variable global

    if nombre == "": # Validacion basica
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacio") # Lanza error HTTP
    
    await asyncio.sleep(3) # Simula retraso de 3 segundo
    
    cliente = {
        "id" : len(clientes) + 1, # Generacion simple de ID
        "nombre" : nombre
    }

    clientes.append(cliente) # Agrega cliente a lista global
    contador_clientes += 1 # Incrementa contador de clientes

    return cliente # Devuelve cliente creado


# LISTAR CLIENTES GET
@app.get("/clientes", response_model = List[dict]) # Define tipo de respuesta
def listar_clientes():
    #Validamos que exitan clientes
    if not clientes: # Si la lista esta vacia
        raise HTTPException(status_code=404, detail="No hay clientes registrados") # Lanza error HTTP
    return clientes # Devuelve lista completa

# OBTENER CLIENTE POR ID PASO 6
@app.get("/clientes/{cliente_id}") # Ruta con parametros dinamicos
def obtener_cliente(cliente_id : int): # tipo entero
    # Validacion basica del ID
    if not cliente_id: # Si no se proporciona ID
        raise HTTPException(status_code=400, detail="El ID es requerido") # Lanza error HTTP
    
    #Validamos que el ID sea positivo
    if cliente_id <= 0:
        raise HTTPException(status_code=400, detail="El ID debe ser un numero positivo") # Lanza error HTTP
    
    #Validamos que el ID no sea mayor al numero de clientes
    if cliente_id > len(clientes):
        raise HTTPException(status_code=404, detail="Cliente no encontrado") # Lanza error HTTP
    
    for cliente in clientes: # recorre lista
        if cliente["id"] == cliente_id:
            return cliente # retorna si encuentra
    
    return {"error" : "Cliente no encontrado"} # manejo basico de errores

# ELIMINAR CLIENTE PASO 7
@app.delete("/clientes/{cliente_id}") # Decorador para metodo DELETE
def eliminar_cliente(cliente_id : int):
    # Validacion que exita el id
    if not cliente_id: # Si no se proporciona ID
        raise HTTPException(status_code=400, detail="El ID es requerido") # Lanza error HTTP
    
    #Validamos que el ID sea positivo
    if cliente_id <= 0:
        raise HTTPException(status_code=400, detail="El ID debe ser un numero positivo") # Lanza error HTTP
    
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            clientes.remove(cliente) # Elimina cliente de la lista
            return {"mensaje" : "Cliente eliminado"}
    
    return {"error" : "Cliente no encontrado"} # manejo basico de errores

# ACTUALIZAR CLIENTE PASO 8
@app.put("/clientes/{cliente_id}") # Decorador para metodo PUT
def actualizar_cliente(cliente_id : int, nombre : str): # Recibe ID y nuevo nombre
    # Validacion que exita el id
    if not cliente_id: # Si no se proporciona ID
        raise HTTPException(status_code=400, detail="El ID es requerido") # Lanza error HTTP
    
    #Validamos que el ID sea positivo
    if cliente_id <= 0:
        raise HTTPException(status_code=400, detail="El ID debe ser un numero positivo") # Lanza error HTTP
    
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = nombre # Actualiza el nombre
            return cliente # Devuelve cliente actualizado
    
    return {"error" : "Cliente no encontrado"} # manejo basico de errores

# CONTADOR GLOBAL
@app.get("/contador")
def contador():
    return {"clientes_creados": contador_clientes}
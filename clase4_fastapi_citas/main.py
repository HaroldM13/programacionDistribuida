# Codigo python
from fastapi import FastAPI, HTTPException # Importa propio  del framework FastAPI
from typing import List # Importa estandar de python para tipado
import asyncio # Importa estandar de python para asincronia

# CREACION DE LA APLICACION

app = FastAPI() # Objeto principal de la API (Intancia del framework)

#  BASE DE DATOS SIMULADA  

citas = [] # Variable global tipo lista alamacenar citas en memoria

# ENDOPINT RAIZ
@app.get("/") # Decroador propio de FastAPI para metodos GET

# http exepcion ===> para crear una respuesta

def home(): # Funcion normal (no asincrona por simplicidad)
    return {"Mensaje": "API de citas con FastAPI"} # Retorna diccionario que se convierte en JSON automaticamente

# CREAR cita
@app.post("/citas") # Decorador para metodo POST
async def crear_cita(nombre_medico: str, nombre_paciente: str): # Parametro recibido por query

    if nombre_medico == "": # Validacion basica
        raise HTTPException(status_code=400, detail="El nombre del medico no puede estar vacio") # Lanza error HTTP
    
    if nombre_paciente == "": # Validacion basica
        raise HTTPException(status_code=400, detail="El nombre del paciente no puede estar vacio") # Lanza error HTTP
    
    await asyncio.sleep(2) # Simula retraso de 2 segundo
    
    cita = {
        "id" : len(citas) + 1, # Generacion simple de ID
        "medico" : nombre_medico, # Asigna nombre del medico
        "paciente" : nombre_paciente, #Nombre de paciente
        "estado" : "activa" # Estado inicial de la cita

    }

    citas.append(cita) # Agrega cita a lista global

    return cita # Devuelve cita creado

# LISTAR citaS GET
@app.get("/citas", response_model = List[dict]) # Define tipo de respuesta
def listar_citas():
    #Validamos que exitan citas
    if not citas: # Si la lista esta vacia
        raise HTTPException(status_code=404, detail="No hay citas registrados") # Lanza error HTTP
    return citas # Devuelve lista completa

# OBTENER cita POR nombre de cliente PASO 6
@app.get("/citas/{nombre_paciente}", response_model = List[dict]) # Ruta con parametros dinamicos
def obtener_cita(nombre_paciente : str): # tipo entero
    # Validacion basica del nombre de cliente
    if not nombre_paciente: # Si no se proporciona nombre de cliente
        raise HTTPException(status_code=400, detail="El nombre de cliente es requerido") # Lanza error HTTP
    
    #Validamos que el nombre de cliente sea positivo
    if nombre_paciente == "": # Si el nombre de cliente esta vacio
        raise HTTPException(status_code=400, detail="El nombre de cliente no puede estar vacio") # Lanza error HTTP
    
    #Validamos que el nombre de cliente no sea mayor al numero de citas
    if nombre_paciente > len(citas):
        raise HTTPException(status_code=404, detail="cita no encontrado") # Lanza error HTTP
    
    response = [cita for cita in citas if cita["paciente"] == nombre_paciente] # Busca citas por nombre de cliente

    # Validacion que se encontraron citas
    if len(response) == 0: # Si no se encontraron citas
        raise HTTPException(status_code=404, detail="cita no encontrado") # Lanza error HTTP
    
    return response # Devuelve lista de citas encontradas

# CANCELAR cita PASO 7
@app.put("/citas/{cita_id}") # Decorador para metodo PUT
def cancelar_cita(cita_id : int):
    # Validacion que exita el id
    if not cita_id: # Si no se proporciona ID
        raise HTTPException(status_code=400, detail="El ID es requerido") # Lanza error HTTP
    
    #Validamos que el ID sea positivo
    if cita_id <= 0:
        raise HTTPException(status_code=400, detail="El ID debe ser un numero positivo") # Lanza error HTTP
    
    for cita in citas:
        if cita["id"] == cita_id and cita["estado"] != "cancelada": # Si se encuentra la cita y no esta cancelada
            cita["estado"] = "cancelada" # Cambia el estado de la cita a cancelada
            return {"mensaje" : "cita cancelada exitosamente"} # Devuelve mensaje de exito
    
    return {"error" : "cita no encontrado"} # manejo basico de errores

# ACTUALIZAR cita PASO 8
@app.put("/citas/{cita_id}") # Decorador para metodo PUT
def actualizar_cita(cita_id : int, nombre_paciente : str, nombre_medico : str): # Recibe ID y nuevo nombre_paciente
    # Validacion que exita el id
    if not cita_id: # Si no se proporciona ID
        raise HTTPException(status_code=400, detail="El ID es requerido") # Lanza error HTTP
    
    #Validamos que el ID sea positivo
    if cita_id <= 0:
        raise HTTPException(status_code=400, detail="El ID debe ser un numero positivo") # Lanza error HTTP
    
    for cita in citas:  
        if cita["id"] == cita_id:
            cita["medico"] = nombre_medico # Actualiza el nombre_medico
            cita["paciente"] = nombre_paciente # Actualiza el nombre_paciente
            return cita # Devuelve cita actualizado
    
    return {"error" : "cita no encontrado"} # manejo basico de errores
import asyncio

contador_clientes = 0

lock = asyncio.Lock()

# Funcion que maneja cada cliente (coroutine)
async def handle_client(reader, writer):
    global contador_clientes

    # Espera datos del cliente (maximo 1024 bytes)
    data = await reader.read(1024)

    # Convierte los bytes recibidos en texto
    name = data.decode()

    await asyncio.sleep(5)

    async with lock:
        contador_clientes += 1
        numero_cliente = contador_clientes

    # Construye el mensaje personalizado con el numero de cliente
    response = f"Hola {name}, eres el cliente numero {numero_cliente}"

    print(f"[Servidor] Atendiendo a {name} → cliente #{numero_cliente}")

    # Envia la respuesta al cliente (en bytes)
    writer.write(response.encode())

    # Espera a que los datos se envien completamente
    await writer.drain()

    # Cierra la conexion con el cliente
    writer.close()

# Funcion principal del servidor
async def main():
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 5000
    )

    print("[Servidor] Banco en linea. Esperando clientes en puerto 5000...")

    # Mantiene el servidor activo
    async with server:
        # El servidor queda escuchando indefinidamente
        await server.serve_forever()

# Ejecuta el event loop principal
asyncio.run(main())

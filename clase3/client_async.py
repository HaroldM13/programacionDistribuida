import asyncio  # Libreria para programacion asincrona
import time      # Libreria para medir tiempo

async def main():
    # Abre conexion con el servidor
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 5000
    )

    # Solicita el nombre al usuario
    name = input("Ingresa tu nombre: ")

    start_time = time.time()

    # Envia el nombre al servidor
    writer.write(name.encode())

    # Asegura que el mensaje se envie completamente
    await writer.drain()

    # Espera respuesta del servidor
    data = await reader.read(1024)

    end_time = time.time()

    # Muestra la respuesta del servidor
    print(data.decode())

    # Calcula e imprime el tiempo total de atencion
    tiempo_total = round(end_time - start_time, 2)
    print(f"Tiempo de atencion: {tiempo_total} segundos")

    # Cierra la conexion
    writer.close()
    await writer.wait_closed()

# Ejecuta el cliente
asyncio.run(main())

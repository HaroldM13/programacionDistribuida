Preguntas: 
• ¿Es seguro usar variable global? 
Respuesta: No, porque se manejan varias peticiones al mismo tiempo es probable que una petición modifique la variable mientras la esta usando otra petición distinta

• ¿Dónde aparece el recurso compartido? 
Respuesta: La lista y el contador de clientes ya que varios edpoints lo usan y lo pueden leer o modificar

• ¿Se debería usar lock en producción?
Respuesta: Claro que si, esto permite bloquar de cierta forma las peticiones despues que una este en euso y s forma una "Cola de peticiones" que deben esperar que termine de ejecutar la que esta en ejecucion
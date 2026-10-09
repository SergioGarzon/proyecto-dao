# Biblioteca: Sistema de Préstamos Interbibliotecarios 

### Contexto  
---
Unareddebibliotecas públicas administra cientos de socios y un amplio catálogo de libros y otros materiales de consulta. Actualmente muchas tareas se realizan en forma manual, lo que dificulta el control de préstamos, devoluciones y disponibilidad de ejemplares.  
Se requiere un sistema que administre las operaciones habituales de la biblioteca, administre las sedes que conforman la red y facilite la consulta de información tanto al personal como alos usuarios, incluyendo el envío de ejemplares entre las distintas sedes de la red. 

### Procesosdenegocio obligatorios   
---
1. Administrar las sedes de la red (dirección, datos de contacto, horarios y estado activo/baja). 
2. Administrar socios. 
3. Administrarcatálogodelibrosyejemplaresfísicos,indicandolasedealaquepertenece cada ejemplar. 
4. Registrar solicitudes de préstamo local e interbibliotecario (indicando sede origen y sede destino). 
5. Empaquetar, despachar y recibir ejemplares, asignando un remito y permitiendo la trazabilidad del mismo a lo largo del trayecto (estados). 
6. Consultar disponibilidad. 
7. Gestionar reservas. 
8. Registrar devoluciones y el estado físico del material devuelto. 
 
### Procesosdenegocio opcionales  
---
* Envío de notificaciones. 
* Gestionar historial de lecturas. 
* Recomendaciones. 
* Inventario con códigos. 
* Revisión de estado de recepción de ejemplares (extravío, daño, destrucción). 
  
### Validaciones de negocio  
---
* Noprestar ejemplares no disponibles. 
* Noprestar material a socios inhabilitados. 
* Controlar fechas de vencimiento de préstamos. 
* Mantener trazabilidad del remito en todo el trayecto. Evitar duplicados (socios, catálogo, ejemplares). 
* Noprestar ejemplares que no pertenezcan a la sede de origen del préstamo. 
* Noiniciar préstamos, reservas ni envíos hacia o desde una sede dada de baja. 
  
### Reportessugeridos  
---
* Préstamos activos y material en tránsito. 
* Préstamos vencidos y multas acumuladas. 
* Libros más solicitados para préstamos inter-sedes. 
* Disponibilidad de catálogo por sede. 
* Tasa de envíos logísticos exitosos e incidencias. 
* Movimiento de ejemplares entre sedes: envíos por sede origen/destino y tiempo promedio de tránsito. 

### Consideraciones particulares  
---
El equipo deberá investigar el dominio de bibliotecas y definir las entidades, atributos y reglas de negocio necesarias.  
El ciclo de vida del remito y sus estados será evaluado críticamente en el modelo. De forma obligatoria, el grupo debe aplicar **al menos dos patrones de diseño** y debe implementar **al menos cuatro reportes no triviales**, además de cumplir con todos los procesos obligatorios y las validaciones descriptas en esta consigna.
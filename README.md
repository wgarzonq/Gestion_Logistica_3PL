# Gestión Logística 3PL
Proyecto de software para los procesos de gestión logística de terceros; facilitando la distribución de medicamentos.
## Autor: William David Garzón Quevedo (100223601)
## Institución: Universidad Corporación Universitaria Iberoamericana
## Programa: Ingeniería de Software
## Curso: Proyecto de Software

## Objetivo General

Desarrollar y validar un producto mínimo viable sobre la logística de terceros para la dispensación de medicamentos de forma oportuna que centralice la información operacional, permitiendo controlar los procesos prioritarios del movimiento y alistamiento de las mercancías, facilitando la consulta y la trazabilidad transparente.

## Objetivos Específicos 

-	Identificar los requerimientos funcionales y no funcionales de los procesos logísticos seleccionados.
-	Diseñar la arquitectura de software, el modelo de datos y las interfaces necesarias para la gestión centralizada de la información.
-	Implementar tanto los módulos de autenticación de los usuarios como los módulos para los procesos de recepción a la bodega, movimientos, pedidos, alistamientos y despachos de las mercancías.
-	Permitir que se importen procesos anteriores realizados mediante Excel, organizando la información para que sea compatible con la estructura del sistema.
-	Evaluar el funcionamiento del producto mediante pruebas de funcionalidad, seguridad básica, integridad de datos y rendimiento.

## Diagrama de Desglose EDT

<img width="1024" height="768" alt="Image" src="https://github.com/user-attachments/assets/09d39562-4671-445c-8dcd-f662d5f40290" />

## Alcance

El proyecto contempla el análisis, diseño, desarrollo y validación de un producto mínimo viable para la gestión de procesos logísticos de terceros, hacia la distribución de los productos fármacos tanto de necesidad vital como no vital. Permitiendo administrar los productos, controlar el inventario y seguir los pedidos realizados; para el cumplimiento oportuno de las entregas hacia los consumidores.

El sistema incluirá la autenticación de los usuarios, control de acceso según sus roles, trazabilidad de las operaciones e importación controlada de la información trabajada previamente mediante archivos con extensión CSV de Excel, siempre que se cumpla la estructura definida predispuesta por el desarrollable.

### Elementos Fuera del Alcance

Para el producto mínimo viable a desarrollar, solo se buscará que se cumpla los procesos logísticos de terceros básicos, por ello no se contempla el entrenamiento de modelos de Machine Learning y la integración con múltiples ERP.

### Restricciones

-	Tiempo: el desarrollo estará limitado por un periodo de tiempo mayor a 2 meses con trabajo intensivo, desde finales de septiembre del 2026 hasta los comienzos de diciembre del 2026.
-	Recursos: se utilizarán los recursos humanos, técnicos y económicos disponibles para el equipo de desarrollo.
-	Infraestructura: la disponibilidad del sistema dependerá de la configuración y continuidad de los servicios externos utilizados.
-	Funcionalidad: el producto mínimo viable cubrirá únicamente los procesos definidos como prioritarios.

### Criterios de Aceptación

 El producto mínimo viable será aceptado cuando se demuestre, mediante pruebas documentadas, que:
-	Los usuarios pueden iniciar sesión y acceder únicamente a las funciones autorizadas para su rol.
-	Los productos pueden registrarse, consultarse y modificarse correctamente.
-	Los movimientos de inventario quedan registrados para su posterior consulta.
-	Las recepciones, despachos y el alistamiento de los pedidos puedan registrarse cambiando de estado según las reglas definidas.
-	La importación de archivos CSV cargue según lo esperado, informándole al usuario que datos cumplen con la estructura del sistema y cuáles no.
-	Los reportes presentan información consistente con los registros almacenados.
-	Las pruebas funcionales definidas para la versión inicial se ejecuten satisfactoriamente y sus resultados queden documentados.

## Cronograma

El equipo de desarrollo estará conformado por:
-	1 desarrollador Front-End: Desarrolla e implementa las interfaces gráficas con las que interactúa el usuario.
-	1 desarrollador Back-End: Encargado de desarrollar la lógica de negocio del lado del servidor, implementar los servicios y las API y gestionar la comunicación entre las interfaces del usuario y la base de datos.
-	1 analista de datos: Estudia los requerimientos del cliente y del negocio para diseñar una estructura de datos coherente, organizada y eficiente.
-	1 diseñador UX/ UI: Diseña la experiencia de usuario y la interfaz de usuario, teniendo en cuenta las necesidades, las expectativas y la comodidad de las personas que utilizarán el aplicativo.
Se define el equipo de desarrollo, porque en la realización del cronograma tanto las fases de trabajo como las actividades, están establecidas mediante la jerarquía presentada en el diagrama de desglose EDT, por ende, cada actividad debe tener una persona responsable en su llevada a cabo y la culminación.

<img width="1062" height="333" alt="image" src="https://github.com/user-attachments/assets/0b8c33c8-1360-4a0f-9c77-2fb8607f31c5" />
<img width="1058" height="338" alt="image" src="https://github.com/user-attachments/assets/1076b690-86e2-44fc-94bd-26b9e5788099" />
<img width="1053" height="330" alt="image" src="https://github.com/user-attachments/assets/0e04c56a-8bf3-463f-aa78-cb46b73f0bec" />
<img width="1055" height="331" alt="image" src="https://github.com/user-attachments/assets/0b5f0943-4484-41b9-9ee5-7a1555ddefc6" />
<img width="1060" height="398" alt="image" src="https://github.com/user-attachments/assets/dfb9d07c-6fd3-43c5-be1c-8866e86cfb1b" />
<img width="1060" height="400" alt="image" src="https://github.com/user-attachments/assets/4c62673e-ff39-4944-af04-79fd68560f10" />
<img width="1058" height="694" alt="image" src="https://github.com/user-attachments/assets/87ab9d89-4b31-4e40-878f-970b7f5a9110" />









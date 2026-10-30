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

## Requerimientos Funcionales
### RF-01: Gestión de Usuarios
Los usuarios pueden registrarse, iniciar sesión, cerrar sesión, consultar y editar sus datos personales.

### RF-02: Gestión de Empresas
El representante o el primer usuario registrado relacionado a una empresa, será el encargado de registrarla y editarla.

### RF-03: Solicitud de Vinculación Empresarial
Los usuarios registrados que no representen a una empresa en el aplicativo, pueden enviar una solicitud de vinculación hacia la compañía correspondiente.

### RF-04: Gestión de Colaboradores
El representante de la empresa podrá aprobar o rechazar las solicitudes de vinculación, de igual forma podrá desvincular a los colaboradores de su compañía.

### RF-05: Gestión de Procesos Logísticos
Todos los usuarios tendrán acceso a la totalidad de los procesos logísticos relacionados a una empresa vinculada, permitiendo: registrar, consultar, filtrar y editar.

### RF-06: Recuperación de Contraseña
El usuario podrá reestablecer su contraseña mediante el correo electrónico asociado al aplicativo.

### RF-07: Visualización de Gráficos Estadísticos
Por cada proceso logístico se debe generar una variada gama de gráficos estadísticos, utilizando la información almacenada.

### RF-08: Ampliación y Exportación de Gráficos
El usuario podrá ampliar los gráficos relacionados a los procesos logísticos y exportarlos en formato PDF para su descarga.

### RF-09: Importación de Datos
El usuario puede importar los registros relacionados a los procesos logísticos mediante un archivo Excel con extensión CSV, teniendo en cuenta que su estructura sea compatible con la estructura definida en el sistema.

### RF-10: Administración de Usuarios
Los administradores del aplicativo gestionan las cuentas de usuario mediante su activación, desactivación y modificación de roles.

### RF-11: Vinculación Entre Registros
Los registros relacionados entre procesos logísticos como, por ejemplo: la vinculación de producto a un pedido, se seleccionarán de forma clara e intuitiva.

### RF-12: Trazabilidad de los Registros
Cada registro de un proceso logístico debe estar asociado con el usuario que lo creo. 

### RF-13: Información Adicional en los Procesos Logísticos
Los formularios relacionados a los procesos logísticos tanto en su registro como en su edición, cuentan con la opción de agregar información complementaria aparte de los campos definidos.

## Requerimientos no Funcionales
### RNF-01: Confidencialidad
La información de los procesos logísticos relacionada a cada una de las empresas, solo debe ser manipulada y visualizada, por el representante y los colaboradores vinculados.

### RNF-02: Protección de los Datos Personales
La visualización de los datos de los usuarios es limitada, solo suministrando la información necesaria para la gestión de los procesos logísticos, la vinculación empresarial y la administración de las cuentas registradas.

### RNF-03: Disponibilidad
El sistema debe estar disponible cuando los usuarios de las diferentes empresas realicen las operaciones logísticas de manera simultánea y aislada.

### RNF-04: Tiempo de Respuesta
Las transiciones entre pantallas se completarán en un tiempo máximo de dos segundos, bajo las condiciones normales de operación con una conexión de red estable.

### RNF-05: Facilidad de Navegación
La interfaz gráfica presentará menús, paneles y enlaces de navegación; claramente identificables, permitiendo a los usuarios el acceso de forma intuitiva a los diferentes módulos del aplicativo.

### RNF-06: Eficiencia de Interacción
La manipulación del usuario hacia las operaciones frecuentes del aplicativo, se realizará con una cantidad reducida de pasos de interacción.

### RNF-07: Gestión de Errores
Mediante mensajes claros se notificará al usuario cuando se presenten fallos en los servicios principales o externos que afecten el funcionamiento del sistema.

### RNF-08: Compatibilidad
El aplicativo debe funcionar correctamente en los dispositivos definidos como compatibles.

### RNF-09: Recuperación Ante Fallos
Habrá mecanismos de respaldo y recuperación que permitan reestablecer la información ante incidentes.

### RNF-10: Integridad de la Información
Las operaciones de registro y edición garantizarán que se mantenga la consistencia de los datos.

### RNF-11: Mantenibilidad
La aplicación se organizará en componentes que faciliten la corrección de errores y la incorporación de futuros incrementos.

## Alcance
### Objetivo del Prototipo
El prototipo tiene como objetivo desarrollar una representación visual de un sistema que permita centralizar los procesos de la gestión logística de terceros, orientada a la mejor distribución de los medicamentos hacia los sitios de dispensación; con el propósito que se puedan cumplir los procesos de forma ágil, sincrónica, con una trazabilidad transparente y de fácil curva de aprendizaje para los usuarios.

### Usuarios
-	Administradores: gestionan las cuentas de usuario, modifican los roles dentro del aplicativo, asigna el representante de una empresa ya registrada; en caso que el representante anterior sea desvinculado de la misma.
-	Representante de una empresa: gestiona a los colaboradores vinculados, revisa las solicitudes de los nuevos colaboradores, registra; consulta y edita los procesos logísticos vinculados a su organización.
-	Colaboradores: solicita la vinculación hacia una empresa, registra; consulta y edita los procesos logísticos vinculados a su organización.

### Funcionalidades Incluidas
-	Pantalla de inicio.
-	Formulario de inicio de sesión del usuario.
-	Formulario de registro del usuario.
-	Formulario de edición del usuario.
-	Formulario para solicitar la vinculación hacia una empresa.
-	Formulario de registro de una empresa.
-	Formulario de edición de una empresa.
-	Formulario de restablecimiento de la contraseña.
-	Panel para gestionar a los colaboradores vinculados a una empresa.
-	Desvinculación de los colaboradores asociados a una empresa.
-	Aceptación y descarte de las solicitudes de vinculación a una empresa.
-	Panel para la administración de las cuentas de usuario.
-	Habilitación, suspensión y cambio de rol de las cuentas de usuario.
-	Paneles de los procesos logísticos: productos, conductores, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.
-	Visualizaciones de los procesos logísticos: productos, conductores, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.
-	Formularios de registro de los procesos logísticos: productos, conductores, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.
-	Formularios de edición de los procesos logísticos: productos, conductores, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.
-	Visualización de los gráficos estadísticos relacionados a los procesos logísticos: productos, pedidos, recepciones, inventarios, cross-docking, alistamientos y despachos.
-	Visualización ampliada y exportación de los gráficos estadísticos.
-	Visualización de la importación de los registros hechos en archivos Excel con formato CSV de los procesos logísticos: productos, conductores, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.
-	Paneles de la organización de la información importada de los procesos logísticos.
-	Eliminación única de un registro importado.
-	Subida de los registros importados de acuerdo a la estructura planteada por el aplicativo.
-	Desplegable mediante el icono de avatar del usuario con las opciones de navegación: editar perfil, empresas, usuarios y cerrar sesión.
-	Barra deslizable con las opciones de navegación a los paneles de: colaboradores, conductores, productos, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.

### Funcionalidades Excluidas
-	Comunicación con la base de datos.
-	Importación de la información contenida en archivos Excel con extensión CSV.
-	Relleno de los formularios con las entradas de caracteres por parte del usuario.
-	Conexión de las cuentas de usuario con los correos electrónicos asociados.
-	Uso simultaneo del prototipo entre varios usuarios vinculados a diferentes empresas.
-	Separación de las funcionalidades del aplicativo dependiendo los roles de usuario.
-	Exportación de los gráficos estadísticos mediante un archivo PDF.
-	Funcionamiento del consumo de servicios por parte del servidor.
-	Despliegue del aplicativo o sus componentes a servicios en la nube.
-	Filtrado y búsqueda de los registros.
-	Agregado de los campos complementarios en los formularios de los procesos logísticos.

### Entregables
-	Diseño de las pantallas principales.
-	Prototipo navegable.
-	Paso a paso de las operaciones que se realizaran en el aplicativo.
-	Uso de datos ficticios.
-	Visualización completa de los componentes del sistema.
-	Funcionalidades parciales de algunos de los campos críticos para relacionar los registros entre los procesos logísticos.
-	Documentación sobre el recorrido de la conexión entre las pantallas para la validación por parte del usuario.

### Recorrido del Prototipo
1.	Presentación de la pantalla de inicio, direccionando hacia las pantallas del registro de las cuentas de usuario e inicio de sesión.
2.	Demostrar como el usuario recién registrado puede solicitar la vinculación hacia una empresa ya registrada en el aplicativo o registrar la empresa para vincular otros colaboradores.
3.	Descripción de los paneles de los procesos logísticos: productos, conductores, pedidos, recepciones, inventarios, cross-dockings, alistamientos y despachos.
4.	Explicar los procesos de consigna y edición de los procesos logísticos, destacando como se relacionan algunos.
5.	Detallar el paso a paso de la importación de los registros hechos mediante Excel y como se manejarla limpieza de los mismos, para que su estructura sea acorde a la estructura exigida por el sistema.
6.	Identificar los componentes relacionados a la navegación entre pantallas, buscando minimizar los tiempos de desplazamiento.
7.	Evidenciar como los representantes de las organizaciones gestionan a sus colaboradores, la información de la empresa y revisan las solicitudes de colaboraciones hechas por los usuarios recién registrados en el aplicativo.
8.	Establecer el papel que juegan los administradores del sistema sobre la gestión de las cuentas de usuario.

### Criterios de Aceptación
El prototipo se considerará satisfactorio cuando:
-	El usuario pueda recorrer las pantallas sin errores en la navegación.
-	Se entiendan los pasos para completar los formularios, tanto en los registros como en las ediciones.
-	La mayoría de los botones deben representar a una funcionalidad dentro del sistema.
-	Simule las operaciones que realiza el administrador en la gestión de las cuentas de usuario.
-	Los usuarios puedan comprender las tareas definidas proporcionando una retroalimentación.
-	El 80% del prototipo debe ser apto para su interpretación mediante código.
-	Los roles de los usuarios se establezcan desde el registro inicial.

### Limitaciones
El prototipo tendrá fines demostrativos y de validación. La información presentada es ficticia con el propósito de representar la funcionalidad de los componentes y la comunicación entre ellos, por ende, no se permite la realización de las gestiones de las cuentas de usuario, los procesos logísticos, la interpretación de los gráficos estadísticos y la importación de registros mediante archivos Excel de forma real, ni se considera como un sistema de gestión logística de terceros en funcionamiento.

### Resultado Esperado
Se espera validar que el producto de software a construir, los procesos logísticos de terceros sean centralizados, con una trazabilidad detallada donde se informe las novedades que ocurren sobre cada proceso y para los usuarios que manipulen el sistema; el aplicativo tenga una curva de aprendizaje sencilla, teniendo en cuenta que los procesos logísticos son acciones que entre más agilidad se tenga en los registros mejor es el servicio que se les brinda a los clientes. Se espera obtener una retroalimentación para definir la interpretación del prototipo mediante código.

## Vistazo del Prototipo
<img width="401" height="412" alt="Image" src="https://github.com/user-attachments/assets/9065e778-2cbe-4e6b-8d2e-a5fdc3e1e6c0" />
<img width="505" height="325" alt="Image" src="https://github.com/user-attachments/assets/9d469cab-5e16-4756-b1a9-3277ab61be89" />
<img width="700" height="301" alt="Image" src="https://github.com/user-attachments/assets/8597a750-169c-4305-9e91-3f282d8026a1" />
<img width="1033" height="691" alt="Image" src="https://github.com/user-attachments/assets/37bc85bf-db8a-414b-8317-a84696a4396d" />
<img width="1042" height="688" alt="Image" src="https://github.com/user-attachments/assets/4cb0af46-71ba-4dbe-8749-d4a737b73e67" />
<img width="1036" height="589" alt="Image" src="https://github.com/user-attachments/assets/a88fcdeb-7168-44e1-ae06-6dfad3c50ca2" />
<img width="1041" height="694" alt="image" src="https://github.com/user-attachments/assets/e83bf411-0f96-46ad-85c0-b851a446d3fb" />
<img width="1039" height="692" alt="image" src="https://github.com/user-attachments/assets/94628572-1836-41d7-9fc4-aaf8c6776b08" />
<img width="1036" height="694" alt="image" src="https://github.com/user-attachments/assets/0a7199ae-a228-44e0-898e-10a38140096f" />

## Instalación del Avance
El usuario para querer ensayar los servicios de la api, debe contar con la versión de Python 3.11.2, no se usa la versión 3.12 porque la librería REST Framework presenta fallas de punto nulo. Teniendo instalada la versión de Python indicada, se crea una carpeta donde se almacenará el proyecto Django en el dispositivo; abriendo la consola se crea y se activa un entorno virtual para instalar las librerías necesarias mediante el gestor de paquetes PIP.

python311 -m venv venv
.\venv\scripts\activate

Activado del entorno virtual se actualiza el gestor de paquetes PIP.

python311 -m pip install --upgrade pip

Con los pasos anteriores realizados se instala el archivo requirements.txt, conteniendo las librerías que fueron usadas para la construcción del proyecto de api rest consumible y para ejecutar el proyecto solo se usa el comando run server.

pip install -r requirements.txt

python manage.py runserver

En la herramienta para ensayar los métodos HTTP, al subir el primer registro mediante la api va creándose tanto la base de datos como la colección en el gestor de almacenamiento.








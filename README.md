# Portal Prácticas de Ciclos - Guía de uso de la aplicación

A continuación se incluyen las instrucciones básicas para acceder a la aplicación web, así como realizar las principales operaciones que se encuentran habilitadas en el entorno de producción. El objetivo es ofrecer a los usuarios una visión clara del funcionamiento de la herramienta y de las posibilidades disponibles.


## Acceso a la página web

La aplicación está disponible públicamente en la siguiente dirección:

https://tfm-anmarlea-upv-15.appspot.com/

Al acceder a la página por primera vez, se mostrará la vista inicial con el formulario de inicio de sesión:

<img width="1710" height="979" alt="Screenshot 2025-09-08 at 19 15 42" src="https://github.com/user-attachments/assets/5a2e3f83-8cf5-4f90-94c5-fba74c9cad9c" />


## Inicio de sesión

Para acceder a las funcionalidades internas es obligatorio iniciar sesión con unas credenciales predefinidas. A efectos de prueba, se han preparado los siguientes datos:

- email: coordinador@gmail.com
- contraseña: 1234

Una vez introducidos estos valores, el usuario será redirigido a la ventana de inicio, lugar donde tendrá acceso al resto de vistas disponibles.


## Navegación entre las diferentes páginas

El sistema está dividido en diferentes vistas o secciones, las cuales son accesibles mediante el uso de la barra de navegación, situada debajo del encabezado de "Portal Prácticas de Ciclos".

<img width="1172" height="47" alt="Screenshot 2025-09-08 at 19 16 44" src="https://github.com/user-attachments/assets/7d593308-8601-49d4-845f-3993788eddb3" />

Desde este menú es posible desplazarse entre las páginas dedicadas a estudiantes, tutores, empresas y asignaciones. Cada página muestra una tabla de las entidades actuales junto con las acciones que tienen disponibles.


## Modificación de entidades

Se ha habilitado la posibilidad de editar las entidades actuales, pudiendo cambiar temporalmente valores de las entidades. Sin embargo, con el fin de preservar la integridad de la base de datos, el _endpoint_ encargado de guardar los cambios está deshabilitado.

Esto implica que las modificaciones serán visibles únicamente en la sesión actual, pero se perderán al recargar la página o las listas de entidades. El propósito de esta limitación es permitir a los usuarios explorar la interfaz sin riesgo de alterar los datos originales.


## Creación de nuevas entidades mediante archivos CSV

La creación de nuevas entidades sí está disponible a través de la opción de subida de archivos CSV. Para ello, el usuario debe preparar un archivo siguiendo el formato del ejemplo proporcionado en la interfaz.

Algunos de los campos están limitados a valores existentes en la base de datos, motivo por el que a continuación se adjuntan ejemplos de valores válidos:

- _degree_/_degrees_: PRG, SEC, ALG, RED
- _field_: Programacion, Ciberseguridad, Algoritmia, Redes

Por último, se ruega a los usuarios que introduzcan datos ficticios respetuosos y adecuados, dado que la aplicación está disponible públicamente y las entidades creadas podrán ser vistas por el resto de personas que accedan.

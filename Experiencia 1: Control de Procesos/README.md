# Interfaz Gráfica

Módulo de la Interfaz gráfica del laboratorio

### Prerrequisitos

La tarea fue implementada usando un ambiente virtual en Python3.6, por lo que se recomienda fuertemente hacer lo mismo.

A continuación proveeré unos links para su instalación y uso:

[Instalación y uso en Ubuntu](https://www.digitalocean.com/community/tutorials/como-instalar-python-3-y-configurar-un-entorno-de-programacion-en-ubuntu-18-04-guia-de-inicio-rapido-es)

[Instalación y uso en Mac](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)

[Instalación y uso en Windows](https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/)

Luego de tener el ambiente virtual, es necesario ingresar a el para los pasos que vienen.

Crear un ambiente virtual de python ejecutando

```
virtualenv -p python3.6 venv
```

Luego ingresar a este con el comando:

```
. venv/bin/activate
```

Finalmente instalar las dependencias con:

```
pip install -r requirements.txt
```

## Corriendo la interfaz

Ubicarse en el directorio donde se ubica la carpeta ```OPC-QuadrupleTank```

Luego ejecutar:

```
bokeh serve --show OPC-QuadrupleTank
```

Y debería abrirse una ventana en el navegador con la interfaz


## Autores

* **Rodrigo Nazar** - *Front Developer* - [RodrigoNazar](https://github.com/RodrigoNazar)
* **Milena Gonzalez** - *Research and Developer* - [Milena2021](https://github.com/Milena2021)
* **Mathias Lambert** - *Back Developer* - [mglambert](https://github.com/mglambert)

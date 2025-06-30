# Proyecto 8: Generador de manifiestos de Kubernetes parametrizado

Este proyecto construye una herramienta que genere manifiestos de Kubernetes de forma dinámica y parametrizada, similar a un templating engine simplificado, utilizando Python.

## Estructura base del proyecto

Esctructura inicial del proyecto:

```
Generador-de-manifiestos-de-Kubernetes-parametrizado/
│
├── hooks/
│   ├── commit-msg
│   └── pre-push
│
├── src/
│   └── __init__.py
│
├── templates/
│   └── example.yaml.template
│
├── tests/
│   └── __init__.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── setup.sh
```

Se crearon 2 hooks iniciales:

- **commit-msg:** valida el formato de los commits
- **pre-push:** evita push directo a main, protege la rama main

Y un bash script `setup.sh` para inicializar el proyecto, este script instalara las librerias de requeriments,txt e instalara los hooks en el local de cada desarrollador, listo para el desarrollo del proyecto

## Git Flow

Seguimos las politicas de Git Flow lo que nos permitio seguir un flujo de trabajo estructurado para separar los procesos de desarrollo y asi mantener un historial más legible y reversible.

   <div align="center">
      <img src="https://i.postimg.cc/x1qspHYj/image.png" alt="image" width="700" />
   </div>

## Requisitos
- Python 3.10+
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
- [Helm](https://helm.sh/es/docs/intro/install/)

## Instalacion del Proyecto

Para instalar o inicializar el proyecto hay que seguir los siguientes pasos

- Clonar repositorio

```bash
$ git clone https://github.com/Ox-Chema-xO/Generador-de-manifiestos-de-Kubernetes-parametrizado.git
$ cd Generador-de-manifiestos-de-Kubernetes-parametrizado
```

- Crear entorno virtual

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate 
```

- Instalacion de dependencias y hooks

```bash
$ chmod +x setup.sh 
$ ./setup.sh
```

- Iniciar cluster Kubernetes local

```bash
$ minikube start
```

## Sprint 1

### Estructura del proyecto

```
Generador-de-manifiestos-de-Kubernetes-parametrizado/
│
├── hooks/
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
│
├── src/
│   ├── __init__.py
│   └── manifest_generator.py
│
├── templates/
│   ├── deployment.yaml.template
│   ├── service.yaml.template
│   └── values.yaml
│
├── tests/
│   └── __init__.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── setup.sh
```

### Modulos

#### hooks/

Se agrego un nuevo hook:

- **pre-commit**: Valida la sintaxis YAML de los archivos de plantilla y del  archivo de valores de configuracion values.yaml

#### src/

Se desarrolla un script Python:

- **manifest_generator.py**: Este script lee una plantilla de manifiesto y el archivo de valores de configuracion `values.yaml` en templates/. Reemplaza los placeholders en la plantilla con los valores correspondientes y finalmente genera el manifiesto final de Kubernetes

#### templates/

Se crearon 2 templates y 1 archivo de valores de configuracion:

- **deployment.yaml.template**: Define un template con placeholders para el Deployment de forma basica agregando parametros como app_name, replicas, image y container_port
- **service.yaml.template**: Define un template con placeholders para el Service de forma basica agregando parametros como app_name, protocol, service_port y target_port
- **values.yaml**: Da valores de configuracion para el reemplazo en los templates con parametros especificos de la aplicacion, servicio, recursos, etc.

### Script `setup.sh`
Se añade la instalacion del hook `pre-commit` en el script `setup.sh` para que los desarrolladores realicen sus commits pero antes verificar si los templates cumplen con la sintaxis YAML

### Flujo de Trabajo

En este Sprint delegamos issues parte del sprint 1 a cada integrante

   <div align="center">
      <img src="https://i.postimg.cc/hGp1m793/pc41-1.png" alt="image1" width="800" />
   </div>

Para cada issue se agregaron los siguientes fields:

- **Puntos:** Nivel de importancia de la issue en un rango de 1-5
- **Horas estimadas:** Tiempo estimado para completar la issue
- **Horas reales:** Tiempo real invertido al completar la issue
- **Sprint:** Sprint al que pertenece

Por ejemplo esta son los fields de la issue #4 Crear hook pre-commit para validar la sintaxis YAML

   <div align="center">
      <img src="https://i.postimg.cc/cLrVJYPT/pc41-2.png" alt="image2" width="250" />
   </div>

El kanban board inicial para el sprint 1, en donde todas las issues estan en Sprint Backlog luego se van moviendo a In progress cuando se va desarrollando

   <div align="center">
      <img src="https://i.postimg.cc/ZKh8nhgQ/pc41-3.png" alt="image3" width="1100" />
   </div>

Al terminar la issue, esta se movieron a la columna Review/QA en donde los otros desarrolladores revisaron los cambios si estan bien implementados

El desarrollador encargado de la issue envia una Pull Request desde la rama que trabajo a la rama develop en donde se solicita la revision de los cambios y si estan conformes con los cambios o nuevas implementaciones hechas 

   <div align="center">
      <img src="https://i.postimg.cc/rsDPp2Ps/pc41-5.png" alt="image6" width="800" />
   </div>

Los otros desarrolladores revisan el PR y envian un mensaje de confirmacion en donde se aprueba el PR

   <div align="center">
      <img src="https://i.postimg.cc/Jn6FmzKS/pc41-6.png" alt="image7" width="600" />
   </div>

Cuando los otros desarrolladores aceptaron los cambios hechos, el desarrollador encargado de la issue le asigna las horas reales que le tomo completar esta issue y se mueve a la columna Done, asi hasta que todas las issues lleguen a Done

   <div align="center">
      <img src="https://i.postimg.cc/RVQcnDxZ/pc41-4.png" alt="image4" width="1000" />
   </div>

### Historial y ramas
Durante todo el desarrollo del sprint 1 creamos estas ramas:

   <div align="center">
      <img src="https://i.postimg.cc/jjDH0tgk/pc41-7.png" alt="image10" width="750" />
   </div>

Y el historial de commits durante todo el desarrollo del sprint 1 fue el siguiente:

   <div align="center">
      <img src="https://i.postimg.cc/6QFdBgF6/pc41-8.png" alt="image11" width="900" />
   </div>

Durante el desarrollo del Sprint 1 cada desarrollador trabajo cada issue asignada en ramas diferentes en paralelo, al terminar todas las issues y tener todo los cambios en la rama develop, nace otra rama release desde develop en donde se agrega la documentacion correspondiente al sprint 1, asi aplicando correctamente las politicas de Git Flow

## Sprint 2

### Estructura del proyecto

```
Generador-de-manifiestos-de-Kubernetes-parametrizado/
│
├── hooks/
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
│
├── src/
│   ├── __init__.py
│   └── manifest_generator.py
│
├── templates/
│   ├── deployment.yaml.template
│   ├── service.yaml.template
│   └── values.yaml
│
├── tests/
│   ├── __init__.py
│   ├── test_multiples_manifiestos.py
│   ├── test_validacion.py
│   └── test_validar_values.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── setup.sh
```
### Modulos

#### src/
Se relizaron cambio en **manifest_generator.py** tanto como nuevas implementaciones y tambien refactorizacion de metodos ya existentes:
- Agregada validacion de esquema JSON para values.yaml usando `jsonschema`
- Integracion de Jinja2 para procesamiento de templates
- Implementada funcion `validar_manifiesto_k8s()` con `kubectl dry-run --validate`
- Modificado para procesar multiples templates

#### tests/
Se agregaron tests para validar las nuevas implementaciones:
- Pruebas unitarias para validacion de esquema con casos validos e invalidos
- Tests para procesamiento de multiples manifiestos
- Validacion de que los manifiestos generados son sintacticamente correctos
- Pruebas de manejo de errores en validaciones
- Test de validacion usando `minikube` y `kubectl`  

### Flujo de Trabajo

En este Sprint delegamos issues parte del sprint 2 a cada integrante

   <div align="center">
      <img src="https://i.postimg.cc/1tcC99bh/pc41-9.png" alt="image1" width="800" />
   </div>

Tambien hicimos uso del Kaban Board para el Sprint 2, de igual forma que se hizo para el Sprint 1 tambien se hizo para el Sprint 2 hasta que todas las issues terminaron en la columna Done

   <div align="center">
      <img src="https://i.postimg.cc/HsPSWvvx/pc41-10.png" alt="image1" width="1100" />
   </div>

### Historial y ramas
Durante todo el desarrollo del sprint 2 creamos estas ramas:

   <div align="center">
      <img src="https://i.postimg.cc/j5Kc3p28/pc41-11.png" alt="image10" width="350" />
   </div>

Y el historial de commits durante todo el desarrollo del sprint 2 fue el siguiente:

   <div align="center">
      <img src="https://i.postimg.cc/8kZ4wnSH/pc41-12.png" alt="image11" width="1000" />
   </div>

Durante el desarrollo del Sprint 2 cada desarrollador trabajo cada issue asignada en ramas diferentes en paralelo, al terminar todas las issues y tener todo los cambios en la rama develop, nace otra rama release/sprint2 desde develop en donde se agrega la documentacion correspondiente al sprint 2, asi aplicando correctamente las politicas de Git Flow

## Sprint 3

### Estructura del proyecto

```
Generador-de-manifiestos-de-Kubernetes-parametrizado/
│
├── helm-chart/app-chart/ 
│ 	├── templates/
│	│ 	├── _helpers.tpl
│	│ 	├── deployment.yaml
│	│ 	└── service.yaml
│ 	├── .helmignore
│ 	├── Chart.yaml
│ 	└── values.yaml
│
├── hooks/
│   ├── commit-msg
│   ├── pre-commit
│   └── pre-push
│
├── src/
│   ├── __init__.py
│   └── manifest_generator.py
│
├── templates/
│   ├── deployment.yaml.template
│   ├── service.yaml.template
│   └── values.yaml
│
├── tests/
│   ├── __init__.py
│   ├── test_e2e_local.py
│   ├── test_multiples_manifiestos.py
│   ├── test_validacion.py
│   └── test_validar_values.py
│
├── .gitignore
├── README.md
├── requirements.txt
├── comparar.sh
└── setup.sh
```
### Modulos

#### helm-chart/app-chart/
Se creo un Helm Chart minimo que reproduce la funcionalidad del generador de manifiestos. Sirve como punto de comparacion entre Helm y la generacion propia de YAML.

- `Chart.yaml`: Define los metadatos del chart (nombre, version, etc.)
    
- `values.yaml`: Archivo donde se definen los valores por defecto que se inyectaran en las plantillas
    
- `.helmignore`: Especifica archivos a ignorar al empaquetar el chart
    
- `templates/`: Contiene las plantillas del Deployment y Service

#### src/
Se agrego nueva funcionalidad en `manifest_generator.py`, con la funcion `desplegar_manifiestos()` se puede desplegar los manifiestos generados usando `kubectl apply`


#### tests/ 
Se agregaron nuevos test para pruebas End-to-End (E2E) para validar el correcto funcionamiento del despliegue

- `test_e2e_local.py`: Prueba E2E que genera los manifiestos, los aplica con `kubectl` y valida:
    
    - Que el Pod se encuentre en estado `Running`
        
    - Que el Service sea accesible desde el entorno local

### Flujo de Trabajo

En este Sprint delegamos issues parte del sprint 3 a cada integrante

   <div align="center">
      <img src="https://i.postimg.cc/pdbywPBQ/pc41-13.png" alt="image1" width="800" />
   </div>

Tambien hicimos uso del Kaban Board para el Sprint 3, de igual forma que se hizo para el Sprint 1 y Sprint 2 tambien se hizo para el Sprint 3 hasta que todas las issues terminaron en la columna Done

   <div align="center">
      <img src="https://i.postimg.cc/pdCxsvcL/pc41-14.png" alt="image1" width="1100" />
   </div>

   <div align="center">
      <img src="https://i.postimg.cc/gjCPx2jN/pc41-15.png" alt="image1" width="1100" />
   </div>

### Historial y ramas
Durante todo el desarrollo del sprint 3 creamos estas ramas:

   <div align="center">
      <img src="https://i.postimg.cc/HsMgfXvK/pc41-16.png" alt="image10" width="290" />
   </div>

Y el historial de commits durante todo el desarrollo del sprint 3 fue el siguiente:

   <div align="center">
      <img src="https://i.postimg.cc/bYTCdJDJ/pc41-17.png" alt="image11" width="1000" />
   </div>

Durante el desarrollo del Sprint 3 de igual forma para el Sprint 1 y 2, cada desarrollador trabajo cada issue asignada en ramas diferentes en paralelo, al terminar todas las issues y tener todo los cambios en la rama develop, nace otra rama release/sprint3 desde develop en donde se agrega la documentacion correspondiente al sprint 3, asi aplicando correctamente las politicas de Git Flow

## Videos
Se referencia el link de los video de cada cada Sprint hecho:

- **Sprint 1**: [link_video_script1](https://unipe-my.sharepoint.com/:v:/g/personal/guido_chipana_c_uni_pe/Ee90swFctiRJolXvJaV-kG0BqBnW4DzHIRHrsNBbQiJl8Q?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=bLpz5y)

- **Sprint 2**: [link_video_script2](https://unipe-my.sharepoint.com/:v:/g/personal/guido_chipana_c_uni_pe/EVNmnqCV_R9PhcDtPqz3Dp0B9gQepbF2OBd1B3-ASJXUIQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=tgAtgA)

- **Sprint 3**: [link_video_script3](https://unipe-my.sharepoint.com/:v:/g/personal/guido_chipana_c_uni_pe/EYNPrvjfrNhDnWYWkp5ENhkBmEG15aYuc6yJs3dyaG6mbw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DEsLda)

- **Video final**: [link_video_final](https://unipe-my.sharepoint.com/:v:/g/personal/guido_chipana_c_uni_pe/EW5e-fY4dW5OhKPJELwZoUkBk9AMLTpl17kLS0igXY6C_Q?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=pTZG4S)
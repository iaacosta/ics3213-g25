# Instrucciones de uso

## Modelo de optimización
Se necesita una licencia de `gurobipy` para poder ejecutarlo correctamente con el comando:

```sh
python optimization/assignation_model.py
```

## Modelo de simulación

Se requiere tener los datos como el formato de los archivos `./data/optimal_routes.csv` o `./data/original_routes.csv`. Si se usan más camiones, agregarlos a `./data/trucks.csv`, asegurarse que los identificadores sean los mismos.

Dado que este modelo no utiliza librerías pagadas, se puede utilizar con `pipenv`.

### Obtenedor de tiempos entre puntos

Para obtener los tiempos entre rutas se usa la API de Google Maps. Se necesita setear la variable de entorno `GOOGLE_API_KEY` para agregar al archivo `./data/times_matrix.csv` los tiempos entre rutas adicionales.

Su ejecución es con el siguiente comando

```sh
python index.py fetch
```

### Simulador simple

Para hacer una simulación base (una iteración), se ejecuta el siguiente comando:

```sh
python index.py simulate
```

Se puede obtener mayor información con `python index.py simulate -h`


### Simulador largo

Para hacer una simulación con `n` iteraciones, se debe abrir el Jupyter Notebook adjunto (`long_simulation.ipynb`). Está autodocumentado

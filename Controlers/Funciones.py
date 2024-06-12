import random

def crear_grupos(numero_grupos, diccionario_nombres):
    """
    Función que crea grupos a partir de un diccionario de nombres.
    Intenta que la suma de los valores de cada grupo sea lo más igual posible.
    Args:
        numero_grupos: El número de grupos a crear.
        diccionario_nombres: Un diccionario con nombres como claves y 1 o 2 como valores.
    Returns:
        Una lista de listas, donde cada sublista representa un grupo.
    """
    nombres = list(diccionario_nombres.keys())
    valores = list(diccionario_nombres.values())

    # Mezclamos los nombres aleatoriamente
    combinados = list(zip(nombres, valores))
    random.shuffle(combinados)
    nombres[:], valores[:] = zip(*combinados)

    grupos = [[] for _ in range(numero_grupos)]
    sumas_grupos = [0] * numero_grupos

    # Asignamos nombres a los grupos intentando equilibrar las sumas
    for nombre, valor in zip(nombres, valores):
        # Encontramos el grupo con la suma más baja
        indice_grupo = sumas_grupos.index(min(sumas_grupos))
        grupos[indice_grupo].append(nombre)
        sumas_grupos[indice_grupo] += valor

    return grupos


# Método 1: Usando frozenset (recomendado)
def generate_id_frozenset(tuplas):
    """
    Genera un ID usando frozenset, que es independiente del orden
    """
    return hash(frozenset(tuplas))

# Método 2: Ordenando las tuplas y usando hash
def generate_id_sorted(tuplas):
    """
    Ordena las tuplas y genera un hash del resultado
    """
    sorted_tuplas = tuple(sorted(tuplas))
    return hash(sorted_tuplas)

# Método 3: Ordenando y usando string (más legible pero menos eficiente)
def generate_id_string(tuplas):
    """
    Ordena las tuplas y genera un ID string
    """
    sorted_tuplas = tuple(sorted(tuplas))
    return str(sorted_tuplas)

# Método 4: Usando hashlib para IDs más consistentes entre ejecuciones
import hashlib

def generate_id_hashlib(tuplas):
    """
    Genera un ID usando hashlib que es consistente entre ejecuciones
    """
    sorted_tuplas = tuple(sorted(tuplas))
    data = str(sorted_tuplas).encode('utf-8')
    return hashlib.md5(data).hexdigest()

# Ejemplos de uso
if __name__ == "__main__":
    # Casos de prueba
    caso1 = [(0, 0), (0, 1)]
    caso2 = [(0, 1), (0, 0)]  # Mismo contenido, diferente orden
    caso3 = [(1, 2), (3, 4)]
    caso4 = [(3, 4), (1, 2)]  # Mismo contenido, diferente orden
    
    print("=== Método 1: frozenset ===")
    id1_fs = generate_id_frozenset(caso1)
    id2_fs = generate_id_frozenset(caso2)
    id3_fs = generate_id_frozenset(caso3)
    id4_fs = generate_id_frozenset(caso4)
    
    print(f"Caso 1: {caso1} -> ID: {id1_fs}")
    print(f"Caso 2: {caso2} -> ID: {id2_fs}")
    print(f"¿Son iguales?: {id1_fs == id2_fs}")
    print(f"Caso 3: {caso3} -> ID: {id3_fs}")
    print(f"Caso 4: {caso4} -> ID: {id4_fs}")
    print(f"¿Son iguales?: {id3_fs == id4_fs}")
    
    print("\n=== Método 2: sorted + hash ===")
    id1_s = generate_id_sorted(caso1)
    id2_s = generate_id_sorted(caso2)
    print(f"Caso 1: {caso1} -> ID: {id1_s}")
    print(f"Caso 2: {caso2} -> ID: {id2_s}")
    print(f"¿Son iguales?: {id1_s == id2_s}")
    
    print("\n=== Método 3: string ===")
    id1_str = generate_id_string(caso1)
    id2_str = generate_id_string(caso2)
    print(f"Caso 1: {caso1} -> ID: {id1_str}")
    print(f"Caso 2: {caso2} -> ID: {id2_str}")
    print(f"¿Son iguales?: {id1_str == id2_str}")
    
    print("\n=== Método 4: hashlib (consistente) ===")
    id1_hl = generate_id_hashlib(caso1)
    id2_hl = generate_id_hashlib(caso2)
    print(f"Caso 1: {caso1} -> ID: {id1_hl}")
    print(f"Caso 2: {caso2} -> ID: {id2_hl}")
    print(f"¿Son iguales?: {id1_hl == id2_hl}")

# Función recomendada para uso general
def generar_id(tuplas):
    """
    Función principal recomendada para generar IDs consistentes
    """
    return hash(frozenset(tuplas))

# Ejemplo adicional con más casos
print("\n=== Pruebas adicionales ===")
test_cases = [
    [(0, 0), (0, 1)],
    [(0, 1), (0, 0)],
    [(1, 1), (2, 2)],
    [(2, 2), (1, 1)],
    [(5, 3), (1, 8)],
    [(1, 8), (5, 3)]
]

ids_generados = {}
for i, case in enumerate(test_cases):
    id_generado = generar_id(case)
    print(f"Caso {i+1}: {case} -> ID: {id_generado}")
    
    # Verificar si ya vimos este ID
    if id_generado in ids_generados:
        print(f"  ¡Coincide con el caso {ids_generados[id_generado]}!")
    else:
        ids_generados[id_generado] = i+1
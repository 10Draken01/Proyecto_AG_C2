import json
# leer y escribir archivos JSON

with open('./data/plants_with_id.json', 'r', encoding='utf-8') as file:
    plants_data = json.load(file)
    total_plants = len(plants_data)
    medicinal_count = 0
    aromatic_count = 0
    vegetal_count = 0
    ornamental_count = 0

    seen_names = set()
    duplicates = []

    for plant in plants_data:
        name = plant.get('name')
        if name in seen_names:
            duplicates.append(name)
        else:
            seen_names.add(name)

        types = plant.get('type', [])
        if 'medicinal' in types:
            medicinal_count += 1
        if 'aromatic' in types:
            aromatic_count += 1
        if 'vegetable' in types:
            vegetal_count += 1
        if 'ornamental' in types:
            ornamental_count += 1

    print(f"Número total de plantas: {total_plants}")
    print(f"Número de vegetales: {vegetal_count}")
    print(f"Número de plantas medicinales: {medicinal_count}")
    print(f"Número de plantas aromáticas: {aromatic_count}")
    print(f"Número de plantas ornamentales: {ornamental_count}")

    if duplicates:
        print("Plantas repetidas encontradas:")
        for name in duplicates:
            print(f"- {name}")
    else:
        print("No hay plantas repetidas.")
import json

with open('faker_data_generation.ipynb') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        for j, line in enumerate(cell['source']):
            print(f"Cell {i} Line {j+1}: {repr(line)}")


import ast
import json

with open('faker_data_generation.ipynb') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        print(f"--- Cell {i} ---")
        print(source)
        try:
            ast.parse(source)
            print("Parses OK!")
        except Exception as e:
            print(f"Parse error: {e}")

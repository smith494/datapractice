import ast
import json

with open('faker_data_generation.ipynb') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        print(f"--- Cell {i} ---")
        try:
            ast.parse(source)
            print("Parses OK with ast!")
        except Exception as e:
            print(f"AST Parse error: {e}")
            
        # also try compiling
        try:
            compile(source, f"<cell {i}>", "exec")
            print("Compiles OK!")
        except Exception as e:
            print(f"Compile error: {e}")

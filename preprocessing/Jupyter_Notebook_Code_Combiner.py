import json
import glob

# input name here
notebook_name = "auto_training"

def extract_code_cells(notebook_path):
    with open(notebook_path, "r") as f:
        notebook = json.load(f)
    code_cells = [
        cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "code"
    ]
    return code_cells


def save_combined_code(cells, output_path):
    with open(output_path, "w") as f:
        for cell in cells:
            f.write("".join(cell) + "\n\n")


notebook_paths = glob.glob(f"{notebook_name}.ipynb")
all_code_cells = []

for path in notebook_paths:
    all_code_cells.extend(extract_code_cells(path))

save_combined_code(all_code_cells, f"{notebook_name}.py")

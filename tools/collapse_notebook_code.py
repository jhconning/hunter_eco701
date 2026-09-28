import glob
import json
import os

notebook_files = glob.glob("notebooks/*.ipynb")
print(f"Found {len(notebook_files)} notebooks to process:")

for nb_file in notebook_files:
    with open(nb_file, "r", encoding="utf-8") as f:
        nb_data = json.load(f)
    
    modified_count = 0
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") == "code":
            if "metadata" not in cell:
                cell["metadata"] = {}
            if "tags" not in cell["metadata"]:
                cell["metadata"]["tags"] = []
            
            tags = cell["metadata"]["tags"]
            if "hide-input" not in tags:
                tags.append("hide-input")
                modified_count += 1
                
    with open(nb_file, "w", encoding="utf-8") as f:
        json.dump(nb_data, f, indent=1, ensure_ascii=False)
        
    print(f"  Processed {nb_file}: added 'hide-input' tag to {modified_count} code cells")

print("Done updating all notebooks.")

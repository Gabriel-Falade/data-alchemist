# Logic to loop through folders 

import os
from markitdown import MarkItDown
md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
add_docs = []

path = r"C:\ugahacks\data-alchemist\backend\test-files"

# looping through each file and appending to array
for e in os.scandir(path):
    if e.is_file():
        with open(e.path, "r") as f:
            results = md.convert(f)
            add_docs.append(results.text_content)
            f.close()


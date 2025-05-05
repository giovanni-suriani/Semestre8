from PyPDF2 import PdfReader, PdfWriter

import os, sys
path_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path_directory) # Correct to the path to the Django project
print(f"path_directory: {sys.path}")

# Load your original PDF

input_path = f"{path_directory}/OTI-II-Texto1-1SEM2025-2.pdf"  # Replace with your actual path
reader = PdfReader(input_path)

CONST = -1  # Adjust this constant if needed

# Define the modules and their page ranges
modules = {
    "01_Simplex": (13 + CONST, 52 + CONST),
    "02_Dualidade": (53 + CONST, 74 + CONST),
    "03_Dualidade": (75 + CONST, 84 + CONST),
}


# Split and write each module
for title, (start, end) in modules.items():
    writer = PdfWriter()
    for i in range(start, end + 1):
        writer.add_page(reader.pages[i])
    with open(f"{title}.pdf", "wb") as f:
        writer.write(f)
    print(f"Created: {title}.pdf")

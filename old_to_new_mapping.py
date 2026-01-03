import os
import json
from pathlib import Path

# Old to new class mapping
old_to_new_mapping = {
    0: 0,  # hand -> Master ID 0
    1: 2,  # conical beaker -> Master ID 2 (Beaker)
    2: 3,  # erlenmeyer flask -> Master ID 3 (Conical_Flask)
    3: 4,  # reagent bottle -> Master ID 4 (Reagent_Bottle)
    4: 5,  # pipette -> Master ID 5 (Pipette)
    5: 1,  # eggplant shaped flask -> Master ID 1
    6: 6,  # separatory funnel -> Master ID 6 (Separating_Funnel)
}
# old_to_new_mapping = {
#     0: 2,      # Beaker -> Beaker
#     1: 7,      # Buchner_Funnel -> Buchner_Funnel
#     2: 8,      # Burette_Stands -> Burette_Stands
#     3: 9,      # Calorimeter -> Calorimeter
#     4: 3,      # Conical_Flask -> Conical_Flask
#     5: 10,     # Funnel -> Funnel
#     6: 11,     # Glass_Rod -> Glass_Rod
#     7: 12,     # Measuring_Cylinder -> Measuring_Cylinder
#     8: 13,     # Mechanical_Balance_Scale -> Mechanical_Balance_Scale
#     9: 14,     # Nessler_Reagent_Bottle -> Nessler_Reagent_Bottle
#     10: 5,     # Pipette -> Pipette
#     11: 15,    # Porcelain_Mortar_Pestle -> Porcelain_Mortar_Pestle
#     12: 16,    # Precision_Weight_Scale -> Precision_Weight_Scale
#     13: 4,     # Reagent_Bottle -> Reagent_Bottle
#     14: 17,    # Round_Bottom_Flask_Borosilicate_Glass_1_Neck
#     15: 18,    # Round_Bottom_Flask_Borosilicate_Glass_2_Neck
#     16: 19,    # Round_Bottom_Flask_Borosilicate_Glass_3_Neck
#     17: 6,     # Separating_Funnel -> Separating_Funnel
#     18: 20,    # Spirit_Lamp -> Spirit_Lamp
#     19: 21,    # TestTube_Holder -> TestTube_Holder
#     20: 22,    # Test_Tube -> Test_Tube
#     21: 23,    # Volumetric_Flask -> Volumetric_Flask
#     22: 24,    # Volumetric_Pipet -> Volumetric_Pipet
#     23: 25,    # Wash_Bottle -> Wash_Bottle
#     24: 26,    # Weighing_Bottle -> Weighing_Bottle
# }

# Create new output folder
output_dir = Path("./valid/new")
output_dir.mkdir(exist_ok=True)

# Process annotation files in test folder
test_dir = Path("./valid/labels")
for txt_file in test_dir.glob("*.txt"):
    new_lines = []
    with open(txt_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                old_class = int(parts[0])
                new_class = old_to_new_mapping.get(old_class, old_class)
                new_line = f"{new_class} " + " ".join(parts[1:])
                new_lines.append(new_line)

    # Save to new folder
    output_file = output_dir / txt_file.name
    with open(output_file, 'w') as f:
        f.write("\n".join(new_lines))
    print(f"Converted: {txt_file.name}")

print(f"Conversion completed! Files saved to: {output_dir}")
import numpy as np
from generate import generate_diagram

with open("data.txt", "r", encoding="utf-8") as f:
    raw = f.read().strip()

groups = raw.split("|||")

for i, group in enumerate(groups, 1):
    group = group.strip()
    if not group:
        continue

    moment_data = []
    axial_data = []
    reading_moment = True

    for line in group.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line == "---":
            reading_moment = False
            continue
        value = float(line)
        if reading_moment:
            moment_data.append(value)
        else:
            axial_data.append(value)

    moment_data = np.array(moment_data)
    axial_data = np.array(axial_data)
    output_path = f"./img/Figure_{i}.svg"
    generate_diagram(moment_data, axial_data, output_path)
    print(f"Figure_{i}.svg 已保存")

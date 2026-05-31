import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"


def generate_diagram(moment_data, axial_data, output_path, flip_moment=False):
    R = 4
    angle_rad = np.deg2rad(101)

    moment_scale = 1.2 / max(np.max(moment_data) - np.min(moment_data), 1)
    axial_scale = 0.6 / max(np.max(axial_data) - np.min(axial_data), 1)

    theta_m = np.linspace(np.pi / 2, np.pi / 2 + angle_rad, len(moment_data))
    theta_n = np.linspace(np.pi / 2, np.pi / 2 - angle_rad, len(axial_data))

    x_m = R * np.cos(theta_m)
    y_m = R * np.sin(theta_m)
    x_n = R * np.cos(theta_n)
    y_n = R * np.sin(theta_n)

    nx_m = x_m / R
    ny_m = y_m / R
    nx_n = x_n / R
    ny_n = y_n / R

    sign = -1 if flip_moment else 1
    x_force_m = x_m + sign * moment_data * moment_scale * nx_m
    y_force_m = y_m + sign * moment_data * moment_scale * ny_m
    x_force_n = x_n + axial_data * axial_scale * nx_n
    y_force_n = y_n + axial_data * axial_scale * ny_n

    fig, ax = plt.subplots(figsize=(8, 8))

    theta_full = np.linspace(np.pi / 2 - angle_rad, np.pi / 2 + angle_rad, 400)
    x_circle = R * np.cos(theta_full)
    y_circle = R * np.sin(theta_full)
    ax.plot(x_circle, y_circle, color="black", linewidth=1.5)

    ax.plot(x_force_m, y_force_m, color="black", linewidth=1, label="弯矩图")

    for i in range(len(x_m)):
        ax.plot(
            [x_m[i], x_force_m[i]], [y_m[i], y_force_m[i]], color="gray", linewidth=0.6
        )

    # label_interval = 3
    label_interval = 1
    for i in range(0, len(moment_data), label_interval):
        value = moment_data[i]
        offset = 0.4
        if value >= 0:
            text_x = x_force_m[i] + offset * nx_m[i]
            text_y = y_force_m[i] + offset * ny_m[i]
        else:
            text_x = x_force_m[i] - offset * nx_m[i]
            text_y = y_force_m[i] - offset * ny_m[i]
        ax.text(text_x, text_y, f"{value:.1f}", fontsize=14, ha="center", va="center")

    ax.plot(x_force_n, y_force_n, color="black", linewidth=1, label="轴力图")

    for i in range(len(x_n)):
        ax.plot(
            [x_n[i], x_force_n[i]], [y_n[i], y_force_n[i]], color="gray", linewidth=0.6
        )

    for i in range(0, len(axial_data), label_interval):
        value = axial_data[i]
        offset = 0.3
        if value >= 0:
            text_x = x_force_n[i] + offset * nx_n[i]
            text_y = y_force_n[i] + offset * ny_n[i]
        else:
            text_x = x_force_n[i] - offset * nx_n[i]
            text_y = y_force_n[i] - offset * ny_n[i]
        ax.text(text_x, text_y, f"{value:.1f}", fontsize=14, ha="center", va="center")

    label_r = R * 0.5
    label_x = label_r * np.sin(angle_rad / 2)
    label_y = label_r * np.cos(angle_rad / 2)
    ax.text(-label_x, label_y, "kN·m", fontsize=20, ha="center", va="center")
    ax.text(label_x, label_y, "kN", fontsize=20, ha="center", va="center")

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-R - 2, R + 2)
    ax.set_ylim(-R - 2, R + 2)
    ax.axis("off")

    plt.tight_layout()
    # plt.savefig(output_path, pad_inches=0, dpi=150)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0, dpi=150)
    plt.close()


if __name__ == "__main__":
    with open("data.txt", "r", encoding="utf-8") as f:
        raw = f.read().strip()

    group = raw.split("|||")[0].strip()

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
    generate_diagram(moment_data, axial_data, "./img/Figure_1.svg", flip_moment=True)

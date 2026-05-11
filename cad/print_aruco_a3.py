"""Layout all ArUco markers on A3 pages and export as PDF.

Page 1 (A3 landscape): footprint + height + material markers (IDs 0-11), 5x5cm each
Page 2 (A3 landscape): method selectors (IDs 20-22), 8x8cm each

Usage:
    python cad/print_aruco_a3.py

Output: cad/aruco-markers/PRINT_A3.pdf
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

OUTPUT_PDF = Path("cad/aruco-markers/PRINT_A3.pdf")
OUTPUT_DIR = Path("cad/aruco-markers")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# A3 landscape in inches (420 x 297 mm)
A3_W = 420 / 25.4
A3_H = 297 / 25.4

LABELS = {
    **{i: f"Footprint {i}" for i in range(10)},
    10: "Height",
    11: "Material",
    20: "Method:\nMasonry",
    21: "Method:\n3D Print",
    22: "Method:\nPrefab",
}


def make_marker_img(marker_id: int, px: int = 800) -> np.ndarray:
    img = cv2.aruco.generateImageMarker(ARUCO_DICT, marker_id, px)
    return img


def page1(pdf: PdfPages):
    """Page 1: IDs 0-11 (small markers, 5x5cm), 6 per row, 2 rows."""
    fig, axes = plt.subplots(2, 6, figsize=(A3_W, A3_H))
    fig.patch.set_facecolor('white')
    plt.suptitle(
        "ArUco Markers — Footprint / Height / Material   |   Print at 100% on A3   |   DICT_4X4_50",
        fontsize=9, y=0.98
    )

    ids_page1 = list(range(10)) + [10, 11]

    for idx, mid in enumerate(ids_page1):
        row, col = divmod(idx, 6)
        ax = axes[row][col]
        img = make_marker_img(mid, 600)
        ax.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
        ax.axis('off')

        label = LABELS[mid]
        ax.set_title(f"ID {mid}\n{label}", fontsize=7, pad=3)

        # Physical size hint
        ax.text(0.5, -0.08, "5 × 5 cm", transform=ax.transAxes,
                ha='center', va='top', fontsize=6, color='#555555')

        # Border rect
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.5)
            spine.set_edgecolor('#aaaaaa')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig, dpi=300)
    plt.close(fig)
    print("[OK] Page 1: IDs 0-11")


def page2(pdf: PdfPages):
    """Page 2: IDs 20-22 (method selectors, 8x8cm), 3 across."""
    fig, axes = plt.subplots(1, 3, figsize=(A3_W, A3_H))
    fig.patch.set_facecolor('white')
    plt.suptitle(
        "ArUco Markers — Method Selectors   |   Print at 100% on A3   |   DICT_4X4_50",
        fontsize=9, y=0.99
    )

    for idx, mid in enumerate([20, 21, 22]):
        ax = axes[idx]
        img = make_marker_img(mid, 900)
        ax.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
        ax.axis('off')
        ax.set_title(f"ID {mid}\n{LABELS[mid]}", fontsize=10, pad=6)
        ax.text(0.5, -0.04, "8 × 8 cm", transform=ax.transAxes,
                ha='center', va='top', fontsize=8, color='#555555')

    # Instruction box
    fig.text(0.5, 0.04,
             "Mount on RFID pedestal sides.  One marker per construction method.",
             ha='center', fontsize=8, color='#333333',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0f0f0', edgecolor='#aaaaaa'))

    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    pdf.savefig(fig, dpi=300)
    plt.close(fig)
    print("[OK] Page 2: IDs 20-22")


def main():
    print(f"Generating {OUTPUT_PDF} ...\n")
    with PdfPages(str(OUTPUT_PDF)) as pdf:
        page1(pdf)
        page2(pdf)

        # PDF metadata
        d = pdf.infodict()
        d['Title']   = 'Hardware III — ArUco Markers for Printing'
        d['Subject'] = 'DICT_4X4_50, IDs 0-11 (5x5cm) and 20-22 (8x8cm)'

    print(f"\nSaved: {OUTPUT_PDF.resolve()}")
    print("Open the PDF and print at 100% scale (no 'fit to page') on A3 paper.")


if __name__ == "__main__":
    main()

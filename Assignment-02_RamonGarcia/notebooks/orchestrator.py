#!/usr/bin/env python
"""
Orchestrator: runs all analysis notebooks and saves output images.

Requirements:
    pip install papermill kaleido

Usage:
    python orchestrator.py
"""
import os
import time

try:
    import papermill as pm
except ImportError:
    print("papermill is required.  Install with:  pip install papermill")
    raise

from datetime import datetime

NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EXECUTED_DIR = os.path.join(NOTEBOOKS_DIR, "executed")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(EXECUTED_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

NOTEBOOKS = [
    "NB-01_Geometry_Import_Setup.ipynb",
    "NB-02_Graph_Metrics_Shortest_Path.ipynb",
    "NB-03_Centrality_Analysis.ipynb",
    "NB-04_Community_Detection_Degree_Centrality.ipynb",
    "NB-05_Visibility_Isovist_Analysis.ipynb",
]

def main():
    total_start = time.time()
    results = []

    for nb in NOTEBOOKS:
        input_path = os.path.join(NOTEBOOKS_DIR, nb)
        name, ext = os.path.splitext(nb)
        output_path = os.path.join(EXECUTED_DIR, f"{name}_{TIMESTAMP}{ext}")

        print(f"\n{'=' * 60}")
        print(f"Running: {nb}")
        print(f"{'=' * 60}")

        start = time.time()
        try:
            pm.execute_notebook(
                input_path,
                output_path,
                parameters={"SAVE_IMAGES": True},
                kernel_name="python3",
                execution_timeout=1800,  # 30 min per cell
            )
            elapsed = time.time() - start
            print(f"  OK  ({elapsed:.1f}s)")
            results.append((nb, "OK", elapsed))
        except Exception as e:
            elapsed = time.time() - start
            print(f"  FAILED  ({elapsed:.1f}s) - {e}")
            results.append((nb, "FAILED", elapsed))

    total_elapsed = time.time() - total_start

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    for nb, status, elapsed in results:
        print(f"  [{status:6s}] {nb}  ({elapsed:.1f}s)")
    print(f"\nTotal time: {total_elapsed:.1f}s")
    print(f"Images saved to: {ASSETS_DIR}")

    # List saved images
    images = sorted(f for f in os.listdir(ASSETS_DIR) if f.endswith(".png"))
    if images:
        print(f"\nGenerated images ({len(images)}):")
        for img in images:
            print(f"  {img}")

if __name__ == "__main__":
    main()

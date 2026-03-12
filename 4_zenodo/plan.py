#!/usr/bin/env python3
from stepup.core.api import copy, glob, mkdir, static
from stepup.reprep.api import make_inventory, sync_zenodo, wrap_git, zip_inventory

# Create Git Repository Archive
glob("../.git/**", _defer=True)
wrap_git(
    "git archive --format=zip --output 4_zenodo/main.zip main",
    out="4_zenodo/main.zip",
    workdir="../",
)

# Copy and pack all PDFs into a single zip file
mkdir("reports/")
static("../3_report/", "../3_report/overview.pdf", "../3_report/reports/")
copy("../3_report/overview.pdf", "reports/")
paths_pdf = ["reports/overview.pdf"]
for m in glob("../3_report/reports/${*case}/", case="*_v*"):
    path_src = m.single / "report.pdf"
    path_dst = f"reports/{m.case}.pdf"
    static(path_src)
    copy(path_src, path_dst)
    paths_pdf.append(path_dst)
make_inventory(*paths_pdf, "reports/inventory.txt")
zip_inventory("reports/inventory.txt", "reports.zip")

# Create a ZIP file of the JSON files containing all the results shown in tables and plots
paths_json = []
static("../3_report/results/")
for m in glob("../3_report/results/${*case}/", case="*_v*"):
    paths_json.extend(glob(m.single / "*.json"))
make_inventory(*paths_json, "../3_report/results/inventory.txt")
zip_inventory("../3_report/results/inventory.txt", "results.zip")

# Upload to zenodo
static(
    "zenodo.md",
    "zenodo.yaml",
)
glob("../LICENSE-*.txt")
sync_zenodo("zenodo.yaml")

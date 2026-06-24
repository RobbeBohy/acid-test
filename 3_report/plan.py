#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
# SPDX-License-Identifier: CC-BY-SA-4.0 OR LGPL-3.0-or-later
"""Definition of the StepUp workflow for analyzing the validation of STACIE with the ACID test set.

See README.md for instructions on how to run this workflow.
"""

from stepup.core.api import glob, loadns, mkdir, runpy, static
from stepup.reprep.api import compile_typst, wrap_git

# Write Git information to text file for inclusion in documents.
glob("../.git/**", _defer=True)
wrap_git("git describe --tags", out="git-version.txt")
wrap_git("git log -n1 --pretty='format:(%cs %h)'", out="git-date.txt")

# Declare static files.
static(
    "../1_dataset/",
    "../1_dataset/output/",
    "../1_dataset/output/codec.zip",
    "../1_dataset/settings.json",
    "../matplotlibrc",
    "scripts/",
    "results/",
    "cases.yaml",
    "overview.typ",
    "plan_report.py",
    "report.typ",
    "references.bib",
    "summary_stats.typ",
)
glob("scripts/*.py")

# Extract and plot short sequences from ACID dataset for inclusion in documents.
settings = loadns("../1_dataset/settings.json", do_amend=True)
mkdir("reports/")
mkdir("reports/shared/")
path_codec = "../1_dataset/output/codec.zip"
for kernel in settings.kernels:
    path_zip = f"../1_dataset/output/{kernel}.zip"
    static(path_zip)
    runpy(
        "./${inp} 1024 256 ${out}",
        inp=[
            "scripts/plot_sequences_subset.py",
            path_zip,
            path_codec,
            "../matplotlibrc",
        ],
        out=f"reports/shared/subset_{kernel}.svg",
    )

# Collect all JSON results files and hand them over to a report planning script.
for m in glob("results/${*case}/"):
    mkdir(f"reports/{m.case}/")
    paths_json = glob(f"results/{m.case}/*.json")
    runpy(
        f"./${{inp}} {m.case}",
        inp=["plan_report.py", *paths_json],
    )
compile_typst("overview.typ")

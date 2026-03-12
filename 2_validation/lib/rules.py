"""Helper functions for StepUp plan.py, a.k.a. rules in other build systems."""

from stepup.core.api import glob, loadns, mkdir, runpy, static


def test_stacie(version: str):
    static(
        "../scripts/",
        "../lib/",
        "../../1_dataset/",
        "../../1_dataset/settings.json",
        "../../1_dataset/output/",
        "../../matplotlibrc",
        "../../3_report/",
    )
    glob("../scripts/*.py")
    glob("../lib/*.py")

    # Prepare output directories
    mkdir("output/")
    mkdir("figures/")
    mkdir("../../3_report/results/")
    for model in ["quad", "lorentz"]:
        mkdir(f"output/{model}/")
        mkdir(f"figures/{model}/")
        mkdir(f"../../3_report/results/stacie_v{version}_{model}/")

    settings = loadns("../../1_dataset/settings.json", do_amend=True)
    for kernel in settings.kernels:
        models = ["quad"]
        if kernel.startswith("exp1"):
            models.append("lorentz")
        for nseq in settings.nseqs:
            for nstep in settings.nsteps:
                path_zip = f"../../1_dataset/output/{kernel}_nstep{nstep:05d}_nseq{nseq:04d}.zip"
                static(path_zip)
                for model in models:
                    path_pickle = (
                        f"output/{model}/estimate_{kernel}_nstep{nstep:05d}_nseq{nseq:04d}.pickle"
                    )
                    runpy(
                        f"${{inp}} {model} ${{out}}",
                        inp=["../scripts/stacie_estimate.py", path_zip],
                        out=[path_pickle],
                    )
                    runpy(
                        "${inp} ${out}",
                        inp=["../scripts/stacie_plot.py", path_pickle, "../../matplotlibrc"],
                        out=[
                            f"figures/{model}/estimate_{kernel}_nstep{nstep:05d}_nseq{nseq:04d}.pdf"
                        ],
                    )
                    runpy(
                        "${inp} ${out}",
                        inp=["../scripts/stacie_extract.py", path_pickle],
                        out=[
                            f"../../3_report/results/stacie_v{version}_{model}/"
                            f"summary_{kernel}_nstep{nstep:05d}_nseq{nseq:04d}.json"
                        ],
                    )
                    runpy(
                        "${inp} ${out}",
                        inp=["../scripts/stacie_mcmap.py", path_pickle],
                        out=[
                            f"../../3_report/results/stacie_v{version}_{model}/"
                            f"mcmap_{kernel}_nstep{nstep:05d}_nseq{nseq:04d}.json"
                        ],
                    )

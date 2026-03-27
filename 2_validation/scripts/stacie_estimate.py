#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
# SPDX-License-Identifier: CC-BY-SA-4.0 OR LGPL-3.0-or-later
"""Compute results with STACIE for a given test case."""

import argparse
import json
import pickle
import zipfile
from traceback import print_exc

import numpy as np
import scipy as sp
from path import Path
from stacie import compute_spectrum, estimate_acint


def main():
    args = parse_args()
    run(args.case, args.model, args.out)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute results with STACIE for a given test case."
    )
    parser.add_argument(
        "case",
        type=Path,
        help="Path to the input ZIP file from the ACID dataset.",
    )
    parser.add_argument(
        "model",
        type=str,
        choices=["quad", "lorentz"],
        help="Spectrum model to use for the estimation.",
    )
    parser.add_argument(
        "out",
        type=Path,
        help="Path to the output pickle file to store the results.",
    )
    return parser.parse_args()


def run(inp: Path, model: str, out: Path):
    # Exit early if the file exists, meaning that is not recomputed even if the script changed.
    # You need to remove the files manually.
    if Path(out).is_file():
        return

    # Get the model from a helper function to delay imports.
    # This ensures that the script can work with different versions of STACIE.
    spectrum_model = {
        "quad": get_quad_model,
        "lorentz": get_lorentz_model,
    }[model]()

    # Open the input ZIP file and process all sequences.
    with zipfile.ZipFile(inp, "r") as zf, zf.open("meta.json") as fh:
        meta = json.load(fh)
    std = np.sqrt(meta["var"])
    data = np.load(inp)
    results = []
    for iseed in range(meta["nseed"]):
        cfdi = data[f"sequences_{iseed:02d}"]
        imax = np.iinfo(cfdi.dtype).max + 1
        sequences = sp.stats.norm(scale=std).ppf((cfdi + 0.5) / imax)
        # The prefactor 2.0 is used as a matter of convention. It is not critical.
        # It just facilitates reading plots as the DC component of the PSD will
        # now match the autocorrelation integral without additional factors.
        spectrum = compute_spectrum(((2.0, np.array(row)) for row in sequences), prefactors=None)
        spectrum.amplitudes_ref = np.array(data["psd"])
        try:
            result = estimate_acint(
                spectrum,
                spectrum_model,
                neff_max=max(1024, spectrum.nstep // 8),
            )
            result.props["iseed"] = iseed
            print(f"{iseed:3d} {result.neff:7.1f}   {result.acint:8.5f}")
            results.append(result)
        except Exception as exc:  # noqa: BLE001
            # Catch all exceptions, so we can keep track of how many runs failed.
            print(f"{iseed:3d} {exc}")
            print_exc()
    results.sort(key=lambda r: r.props["acint"])
    with open(out, "bw") as fh:
        pickle.dump(results, fh)


def get_quad_model():
    from stacie.model import ExpPolyModel

    return ExpPolyModel([0, 2])


def get_lorentz_model():
    from stacie.model import LorentzModel

    return LorentzModel()


if __name__ == "__main__":
    main()

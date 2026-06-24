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
from path import Path
from stacie import compute_spectrum, estimate_acint


def main():
    args = parse_args()
    run(args.case, args.codec, args.nstep, args.nseq, args.model, args.out)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute results with STACIE for a given test case."
    )
    parser.add_argument(
        "case",
        type=Path,
        help="Path to the kernel ZIP file from the ACID dataset.",
    )
    parser.add_argument(
        "codec",
        type=Path,
        help="Path to the codec ZIP file for decoding integer sequences.",
    )
    parser.add_argument(
        "nstep",
        type=int,
        help="Number of steps.",
    )
    parser.add_argument(
        "nseq",
        type=int,
        help="Number of sequences.",
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


def run(inp: Path, codec: Path, nstep: int, nseq: int, model: str, out: Path):
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

    # Load the codec lookup table for decoding integer sequences.
    lookup_table = np.load(codec)["midpoint"]

    step_path = f"nstep{nstep:05d}/"
    seq_path = f"nstep{nstep:05d}/nseq{nseq:04d}/"

    with zipfile.ZipFile(inp, "r") as zf, zf.open("meta.json") as fh:
        meta = json.load(fh)
    std = np.sqrt(meta["var"])
    data = np.load(inp)
    psd_ref = data[step_path + "psd.npy"]

    results = []
    for iseed in range(meta["nseed"]):
        cdfi = data[seq_path + f"sequences_{iseed:02d}.npy"]
        sequences = lookup_table[cdfi] * std
        # The prefactor 2.0 is used as a matter of convention. It is not critical.
        # It just facilitates reading plots as the DC component of the PSD will
        # now match the autocorrelation integral without additional factors.
        spectrum = compute_spectrum(((2.0, np.array(row)) for row in sequences), prefactors=None)
        spectrum.amplitudes_ref = psd_ref
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

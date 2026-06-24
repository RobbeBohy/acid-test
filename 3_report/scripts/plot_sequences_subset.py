#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
# SPDX-License-Identifier: CC-BY-SA-4.0 OR LGPL-3.0-or-later

import argparse
import json
import zipfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from path import Path
from stacie.spectrum import compute_spectrum


def main():
    args = parse_args()
    run(args.zip, args.codec, args.mplrc, args.nstep, args.nseq, args.svg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a small subset from the full data suitable for plotting the inputs."
    )
    parser.add_argument("zip", type=Path, help="Input ACID ZIP file with full data.")

    parser.add_argument("codec", type=Path, help="Codec ZIP file for decoding integer sequences.")
    parser.add_argument("mplrc", type=Path, help="Matplotlib RC file.")
    parser.add_argument("nstep", type=int, help="Number of steps.")
    parser.add_argument("nseq", type=int, help="Number of sequences.")
    parser.add_argument("svg", type=Path, help="Output SVG image.")
    return parser.parse_args()


def run(path_zip: Path, path_codec: Path, path_mplrc: Path, nstep: int, nseq: int, path_svg: Path):
    with zipfile.ZipFile(path_zip, "r") as zf, zf.open("meta.json") as fh:
        meta = json.load(fh)
    std = np.sqrt(meta["var"])

    lookup_table = np.load(path_codec)["midpoint"]
    data = np.load(path_zip)

    step_path = f"nstep{nstep:05d}/"
    seq_path = f"nstep{nstep:05d}/nseq{nseq:04d}/"

    times = data[step_path + "times.npy"]
    freqs = data[step_path + "freqs.npy"]
    acf = data[step_path + "acf.npy"]
    psd = data[step_path + "psd.npy"]

    # Only take sequences for the first seed for plotting
    cdfi = data[seq_path + "sequences_00.npy"]
    sequences = lookup_table[cdfi] * std

    # Compute spectrum with Stacie, to be included in plot, only for first seed
    spectrum = compute_spectrum(sequences, prefactors=2)
    empirical_acf = np.fft.irfft(spectrum.amplitudes)
    empirical_psd = spectrum.amplitudes

    # Create figure with three subplots
    mpl.rc_file(path_mplrc)
    fig, axs = plt.subplots(1, 3, figsize=(7, 2.3))
    plot_inputs(axs[0], times, sequences)
    plot_acf(axs[1], times, acf, empirical_acf)
    plot_psd(axs[2], freqs, psd, empirical_psd)
    fig.savefig(path_svg)
    plt.close(fig)


def plot_inputs(ax, times, sequences):
    nstep = 100
    ax.plot(times[:nstep], sequences[0, :nstep].T, color="k")
    ax.set_xlabel("Time $t$")
    ax.set_ylabel(r"$\hat{x}(t)$")
    ax.set_title("Example input sequence")


REF_PROPS = {"ls": ":", "lw": 2, "color": "k", "alpha": 0.5}


def plot_acf(ax, times, model_acf, data_acf):
    ndelta = 100
    ax.plot(times[:ndelta], data_acf[:ndelta], color="C4")
    ax.plot(times[:ndelta], model_acf[:ndelta], **REF_PROPS)
    ax.set_xlabel(r"Time lag $\Delta_t$")
    ax.set_ylabel(r"COV[$\hat{x}(t)$, $\hat{x}(t+\Delta_t)$]")
    ax.set_title("Autocorrelation Function")


def plot_psd(ax, freqs, model_psd, data_psd):
    nfreq = freqs.searchsorted(0.1)
    ax.plot(freqs[:nfreq], data_psd[:nfreq], color="C9")
    ax.plot(freqs[:nfreq], model_psd[:nfreq], **REF_PROPS)
    ax.set_xlabel(r"Frequency $f$")
    ax.set_ylabel(r"Amplitude")
    ax.set_ylim(0, None)
    ax.set_title("Power Spectral Density")


if __name__ == "__main__":
    main()

#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
# SPDX-License-Identifier: CC-BY-SA-4.0
#SBATCH --job-name=report
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=5G

source ./.loadvenv
export PATH=$(realpath ${PWD}/scripts/):$PATH
time stepup boot -n ${SLURM_CPUS_PER_TASK}

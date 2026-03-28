<!--
SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

:rotating_light:
This repository is under development as part of the preparation for the ACID 2 release.

You can view the latest version of the ACID 1 dataset and validation results at the following URLs:

- https://github.com/molmod/acid/tree/v1.2.0
- https://zenodo.org/records/18044643

# The AutoCorrelation Integral Drill (ACID) 2 -- Test Bench

This repository contains the scripts and
[StepUp workflows](https://reproducible-reporting.github.io/stepup-core/stable/)
to validate algorithms and their implementations
for computing an integral of an autocorrelation function,
using the "AutoCorrelation Integral Drill" (ACID) test set.
More details on the ACID test can be found in the corresponding
[ACID Git repository](https://github.com/molmod/acid).

A description, test reports and and an archived copy of this repository can be found on Zenodo:
[10.5281/zenodo.18947912](https://doi.org/10.5281/zenodo.18947912).

For now, ACID is only used to validate the [STACIE](https://molmod.github.io/stacie/) algorithm and its implementation.
We plan to test also other programs in the future, including:

- Kute: <https://gitlab.com/nafomat/kute>
- Sportran: <https://github.com/sissaschool/sportran>
- Binary-based time sampling (MSD method): <https://doi.org/10.1063/5.0188081>
- MSD implementation in MDAnalysis: <https://docs.mdanalysis.org/2.0.0/documentation_pages/analysis/msd.html#computing-an-msd>
- Tidydynamics: <https://lab.pdebuyl.be/tidynamics/>

## License

The copyright disclaimer and license conditions are specified at the beginning of each file in the repository,
or, when the header cannot be edited, in the `RESUSE.toml` file.

In summary, the majority of the files in this repository are licensed under
the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).
The main exceptions are the Python files, which have a choice of license between
CC BY-SA 4.0 and the GNU Lesser General Public License v3.0 or later (LGPL-3.0-or-later).

License deeds and legal code for all licenses used in this repository are available in the `LICENSES/` directory.
They can also be consulted online at the following URLs:

- <https://creativecommons.org/licenses/by-sa/4.0/>
- <https://www.gnu.org/licenses/lgpl-3.0.html>

## Citation

If you use this dataset in your research, please cite the following publication:

> Gözdenur Toraman, Dieter Fauconnier, and Toon Verstraelen
> "STable AutoCorrelation Integral Estimator (STACIE):
> Robust and accurate transport properties from molecular dynamics simulations"
> *Journal of Chemical Information and Modeling* 2025, 65 (19), 10445–10464,
> [doi:10.1021/acs.jcim.5c01475](https://doi.org/10.1021/acs.jcim.5c01475),
> [arXiv:2506.20438](https://arxiv.org/abs/2506.20438).
>
> ```bibtex
> @article{Toraman2025,
>  author = {G\"{o}zdenur Toraman and Dieter Fauconnier and Toon Verstraelen},
>  title = {STable AutoCorrelation Integral Estimator (STACIE): Robust and accurate transport properties from molecular dynamics simulations},
>  journal = {Journal of Chemical Information and Modeling},
>  volume = {65},
>  number = {19},
>  pages = {10445--10464},
>  year = {2025},
>  month = {sep},
>  url = {https://doi.org/10.1021/acs.jcim.5c01475},
>  doi = {10.1021/acs.jcim.5c01475},
> }
> ```

## Overview

This consists of four main parts:

1. [`1_dataset/`](1_dataset/):
   Contains a script to download the appropriate ACID dataset from Zenodo.
   It will mirror the `1_dataset/output` directory of the ACID repository,
   which contains the raw data files for the test set.
1. [`2_validation/`](2_validation/):
   Workflows to recompute the validation results for a selection of
   autocorrelation integral estimators with the ACID test set.
   Subdirectories `test_*` contain workflows for different implementations and versions.
1. [`3_report/`](3_report/):
   A workflow with post-processing scripts of the validation results
   to regenerate the figures and tables, similar to those in the initial STACIE paper.
1. [`4_zenodo/`](4_zenodo/):
   A workflow to package and upload the generated data to Zenodo.

When regenerating the data and the validation of results, the workflows
in these directories must be executed in the order listed above.
Each directory contains a `README.md` file that provides more details.

All instructions below assume that you are working on a compute cluster with SLURM job scheduling.
If you are working on a local machine, run `job.sh` scripts directly instead of submitting them with `sbatch`.

## ACID Data Download

Before any of the validations can be performed, the ACID dataset must be downloaded.
Be mindful of the size of the dataset (43 GB) and the bandwidth of your internet connection.

```bash
(cd 1_dataset/; sbatch download.sh)
```

This job script only uses the `wget`, `unzip` and standard posix commands,
which should present by default on most Linux systems.

Instead of downloading the large dataset, you can also regenerate it locally,
by following the instructions in the [ACID repository](https://github.com/molmod/acid).
Due to differences in floating-point arithmetics and compiler optimizations,
the generated dataset may differ from the one on Zenodo,
but it should be sufficiently similar for validation purposes.

To use your local copy, run the script `link.sh` in the same directory.
It assumes that the `output` directory is located at `../acid/1_dataset/output`.

## Software Environments

There are two approaches to software environments in this repository:

1. The `3_report/` and `4_zenodo/` directories use the software environment
   defined in the top-level `requirements.in` file.
   This venv is also suitable for working with this repository in general,
   e.g. it includes pre-commit.
1. The directories `2_validation/test_*` define their own software environment,
   as needed by the different implementations being validated.
   Such independent environments allows for benchmarking different versions of the same software,
   or to support incompatable requirements between different implementations.
   A local `requirements.in` file is used to define the software environment for each workflow.

To create a virtual environment, run or submit the top-level `setup-venv-pip.sh`
from the directory that contains the `requirements.in` file.
If you want this script to use a specific Python version,
set the `PYTHON3` environment variable before running it.
For example:

```bash
export PYTHON3=/usr/bin/python3.13  # optional
cd 2_validation/test_stacie_v1.0.0
sbatch ../../setup-venv-pip.sh
```

After the virtual environment has been created,
you can run or submit the script `job.sh` to perform the actual work.
If you want to work interactively with the virtual environment,
you can source the `.loadvenv` script in the workflow directory.

Note that the workflows and scripts in this repository require Python 3.11 or higher.
They have only been tested on an `x86_64` Linux system (so far).
All results on Zenodo were generated using the following module
on the Tier2 VSC compute cluster donphan

```bash
module load Python/Python/3.13.1-GCCcore-14.2.0
```

When the `setup-venv-pip.sh` script detects the presence of the `$VSC_HOME`
environment variable, it will automatically load this Python module
and include it in the generated `.loadvenv` script.

## How to Work With This Git Repository

Please, follow these guidelines to make clean commits to this repository:

1. Install [pre-commit](https://pre-commit.com/) on your system.
   (It is included in the `requirements.in` file,
   so it will be installed in the virtual environment when you run `setup-venv-pip.sh`.)
1. Install the pre-commit hook by running `pre-commit install` in the root directory of this repository.
1. Use `git commit` as you normally would.

If you are working in an environment with limited permissions,
you can install pre-commit locally by running the following commands:

```bash
wget https://github.com/pre-commit/pre-commit/releases/download/v4.5.1/pre-commit-4.5.1.pyz
python pre-commit-4.5.1.pyz install
```

## How to Make a New Release

After having updated the contents of the repository, the following steps are needed
to make a new release on Zenodo:

- Update `CHANGELOG.md` with a new version section, describing the changes since the last release.

- Update the version number in `4_zenodo/zenodo.yaml`.

- Upload a draft release to Zenodo by running

  ```bash
  (cd 4_zenodo/; sbatch job.sh)
  ```

- Visit the dataset page on Zenodo and click on "New version".
  The files and metadata will already be present due to the previous step.
  Request the DOI for the new draft and add this information to `CHANGELOG.md`.

- Commit all changes to Git and run `git tag` with the new version number.

- Ensure that all validation results are up to date by running the workflows in `2_validation/`.
  For example:

  ```bash
  (cd 2_validation/test_stacie_v1.0.0/; sbatch job.sh)
  ```

  Note that the tests write JSON files with validation results to `3_report/results`,
  which are included in the Zenodo release.

- Recompile all PDF files in the repository to include the Git hash in the PDF frontmatter:

  ```bash
  (cd 3_report/; sbatch job.sh)
  ```

- Sync your local data one last time with Zenodo:

  ```bash
  (cd 4_zenodo/; sbatch job.sh)
  ```

- Log in to <https://zenodo.org/>, go to your draft release,
  check that all files have been uploaded correctly, and publish the release.

- Push your commits and tags to GitHub.

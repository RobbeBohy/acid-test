<!--
SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

First release of a separate ACID test bench repository.
Change below are with respect to the ACID dataset version 1.2.0.

### Changed

- Define a separate software environment for each workflow.
- Possibility to validate different programs and generate reports for each.
- Summary reports aggregating results obtained with different programs
  (and their version and settings), in preparation for a comparative study.
- Generalize the report template to be reusable for different programs,
  their versions and their settings.

### Fixed

- Corrected threshold for `neff` validity,
  which is now correctly based on the number of model parameters in the scripts,
  instead of being hardcoded to 40.
  (This was only consistent for two parameters.)
  This only has a minor influence on a few numbers in the final reports,
  and does not affect the test data itself.

[unreleased]: https://github.com/molmod/acid-test

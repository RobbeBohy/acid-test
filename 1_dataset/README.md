<!--
SPDX-FileCopyrightText: © 2026 ACID Test Contributors <https://doi.org/10.5281/zenodo.18947912>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Local Copy of ACID 2 Dataset

This directory should contain a local copy of the ACID 2 dataset.

There are two ways to set up the dataset:

1. Download the dataset from Zenodo and unpack it in this directory.
   This is the recommended procedure for precise reproducibility,
   as the dataset is versioned and archived on Zenodo.
   The script `./download.sh` will download (43 GB) and unpack the dataset,
   using the appropriate filename conventions.
1. Create a symbolic link to a locally generated version of the dataset.
   This is almost equally good and saves you from having to download the dataset.
   You should first clone the `acid` repository in a sibling directory to `acid-test`,
   generate the data by following instructions in the `acid` repository.
   Finally, you can run the script `./link.sh` here to create a symbolic link to the generated dataset.

# BVI-AOM Dataset Downloader

A Python wrapper around AWS CLI for downloading the [BVI-AOM](https://arxiv.org/abs/2408.03265) (Bristol Vision Institute - Alliance for Open Media) video dataset hosted on Netflix's Open Content platform.

It simply syncs the entire S3 bucket and then extracts the dataset archives for you.

## Installation

```bash
pip install bvi-aom
```

## Usage

### Command Line Interface

Sync and extract the full dataset:

```bash
bvi-aom /path/to/storage
```


### Python API

```python
from bvi_aom import BVIAOMDataset

# Sync the full dataset and extract all archives
dataset = BVIAOMDataset("/path/to/storage")
```


This package depends on `awscli`. After installation, make sure the `aws` command is available on your `PATH`.  
No AWS credentials are required because downloads use `--no-sign-request`.

## What it does

- Runs:

  ```bash
  aws s3 sync s3://download.opencontent.netflix.com/bvi_aom_dataset/ /path/to/storage --no-sign-request
  ```

- Then, in `/path/to/storage`, it looks for these archives and extracts them into the same folder, deleting the archives after successful extraction:

  - `1088p.tar.gz`
  - `2176p_part_a.tar.gz`
  - `2176p_part_b.tar.gz`
  - `2176p_part_c.tar.gz`
  - `2176p_part_d.tar.gz`
  - `2176p_part_e.tar.gz`
  - `2176p_part_f.tar.gz`
  - `272p.tar.gz`
  - `544p.tar.gz`


## Notes and Requirements

- Ensure you have **enough disk space** for all resolutions.
- If you re-run the command or Python API, `aws s3 sync` will only fetch changed/missing files, and already-extracted archives that no longer exist will be skipped safely.

## Dataset Information

The BVI-AOM dataset is a collection of high-quality video sequences used for video codec development and evaluation by the Alliance for Open Media (AOM).
The files can be quite large, so ensure you have sufficient storage space.

## License

The BVI-AOM dataset is subject to its own licensing terms. Please refer to [BVI-AOM Paper](https://arxiv.org/abs/2408.03265).

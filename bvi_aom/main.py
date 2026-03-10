import os
import subprocess
import tarfile


S3_BUCKET = "s3://download.opencontent.netflix.com/bvi_aom_dataset/"

TAR_FILES = [
    "1088p.tar.gz",
    "2176p_part_a.tar.gz",
    "2176p_part_b.tar.gz",
    "2176p_part_c.tar.gz",
    "2176p_part_d.tar.gz",
    "2176p_part_e.tar.gz",
    "2176p_part_f.tar.gz",
    "272p.tar.gz",
    "544p.tar.gz",
]


class BVIAOMDataset:
    def __init__(self, storage_path: str):
        """
        Initialize the BVI-AOM Dataset downloader.

        Syncs the S3 bucket to a local folder, then extracts all tar/tar.gz
        files into the same folder and removes the archives.
        """
        self.storage_path = os.path.abspath(storage_path)
        os.makedirs(self.storage_path, exist_ok=True)
        self.setup()

    def setup(self) -> None:
        self._sync_s3()
        self._extract_and_remove_tars()

    def _sync_s3(self) -> None:
        """Sync the S3 bucket to the local storage path using aws s3 sync."""
        cmd = [
            "aws", "s3", "sync",
            S3_BUCKET,
            self.storage_path,
            "--no-sign-request",
        ]
        print(f"Syncing {S3_BUCKET} to {self.storage_path}...")
        subprocess.run(cmd, check=True)
        print("Sync completed.")

    def _extract_and_remove_tars(self) -> None:
        """Extract each known tar file to the same folder, then remove it."""
        for name in TAR_FILES:
            tar_path = os.path.join(self.storage_path, name)
            if not os.path.exists(tar_path):
                continue
            print(f"Extracting {name} to {self.storage_path}...")
            try:
                with tarfile.open(tar_path, "r:*") as tar:
                    tar.extractall(path=self.storage_path)
                os.remove(tar_path)
                print(f"Extracted and removed {name}.")
            except tarfile.ReadError as e:
                print(f"Error reading {tar_path}: {e}. Skipping.")
            except Exception as e:
                print(f"Unexpected error with {tar_path}: {e}. Skipping.")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Download BVI-AOM dataset: sync S3 bucket to a local folder and extract tar files."
    )
    parser.add_argument(
        "storage_path",
        type=str,
        help="Path to store the dataset (S3 contents will be synced here)",
    )
    args = parser.parse_args()

    BVIAOMDataset(args.storage_path)

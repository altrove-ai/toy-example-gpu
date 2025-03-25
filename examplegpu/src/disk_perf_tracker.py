"""
Module to log the use of storage objects
"""

# import pandas as pd
import csv
import time

import psutil


class DiskPerformanceTracker:
    def __init__(
        self,
        disk_names: list[str],
        file_path: str,
        silent: bool = False,
        time_interval: float = 0.5,
    ) -> None:
        self.fp = file_path
        self.disk_names = disk_names
        self.silent = silent
        self.time_interval = time_interval
        self.field_names = [
            "read_count",
            "write_count",
            "read_bytes",
            "write_bytes",
            "read_time",
            "write_time",
        ]

    def run(self) -> None:
        csvfile = open(self.fp, "w", newline="")
        writer = csv.DictWriter(csvfile, fieldnames=self.field_names)

        t_start: float = time.time()
        while True:
            try:
                all_disk_data = psutil.disk_io_counters(perdisk=True)
                disk_data_: list[int]
                print(f"zzz, all_disk_data: {all_disk_data}")
                for disk_path_, disk_data_ in all_disk_data.items():
                    if disk_path_ in self.disk_names:
                        writer.writerow(
                            {
                                field_name_: field_value_
                                for field_name_, field_value_ in zip(
                                    self.field_names, disk_data_, strict=False
                                )
                            }
                        )
                if not self.silent:
                    print(f"Time: {time.time() - t_start:.2f}s")
                time.sleep(self.time_interval)
            except KeyboardInterrupt:
                print(f"User interruption detected : Exiting...")
                break

        csvfile.close()


if __name__ == "__main__":
    disk_names = [
        "/dev/nvme1n1",
        "/dev/nvme2n1",
        "/dev/nvme3n1",
        "/dev/nvme4n1",
        "/dev/nvme5n1",
        "/dev/nvme6n1",
        "/dev/nvme7n1",
        "/dev/nvme8n1",
        "/dev/md0",
    ]
    disk_performance_tracker = DiskPerformanceTracker(
        disk_names=disk_names,
        file_path="disk_io_log.csv",
        silent=False,
        time_interval=0.5,
    )
    disk_performance_tracker.run()

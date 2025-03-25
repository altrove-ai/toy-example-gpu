from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import override

import wandb
from wandb.wandb_run import Run


class Logger(ABC):
    @abstractmethod
    def log(self, data: dict) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


class LocalLogger(Logger):
    """Single process logger."""

    def __init__(self, log_file: str) -> None:
        self.log_file = log_file
        self.file = open(self.log_file, "w")

    def log(self, data: dict) -> None:
        self.file.write(json.dumps(data) + "\n")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class WandbLogger(Logger):
    """Single process W&B logger."""

    def __init__(
        self,
        project_name: str,
        run_name: str,
        config: dict,
    ) -> None:
        self.project_name = project_name
        self.run_name = run_name
        self.config = config
        self._run: Run | None = None

    def log(self, data: dict) -> None:
        if self._run is None:
            raise ValueError(
                "Initialize the logger before starting with : with wandb_logger as logger:"
            )
        self._run.log(data)

    @override
    def __enter__(self) -> WandbLogger:
        self._run = wandb.init(
            entity="altrove-tech-team",
            project=self.project_name,
            name=self.run_name,
            config=self.config,
        )
        return self

    @override
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._run.finish()

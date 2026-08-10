# SPDX-FileCopyrightText: 2026 Duncan McDougall <duncan.mcdougall@rfi.ac.uk>
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from .data import ManData as ManData
from .data_source_2d import Man2DDataSource as Man2DDataSource


def data_files() -> dict[str, Path]:
    root = Path(__file__).parent
    return {
        "man1": root / "man1.txt",
        "man2": root / "man2.txt",
        "man3": root / "man3.txt",
        "man4": root / "man4.txt",
        "colors": root / "colors.json",
    }

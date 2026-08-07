# SPDX-FileCopyrightText: 2026 Duncan McDougall <duncan.mcdougall@rfi.ac.uk>
#
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

import numpy as np


class ManData:
    def __init__(self):
        self.colors: dict[str, dict[str, list]]
        self.men: list[dict[str, np.ndarray]]

        with open(Path(__file__).parent / "colors.json", "r") as fle:
            data = json.load(fle)

        self.colors = data

        self.men: list[dict] = []
        for ii in range(4):
            man_pos = []
            man_int = []
            with open(Path(__file__).parent / f"man{ii + 1}.txt") as fle:
                for row, line in enumerate(fle):
                    for col, colour in enumerate(line.strip()):
                        colour_mz = self.colors[colour]["mz"]
                        colour_int = self.colors[colour]["int"]
                        man_pos.extend([[col, row, mz] for mz in colour_mz])
                        man_int.extend(colour_int)

            self.men.append({"pos": np.array(man_pos).T, "int": np.array(man_int)})

        self.total_pos = self.men[0]["pos"]
        self.total_int = self.men[0]["int"]
        for ii, man in enumerate(self.men):
            if ii == 0:
                continue
            pos = man["pos"]
            pos[2, :] += ii * 60
            self.total_pos = np.concatenate([self.total_pos, pos], axis=1)
            self.total_int = np.concatenate([self.total_int, man["int"]])

        self.shape = (8, 8, 240)
        self.dense = np.zeros(self.shape)
        for pos, intensity in zip(self.total_pos.T, self.total_int, strict=True):
            self.dense[*pos] = intensity

        self.density = self.total_int.shape[0] / np.prod(self.shape)

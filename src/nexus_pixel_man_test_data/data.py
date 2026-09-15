# SPDX-FileCopyrightText: 2026 Duncan McDougall <duncan.mcdougall@rfi.ac.uk>
#
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

import numpy as np
import sparse


def hex2rgb(hex: str):
    h = hex.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


class ManData:
    def __init__(self):
        self.colors: dict[str, dict[str, list]]
        self.men: list[dict[str, np.ndarray]]

        with open(Path(__file__).parent / "colors.json", "r") as fle:
            data = json.load(fle)

        self.colors = data

        self.rgb_colors = {
            "R": hex2rgb("#EE161F"),
            "G": hex2rgb("#2DBD0B"),
            "B": hex2rgb("#122BD9"),
            "Y": hex2rgb("#FCD301"),
            "S": hex2rgb("#E3B687"),
            "N": hex2rgb("#AB7D4F"),
            "F": hex2rgb("#8C5E39"),
            "E": hex2rgb("#0F0F0F"),
            "_": hex2rgb("#000000"),
        }

        self.men: list[dict] = []
        for ii in range(4):
            man_pos = []
            man_int = []
            man_rgb = []
            with open(Path(__file__).parent / f"man{ii + 1}.txt") as fle:
                for row, line in enumerate(fle):
                    for col, colour in enumerate(line.strip()):
                        colour_mz = self.colors[colour]["mz"]
                        colour_int = self.colors[colour]["int"]
                        man_pos.extend([[col, row, mz] for mz in colour_mz])
                        man_int.extend(colour_int)
                        man_rgb.append([col, row, *self.rgb_colors[colour]])

            self.men.append(
                {
                    "pos": np.array(man_pos).T,
                    "int": np.array(man_int),
                    "rgb": np.array(man_rgb),
                }
            )

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

        coords = []
        rgb = []
        for i in range(len(self.men)):
            for row in self.men[i]["rgb"]:
                for j in range(3):
                    coords.append([i, *row[[1, 0]], j])
                    rgb.append(row[2 + j])
        self.rgb_image = sparse.COO(
            coords=np.array(coords).T, data=rgb, shape=(4, 8, 8, 3)
        ).todense()

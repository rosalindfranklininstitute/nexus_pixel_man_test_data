# SPDX-FileCopyrightText: 2026 Duncan McDougall <duncan.mcdougall@rfi.ac.uk>
#
# SPDX-License-Identifier: Apache-2.0

import json
from random import randint


def hex2rgb(hex: str):
    h = hex.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def generate_spectra(col, col_max_count, mz, mz_offset) -> tuple[list, list]:

    cols = []
    while len(cols) < col_max_count and col > 0:
        c = randint(0, col)
        if c > 0:
            cols.append(c)
        col -= c
    if col > 0:
        cols.append(col)

    count = len(cols)
    mz_so_far = 0
    mzs = []
    for ii in range(count):
        mz_so_far = randint(mz_so_far + 1, mz - count + ii - 1)
        mzs.append(mz_so_far + mz_offset)

    return cols, mzs


if __name__ == "__main__":
    colors = {
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

    color_spectra = {}
    spec_colors = {}

    for k, col in colors.items():
        print(f"{k} {col}")
        r, g, b = col
        rs = generate_spectra(r, 10, 20, 0)
        gs = generate_spectra(g, 10, 20, 20)
        bs = generate_spectra(b, 10, 20, 40)

        c = rs[0] + gs[0] + bs[0]
        m = rs[1] + gs[1] + bs[1]
        spec_colors[k] = {"mz": m, "int": c, "color": [r, g, b]}

    with open("colors.json", "w") as fle:
        json.dump(spec_colors, fle, indent=2)

    men = [
        [
            "__GGGG__",
            "__GGG_G_",
            "__SESE__",
            "__SSNS__",
            "_GBGGBG_",
            "_SBBBBS_",
            "__BBBB__",
            "__F__F__",
        ],
        [
            "__BBBB__",
            "__BBB_B_",
            "__SESE__",
            "__SSNS__",
            "SBRBBRBS",
            "__RRRR__",
            "__RRRR__",
            "__F__F__",
        ],
        [
            "__RRRR__",
            "__RRR_R_",
            "__SESE__",
            "_SSSNS__",
            "_RYRRYR_",
            "__YYYYS_",
            "__YYYY__",
            "__F__F__",
        ],
        [
            "__YYYY__",
            "__YYY_Y_",
            "__SESE__",
            "__SSNS__",
            "_YRYYRYS",
            "_SRRRR__",
            "__RRRR__",
            "__F__F__",
        ],
    ]

    for ii, man in enumerate(men):
        with open(f"man{ii + 1}.txt", "w") as fle:
            for line in man:
                fle.write(line)
                fle.write("\n")

from pathlib import Path

import numpy as np
import h5py

from xartus.lib.chunker import count_chunks_to_cover
from xartus.api import data_convert
from xartus.lib.data_source import Axis, AxisType
from nexus_pixel_man_test_data import Man2DDataSource, ManData, data_files


def test_default_dataset():
    """
    A basic test that exercises some of the configuration options for the data converter.
    This is a repeat of one of the basic tests in Xartus.
    The idea is this allows quickly making changes to the data source and asserting that basic functionality is preserved.
    """
    man_file = data_files()["man1"]
    man_data = ManData()
    man_data_source = Man2DDataSource(
        man_data,
        supplementary_axes=[
            Axis("time", 0, AxisType.EXACT, np.float32, "s"),
            Axis("error", 2, AxisType.EXACT, np.float32, ""),
        ],
        multipliers=dict(x=0.1, y=0.1, mz=0.1, time=1.0, error=1.0),
    )
    filename = Path(__file__).parent / "man.nxs"
    if filename.exists():
        filename.unlink()

    process_args = data_convert.ProcessArgs(
        in_path=man_file,
        out_path=filename,
        chunk_max_byte_count=1024 * 1024,
        memory_max_byte_count=1024 * 1024 * 1024,
        data_source=man_data_source,
    )
    data_convert.process(process_args, {})

    with h5py.File(filename, "r") as fle:
        for data_name in ["images", "spectra"]:
            assert f"/entry/{data_name}/data/signal" in fle
            for axis in man_data_source.axes.values():
                assert f"/entry/{data_name}/data/{axis.name}" in fle
                assert fle[f"/entry/{data_name}/data/{axis.name}"].dtype == axis.dtype
                assert f"{axis.name}_indices" in fle[f"/entry/{data_name}/data/"].attrs
                assert (
                    fle[f"/entry/{data_name}/data"].attrs[f"{axis.name}_indices"]
                    == axis.primary_axis
                )

            assert np.all(
                fle[f"/entry/{data_name}/data"].attrs["axes"] == ["x", "y", "mz"]
            )

            assert (
                fle[f"/entry/{data_name}/data/signal"].shape
                == man_data_source.man_data.shape
            )

            np.testing.assert_allclose(
                fle[f"/entry/{data_name}/data/signal"][:, :, :],
                man_data_source.man_data.dense,
            )

        total_image = np.sum(man_data_source.man_data.dense, axis=2)
        assert fle["/entry/total_image/data/signal"].shape == (2, *total_image.shape)
        np.testing.assert_allclose(
            fle["/entry/total_image/data/signal"][1, :, :], total_image
        )

        total_spectra = np.sum(man_data_source.man_data.dense, axis=(0, 1))
        assert fle["/entry/total_spectra/data/signal"].shape == (
            2,
            *total_spectra.shape,
        )
        np.testing.assert_allclose(
            fle["/entry/total_spectra/data/signal"][1, :], total_spectra
        )

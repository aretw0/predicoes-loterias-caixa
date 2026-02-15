import os
import pytest
import pandas as pd
from data.manager import DataManager


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "concurso": [1, 2, 3],
        "d1": [5, 10, 15],
        "d2": [12, 23, 34],
        "d3": [25, 36, 47],
    })


class TestDataManagerParquet:
    def test_export_parquet_creates_file(self, sample_df, tmp_path):
        path = str(tmp_path / "test.parquet")
        result = DataManager.export_parquet(sample_df, path)
        assert os.path.exists(result)

    def test_parquet_roundtrip(self, sample_df, tmp_path):
        path = str(tmp_path / "test.parquet")
        DataManager.export_parquet(sample_df, path)
        loaded = DataManager.load_parquet(path)
        pd.testing.assert_frame_equal(sample_df, loaded)

    def test_export_parquet_creates_directories(self, sample_df, tmp_path):
        path = str(tmp_path / "sub" / "dir" / "test.parquet")
        result = DataManager.export_parquet(sample_df, path)
        assert os.path.exists(result)

    def test_load_parquet_preserves_dtypes(self, sample_df, tmp_path):
        path = str(tmp_path / "test.parquet")
        DataManager.export_parquet(sample_df, path)
        loaded = DataManager.load_parquet(path)
        assert loaded["concurso"].dtype == sample_df["concurso"].dtype

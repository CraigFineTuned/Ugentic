

import pytest
import pandas as pd
from pathlib import Path

from src.ugentic.core.analysis_tool import AnalysisTool

@pytest.fixture
def analysis_tool():
    """Provides an instance of the AnalysisTool."""
    return AnalysisTool()

@pytest.fixture
def temp_dir(tmp_path: Path):
    """Provides a temporary directory for test files."""
    return tmp_path

class TestAnalysisTool:

    def test_analyze_csv_file_not_found(self, analysis_tool):
        """Tests that an error is returned for a non-existent file."""
        result = analysis_tool.analyze_csv("non_existent_path/non_existent_file.csv")
        assert "Error: File not found" in result

    def test_analyze_csv_success_mixed_types(self, analysis_tool, temp_dir):
        """Tests a successful analysis of a CSV with mixed data types."""
        file_path = temp_dir / "mixed_data.csv"
        data = {
            'age': [25, 30, 35, 40, 45],
            'department': ['HR', 'Sales', 'HR', 'Engineering', 'Sales'],
            'salary': [50000, 80000, 55000, 120000, 85000]
        }
        pd.DataFrame(data).to_csv(file_path, index=False)

        result = analysis_tool.analyze_csv(str(file_path))

        assert "Analysis of mixed_data.csv" in result
        assert "Shape: 5 rows, 3 columns" in result
        assert "Numerical Column Summary:" in result
        assert "age" in result
        assert "salary" in result
        assert "Categorical Column Value Counts" in result
        assert "department" in result
        # Note: The spacing in the string output from pandas can be inconsistent.
        # A more robust test might parse the output, but for now, we match the observed output.
        assert "HR             2" in result
        assert "Sales          2" in result

    def test_analyze_csv_directory_error(self, analysis_tool, temp_dir):
        """Tests that passing a directory path triggers the error handling."""
        # Attempting to read a directory as a CSV should raise an exception.
        result = analysis_tool.analyze_csv(str(temp_dir))
        assert "Error analyzing CSV file" in result

    def test_analyze_csv_only_numerical(self, analysis_tool, temp_dir):
        """Tests a CSV with only numerical data."""
        file_path = temp_dir / "numerical.csv"
        data = {'col1': [1, 2, 3], 'col2': [4.5, 5.5, 6.5]}
        pd.DataFrame(data).to_csv(file_path, index=False)

        result = analysis_tool.analyze_csv(str(file_path))

        assert "Numerical Column Summary:" in result
        assert "Categorical Column Value Counts" not in result

    def test_analyze_csv_only_categorical(self, analysis_tool, temp_dir):
        """Tests a CSV with only categorical data."""
        file_path = temp_dir / "categorical.csv"
        data = {'colA': ['a', 'b', 'a'], 'colB': ['x', 'y', 'y']}
        pd.DataFrame(data).to_csv(file_path, index=False)

        result = analysis_tool.analyze_csv(str(file_path))

        assert "Numerical Column Summary:" not in result
        assert "Categorical Column Value Counts" in result

    def test_analyze_csv_empty_file(self, analysis_tool, temp_dir):
        """Tests an empty CSV file."""
        file_path = temp_dir / "empty.csv"
        # Create an empty file
        file_path.touch()

        result = analysis_tool.analyze_csv(str(file_path))
        # pandas raises an EmptyDataError
        assert "Error analyzing CSV file" in result


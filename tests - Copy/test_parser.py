import sys
import importlib
from pathlib import Path
import pandas as pd
import pytest

# Add project root to the Python path to find the 'custom_parser' package
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Dynamically import the parse function created by the agent
parse = None
try:
    parser_dir = project_root / "custom_parser"
    parser_files = [f for f in parser_dir.glob("*.py") if f.name != "__init__.py"]
    if not parser_files:
        pytest.fail("No parser file found in 'custom_parser' directory.", pytrace=False)
    
    parser_file = parser_files[0]
    module_name = f"custom_parser.{parser_file.stem}"
    parser_module = importlib.import_module(module_name)
    parse = getattr(parser_module, "parse")
    print(f"\n[INFO] Successfully imported 'parse' function from {module_name}")

except (ImportError, AttributeError, IndexError) as e:
    pytest.fail(f"Could not dynamically import the parser function: {e}", pytrace=False)


# --- Test Logic Pointing to the Correct Subfolder ---

def test_parser_with_assignment_files():
    """
    Tests the parser using the exact file names and locations
    provided in the assignment.
    """
    # --- THIS IS THE FINAL CORRECTED PART ---
    # We now point to the files inside the 'data/icici' subfolder.
    pdf_path = project_root / "data" / "icici" / "icici sample.pdf"
    expected_csv_path = project_root / "data" / "icici" / "result.csv"

    # Skip the test if the required assignment files are not found
    if not pdf_path.exists():
        pytest.skip(f"Assignment PDF not found at {pdf_path}")
    if not expected_csv_path.exists():
        pytest.skip(f"Assignment CSV not found at {expected_csv_path}")

    # Load the ground truth data
    expected_df = pd.read_csv(expected_csv_path)

    # Run the dynamically imported parse function
    output_df = parse(str(pdf_path))

    # Use pandas' testing utility for a detailed comparison
    pd.testing.assert_frame_equal(output_df, expected_df)
    print("\n[SUCCESS] Parser output matches the assignment's expected CSV.")

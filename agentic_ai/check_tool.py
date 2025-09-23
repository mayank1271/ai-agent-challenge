import subprocess
from pathlib import Path

def save_parser_code(bank: str, code: str):
    """Saves the generated parser code to a file and ensures the package is valid."""
    # Define the directory and ensure it exists
    parser_dir = Path("custom_parser")
    parser_dir.mkdir(exist_ok=True)
    
    # Create the __init__.py file to make it a package, fixing ModuleNotFoundError
    (parser_dir / "__init__.py").touch()
    
    # Define the full file path for the parser
    file_path = parser_dir / f"{bank.lower()}_parser.py"
    
    # Save the code with UTF-8 encoding to prevent UnicodeEncodeError
    file_path.write_text(code, encoding="utf-8")
    print(f"[INFO] Parser written to {file_path}")

def run_test(bank: str) -> bool:
    """
    Runs the pytest suite and checks the output to determine true success.
    Returns True only if tests pass. Returns False if they fail OR are skipped.
    """
    # Command to run pytest, targeting the specific test file
    command = ["pytest", "tests/test_parser.py"]
    
    # Run the test command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    
    # --- THIS IS THE SMARTER LOGIC ---
    stdout = result.stdout
    
    # A non-zero return code from pytest always means a failure.
    if result.returncode != 0:
        print("[ERROR] Pytest failed.")
        print(f"[ERROR] STDOUT:\n{stdout}")
        print(f"[ERROR] STDERR:\n{result.stderr}")
        return False
        
    # Check the text output to see if tests were skipped.
    # If tests were skipped, it's not a true pass for the agent's purpose.
    if "skipped" in stdout.lower():
        print("[WARN] Pytest tests were skipped. Treating as failure.")
        print(f"[INFO] Pytest Output:\n{stdout}")
        return False

    # If the return code is 0 and no tests were skipped, it's a true success.
    print("[SUCCESS] Pytest passed all tests.")
    print(f"[INFO] Pytest Output:\n{stdout}")
    return True


import os
import shutil
import platform
import subprocess
import re
from typing import List, Dict, Any, Optional, Union

# --- Placeholder Core Utilities and Exceptions (for demonstration) ---
# Assuming these are available from 'core' module in a real project
class ObfuscationError(Exception):
    pass
class UnsupportedLanguageError(Exception):
    pass
class FileReadError(Exception):
    pass

class AnalyzerResults: # Mock class for demonstration
    def __init__(self):
        self.ai_suggested_native_techniques = []

class ProfileConfig: # Mock class for demonstration
    def __init__(self):
        self.obfuscation_level = "HIGH"
        self.native_techniques = []

# Mock utils module with necessary functions
class MockUtils:
    def log_info(self, message):
        print(f"[INFO] {message}")
    def log_warning(self, message):
        print(f"[WARNING] {message}")
    def log_debug(self, message):
        print(f"[DEBUG] {message}")
    def log_error(self, message):
        print(f"[ERROR] {message}")
    def execute_command(self, cmd_list, check_return_code=True):
        self.log_debug(f"Executing command (mock): {' '.join(cmd_list)}")
        # Simulate success or failure
        if "fail" in " ".join(cmd_list):
            raise subprocess.CalledProcessError(1, cmd_list, stderr=b"Mock error output\n")
        return b"Mock command output\n"
    def read_file_as_bytes(self, path):
        self.log_debug(f"Reading file as bytes (mock): {path}")
        return b"MOCK_BINARY_CONTENT"
    def write_bytes_to_file(self, path, data):
        self.log_debug(f"Writing bytes to file (mock): {path} ({len(data)} bytes)")
        with open(path, 'wb') as f: # Actually write for temp files
            f.write(data)
    def create_temp_directory(self):
        temp_dir = os.path.join(tempfile.gettempdir(), f"obf_temp_{os.urandom(4).hex()}")
        os.makedirs(temp_dir, exist_ok=True)
        self.log_debug(f"Created temp directory: {temp_dir}")
        return temp_dir
    def delete_directory(self, path, ignore_errors=False):
        self.log_debug(f"Deleting directory (mock): {path}")
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=ignore_errors)
    def copy_file(self, src, dst):
        self.log_debug(f"Copying file (mock): {src} to {dst}")
        shutil.copy2(src, dst)
    def delete_file(self, path):
        self.log_debug(f"Deleting file (mock): {path}")
        if os.path.exists(path):
            os.remove(path)
    def get_temp_dir(self):
        return tempfile.gettempdir()


utils = MockUtils() # Instance of mock utilities

# --- End Placeholder ---

class CompilationError(ObfuscationError):
    def __init__(self, tool_name: str, exit_code: int, stderr_output: str = ""):
        message = f"Compilation/linking failed during native obfuscation using '{tool_name}'. Exit code: {exit_code}."
        if stderr_output:
            message += f" Details: {stderr_output[:500]}..."
        super().__init__(message)
        self.tool_name = tool_name
        self.exit_code = exit_code
        self.stderr_output = stderr_output#

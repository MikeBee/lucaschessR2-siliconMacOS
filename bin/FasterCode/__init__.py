"""
Platform-Specific FasterCode Module Loader

This module automatically imports the correct FasterCode implementation
based on the current platform:
- Windows: Uses compiled Windows libraries
- Linux: Uses compiled Linux .so files  
- macOS (darwin): Uses pure Python stub implementation

This provides cross-platform compatibility for Lucas Chess engine functions.
Created as part of macOS compatibility implementation.

The loader uses dynamic imports to select the appropriate OS-specific
FasterCode module at runtime.
"""

# Import platform-specific FasterCode implementation
import sys
import os

# Import from OS-specific directory if available  
os_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "OS", sys.platform)
faster_code_path = os.path.join(os_dir, "FasterCode.py")

if os.path.exists(faster_code_path):
    # Load platform-specific FasterCode
    import importlib.util
    spec = importlib.util.spec_from_file_location("FasterCode", faster_code_path)
    FasterCode = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(FasterCode)
else:
    # Fallback: try compiled module
    try:
        import _fastercode as FasterCode
    except ImportError:
        # Create minimal stub
        class FasterCode:
            @staticmethod
            def bmi2():
                return False

# Expose functions at module level
for attr in dir(FasterCode):
    if not attr.startswith('_'):
        globals()[attr] = getattr(FasterCode, attr)

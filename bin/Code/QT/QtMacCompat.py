"""
macOS Qt compatibility fixes for PySide2 enum operations.
This module patches Qt enums to allow bitwise operations on macOS.
"""

import sys

def patch_qt_enums():
    """Patch Qt enums to support bitwise operations on macOS"""
    print("Applying macOS Qt compatibility patches...")
    
    from PySide2 import QtCore, QtGui
    
    # List of enum types that need patching
    enum_types = [
        QtCore.Qt.WindowType,
        QtCore.Qt.AlignmentFlag, 
        QtCore.Qt.ItemFlag,
        QtCore.Qt.TextInteractionFlag,
        QtCore.Qt.WindowFlags,
        QtCore.Qt.KeyboardModifier,
        QtGui.QPainter.RenderHint,
    ]
    
    for enum_type in enum_types:
        try:
            # Save original __or__ method
            original_or = getattr(enum_type, '__or__', None)
            if original_or:
                def make_safe_or(orig_or):
                    def safe_or(self, other):
                        try:
                            # Calculate the result as int then convert back to proper type
                            result_int = int(self) | int(other)
                            if enum_type == QtCore.Qt.WindowType:
                                return QtCore.Qt.WindowFlags(result_int)
                            elif enum_type == QtCore.Qt.AlignmentFlag:
                                return QtCore.Qt.Alignment(result_int)
                            elif enum_type == QtCore.Qt.ItemFlag:
                                return QtCore.Qt.ItemFlags(result_int)
                            elif enum_type == QtCore.Qt.TextInteractionFlag:
                                return QtCore.Qt.TextInteractionFlags(result_int)
                            elif enum_type == QtGui.QPainter.RenderHint:
                                return QtGui.QPainter.RenderHints(result_int)
                            else:
                                return result_int
                        except Exception:
                            # Fallback: return the proper type with combined int value
                            try:
                                result_int = int(self) | int(other)
                                if 'WindowType' in str(enum_type):
                                    return QtCore.Qt.WindowFlags(result_int)
                                elif 'AlignmentFlag' in str(enum_type):
                                    return QtCore.Qt.Alignment(result_int)
                                elif 'ItemFlag' in str(enum_type):
                                    return QtCore.Qt.ItemFlags(result_int)
                                elif 'TextInteractionFlag' in str(enum_type):
                                    return QtCore.Qt.TextInteractionFlags(result_int)
                                elif 'RenderHint' in str(enum_type):
                                    return QtGui.QPainter.RenderHints(result_int)
                                else:
                                    return result_int
                            except:
                                return result_int
                    return safe_or
                
                enum_type.__or__ = make_safe_or(original_or)
                enum_type.__ror__ = make_safe_or(original_or)
        except (AttributeError, TypeError):
            # Skip if enum type doesn't exist or can't be patched
            pass
    
# Apply patches when imported
if sys.platform == "darwin":
    patch_qt_enums()
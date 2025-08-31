"""
macOS Compatibility Stub Module for FasterCode

This module provides stub implementations of all functions and classes
that would normally be provided by compiled C extensions (FasterCode).
On macOS, these compiled extensions are not available, so we provide
basic stub implementations that allow the application to run.

Key components:
- Chess engine interface functions (bmi2, pv_xpv, etc.)
- Board class for chess position handling  
- Search and evaluation function stubs
- Polyglot book interface stubs

This is part of the macOS compatibility implementation for Lucas Chess.
Created as part of macOS porting effort to replace compiled .so files.
"""

def bmi2():
    """Return False - BMI2 detection stub for macOS"""
    return False

def get_captures(fen, si_mb):
    """Stub for get_captures function"""
    return []

def set_fen(fen):
    """Stub for set_fen function"""
    pass

def ischeck():
    """Stub for ischeck function"""
    return False

def get_exmoves():
    """Stub for get_exmoves function"""
    return []

def make_move(move):
    """Stub for make_move function"""
    pass

class InfoMove:
    """Stub class for InfoMove"""
    def __init__(self):
        pass
    
    def xfrom(self):
        return "a1"
    
    def xto(self):
        return "a2"
    
    def promotion(self):
        return ""
    
    def move(self):
        return "a1a2"
    
    def check(self):
        return False
    
    def mate(self):
        return False
    
    def capture(self):
        return False

# Additional function stubs
def pv_xpv(pv):
    """Convert PV format - stub"""
    return ""

def xpv_pv(xpv):
    """Convert XPV format - stub"""  
    return ""

def make_pv(fen, moves):
    """Make PV from moves - stub"""
    return ""

def get_fen():
    """Get FEN string - stub"""
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def fen_fenm2(fen):
    """Convert FEN format - stub"""
    return fen

def num_move(move):
    """Get move number - stub"""
    return 0

def move_num(num):
    """Convert move number - stub"""
    return ""

def pos_a1(pos):
    """Convert position to a1 format - stub"""
    return "a1"

def a1_pos(a1):
    """Convert a1 format to position - stub"""  
    return 0

def xpv_lipv(xpv):
    """Convert XPV to LIPV - stub"""
    return []

def xpv_pgn(xpv, dic=None):
    """Convert XPV to PGN - stub"""
    return ""

def lipv_pgn(lipv, dic=None):
    """Convert LIPV to PGN - stub"""
    return ""

class PGNreader:
    """PGN reader stub class"""
    def __init__(self, file_path):
        self.file_path = file_path
    
    def lee(self):
        """Read next game - stub"""
        return None
    
    def close(self):
        """Close reader - stub"""
        pass

class DBgamesST:
    """Database games stub class"""
    def __init__(self, file_path):
        self.file_path = file_path
    
    def close(self):
        """Close database - stub"""
        pass
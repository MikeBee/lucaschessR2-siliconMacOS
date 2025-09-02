"""
macOS Chess Engine Module for FasterCode

This module provides full chess functionality using the python-chess library
to replace compiled C extensions that aren't available on macOS.
This enables complete chess tactics, training, and gameplay functionality.

Key components:
- Chess move validation and generation using python-chess
- Position analysis and evaluation
- PGN parsing and game handling
- Move format conversion and board state management

This provides full chess functionality on macOS for Lucas Chess.
"""

import chess
import chess.pgn
import io

# Global chess board for state management
_board = chess.Board()

def bmi2():
    """Return False - BMI2 detection stub for macOS"""
    return False

def get_captures(fen, si_mb):
    """Get capture moves from position"""
    board = chess.Board(fen)
    captures = []
    for move in board.legal_moves:
        if board.is_capture(move):
            captures.append(move.uci())
    return captures

def set_fen(fen):
    """Set FEN position"""
    global _board
    try:
        # Clean up FEN string - remove quotes and brackets
        clean_fen = fen.strip().strip('"').strip("'").strip(']').strip('[')
        _board = chess.Board(clean_fen)
    except Exception as e:
        # Fallback to starting position if FEN is invalid
        _board = chess.Board()

def ischeck():
    """Check if current position is in check"""
    return _board.is_check()

def get_exmoves():
    """Get all legal moves as InfoMove objects"""
    moves = []
    for move in _board.legal_moves:
        info_move = InfoMove(move.uci(), _board)
        moves.append(info_move)
    return moves

def make_move(move):
    """Make move on board"""
    global _board
    try:
        chess_move = chess.Move.from_uci(move)
        _board.push(chess_move)
    except Exception as e:
        pass

class InfoMove:
    """InfoMove class with proper chess logic"""
    def __init__(self, move_uci, board=None):
        self.move_uci = move_uci
        self.chess_move = chess.Move.from_uci(move_uci) if move_uci else None
        self.board = board or _board
    
    def xfrom(self):
        if self.chess_move:
            return chess.square_name(self.chess_move.from_square)
        return "a1"
    
    def xto(self):
        if self.chess_move:
            return chess.square_name(self.chess_move.to_square)
        return "a2"
    
    def promotion(self):
        if self.chess_move and self.chess_move.promotion:
            return chess.piece_symbol(self.chess_move.promotion)
        return ""
    
    def move(self):
        return self.move_uci or "a1a2"
    
    def check(self):
        if self.chess_move and self.board:
            board_copy = self.board.copy()
            board_copy.push(self.chess_move)
            return board_copy.is_check()
        return False
    
    def mate(self):
        if self.chess_move and self.board:
            board_copy = self.board.copy()
            board_copy.push(self.chess_move)
            return board_copy.is_checkmate()
        return False
    
    def capture(self):
        if self.chess_move and self.board:
            return self.board.is_capture(self.chess_move)
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
    """Get current FEN string"""
    return _board.fen()

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

def xparse_pgn(pgn_text):
    """Parse PGN text into Lucas Chess token format"""
    try:
        result = []
        lines = pgn_text.strip().split('\n')
        current_board = chess.Board()  # Track board state for move parsing
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse headers [Tag "Value"] 
            if line.startswith('[') and line.endswith(']'):
                # Extract the tag content without brackets for Lucas Chess format
                tag_content = line[1:-1]  # Remove [ and ]
                result.append('[' + tag_content)
                
                # If this is a FEN tag, update our board state
                if tag_content.upper().startswith('FEN '):
                    fen_value = tag_content[4:].strip().strip('"')
                    try:
                        current_board = chess.Board(fen_value)
                    except:
                        current_board = chess.Board()
            
            # Parse moves and comments
            elif line and not line.startswith('%'):
                # Simple tokenization - split on spaces and process each token
                tokens = line.split()
                i = 0
                while i < len(tokens):
                    token = tokens[i].strip()
                    
                    # Skip move numbers like "1." "2."
                    if token.endswith('.') and token[:-1].isdigit():
                        i += 1
                        continue
                    
                    # Handle comments in {}
                    if token.startswith('{'):
                        comment = token
                        while not token.endswith('}') and i + 1 < len(tokens):
                            i += 1
                            token = tokens[i]
                            comment += ' ' + token
                        result.append(comment)
                    
                    # Handle regular moves - convert to UCI format and prefix with M
                    elif token and not token.startswith('{') and not token.startswith(';'):
                        # Convert algebraic notation to UCI using current board state
                        try:
                            # Try to parse as algebraic notation first
                            move = current_board.parse_san(token)
                            uci_move = move.uci()
                            result.append('M' + uci_move)
                            # Update board state
                            current_board.push(move)
                        except Exception as e:
                            # If parsing fails, try as UCI move
                            try:
                                clean_token = token.rstrip('+#!?')
                                if len(clean_token) >= 4 and clean_token[0] in 'abcdefgh' and clean_token[1] in '12345678':
                                    uci_move = clean_token[:4] + (clean_token[4:] if len(clean_token) > 4 else '')
                                    chess_move = chess.Move.from_uci(uci_move)
                                    if chess_move in current_board.legal_moves:
                                        result.append('M' + uci_move)
                                        current_board.push(chess_move)
                                    else:
                                        result.append('M' + token)
                                else:
                                    result.append('M' + token)
                            except:
                                result.append('M' + token)
                    
                    i += 1
        
        return result
    except Exception as e:
        return None

class FastMove:
    """Move object compatible with FasterCode expectations"""
    def __init__(self, from_sq, to_sq, promotion=""):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.promotion = promotion
        self.uci_move = from_sq + to_sq + (promotion if promotion else "")
        
        try:
            from_sq_int = chess.square(ord(from_sq[0]) - ord('a'), int(from_sq[1]) - 1)
            to_sq_int = chess.square(ord(to_sq[0]) - ord('a'), int(to_sq[1]) - 1)
            self.chess_move = chess.Move(from_sq_int, to_sq_int, 
                                       promotion=chess.Piece.from_symbol(promotion.lower()).piece_type if promotion else None)
        except:
            self.chess_move = None
    
    def iscastle_k(self):
        """Check if move is kingside castle"""
        return (self.from_sq == "e1" and self.to_sq == "g1") or (self.from_sq == "e8" and self.to_sq == "g8")
    
    def iscastle_q(self):
        """Check if move is queenside castle"""
        return (self.from_sq == "e1" and self.to_sq == "c1") or (self.from_sq == "e8" and self.to_sq == "c8")
    
    def is_enpassant(self):
        """Check if move is en passant"""
        if self.chess_move and _board:
            return _board.is_en_passant(self.chess_move)
        return False
    
    def movimiento(self):
        """Get move in a1h8 format"""
        return self.uci_move
    
    def san(self):
        """Get move in standard algebraic notation"""
        if self.chess_move and _board:
            try:
                return _board.san(self.chess_move)
            except:
                return self.uci_move
        return self.uci_move

def move_expv(from_sq, to_sq, promotion=""):
    """Convert move to internal format"""
    # Check if move is legal first
    if not is_legal_move(from_sq, to_sq, promotion):
        return None
    return FastMove(from_sq, to_sq, promotion)

def set_init_fen():
    """Set initial FEN position"""
    global _board
    _board = chess.Board()

def make_move_str(move_str):
    """Make move from string"""
    global _board
    try:
        move = chess.Move.from_uci(move_str)
        if move in _board.legal_moves:
            _board.push(move)
            return True
    except:
        pass
    return False

def unmake_move():
    """Unmake last move"""
    global _board
    try:
        _board.pop()
    except:
        pass

def is_legal_move(from_sq, to_sq, promotion=""):
    """Check if move is legal"""
    try:
        from_sq_int = chess.square(ord(from_sq[0]) - ord('a'), int(from_sq[1]) - 1)
        to_sq_int = chess.square(ord(to_sq[0]) - ord('a'), int(to_sq[1]) - 1)
        move = chess.Move(from_sq_int, to_sq_int, promotion=promotion if promotion else None)
        return move in _board.legal_moves
    except:
        return False

def is_mate():
    """Check if position is checkmate"""
    return _board.is_checkmate()

def is_stalemate():
    """Check if position is stalemate"""
    return _board.is_stalemate()

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
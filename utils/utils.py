import pandas as pd
import chess


def get_fen_list(moves : str)->list:
    """Transform a string of moves in SAN into a list of FEN board positions for each of the string's moves.

    Args:
        moves (str): string containing the moves in Standart Algebraic Notation separated by an empty space.

    Returns:
        fen_list (list str): list of the Forsty-Edwards Notation of the current board position of each turn.
    """
    # defines a new board in the starting position
    board = chess.Board()
    # creates a list of FEN's
    fen_list = [board.fen()]
    # transform the string in a list with the moves
    moves = moves.split(" ")

    for mv in moves:
        # aplica o movimento ao tabuleiro
        board.push_san(mv)
        fen_list.append(board.fen())
    
    return fen_list
    

def get_fen_dict(fen: str)->dict:
    placement, active_color, castling, en_passant, halfmove_clock, fullmove_clock = fen.split(" ")
    return {
        "placement":     placement,
        "active_color":  active_color,
        "castling":      castling,
        "en_passant":    en_passant,
        "halfmove_clock":halfmove_clock,
        "fullmove_clock": fullmove_clock
    }


def get_turn_df(fen: str)->pd.DataFrame:    
    """Transforms a FEN str into a dataframe containing a turn's piece, piece color, x position (1=a, ... 8=h) and y position (1, ..., 8)"""
    
    # get only the placement part of the fen string (e.g. rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR)
    fen_dict = get_fen_dict(fen)
    placements = fen_dict['placement'].split("/")

    piece_list = []
    # iterates over the rows
    for i in range(len(placements)):
        row = placements[i]
        # iterates over the columns
        for j in range(len(row)):
            col = row[j]
            if not col.isdigit():
                # the turn will be added later
                game_id = None
                turn = None
                piece = col
                if col.islower():
                    color = 'w'
                else:
                    color = 'b'
                x = i + 1
                y = j + 1
                piece_list.append([turn, piece, color, x, y])
    df = pd.DataFrame(piece_list, columns=['turn', 'piece', 'color', 'x', 'y'])
    return df


def get_game_df(san : str):
    fen_list = get_fen_list(san)
    df_game = pd.DataFrame(columns=['turn', 'piece', 'color', 'x', 'y'])
    for i in range(len(fen_list)):
        turn_list = get_turn_df(fen_list[i]).values
        for turn in turn_list:
            turn[0] = i
            turn = pd.Series(turn, index = df_game.columns)
            df_game = df_game.append(turn, ignore_index=True)
    return df_game


def add_images(game_df : pd.DataFrame)->pd.DataFrame:
    df_icons = {
        'r': 'icons/wr.svg', 'R': 'icons/br.svg',
        'n': 'icons/wn.svg', 'N': 'icons/bn.svg',
        'b': 'icons/wb.svg', 'B': 'icons/bb.svg',
        'q': 'icons/wq.svg', 'Q': 'icons/bq.svg',
        'k': 'icons/wk.svg', 'K': 'icons/bk.svg',
        'p': 'icons/wp.svg', 'P': 'icons/bp.svg'
    }
    icons = []
    for piece in game_df['piece']:
        icons.append(df_icons[piece])
    game_df['icon'] = icons
    return game_df

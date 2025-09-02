from Code.Base import Game, Position


class FNSLine:
    def __init__(self, line):
        self.line = line  # Se usa en ManagerEntPos
        self.position = Position.Position()
        self.label = ""
        self.game_obj = None
        self.game_original = None
        self.read(line)

    def read(self, line):
        li = line.split("|")
        self.position.read_fen(li[0])
        nli = len(li)
        if nli > 1:
            self.label = li[1]

            if nli > 2:
                solucion = li[2]
                pgn_text = '[FEN "%s"]\n%s' % (self.position.fen(), solucion)
                print(f"DEBUG FNSLine calling pgn_game with: {repr(pgn_text)}")
                ok, game_obj = Game.pgn_game(pgn_text)
                print(f"DEBUG FNSLine pgn_game result: ok={ok}, game_obj={game_obj}")
                if ok:
                    self.game_obj = game_obj
                    print(f"DEBUG FNSLine game_obj set successfully")

                    if nli > 3:
                        txt = li[3].replace("]", "]\n").replace(" [", "[")
                        ok, game_original = Game.pgn_game(txt)
                        if ok:
                            ok = False
                            for n in range(len(game_original) - 1, -1, -1):
                                move = game_original.move(n)
                                if move.position == self.position:
                                    ok = True
                                    if n + 1 != len(game_original):
                                        game_original.li_moves = game_original.li_moves[: n + 1]
                                    break
                        if ok:
                            self.game_original = game_original
                            self.game_original.set_unknown()

    def with_game_original(self):
        return self.game_original is not None

    def with_solution(self):
        return self.game_obj is not None

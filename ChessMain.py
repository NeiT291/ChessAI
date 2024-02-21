'''là tệp chính điều khiển, chịu trách nghiệm xử lí thông tin đầu vào của người dùng và thông tin trạng thái của trò chơi'''
import pygame as p
import ChessEngine
import SmartMoveFinder
p.display.set_caption('CHESS')
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["bp", "bR", "bN", "bB", "bQ", "bK", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE, SQ_SIZE))
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    validMovies = gs.getValidMoves()
    moveMade = False  # biến cờ khi thực hiện một nước đi

    loadImages()  # chỉ làm điều này một lần, trước vòng lặp while

    running = True
    sqSelected = ()
    playerClicks = []
    playerOne = True
    playerTwo = False
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # trình xử lý chuột
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanTurn:
                    location = p.mouse.get_pos()  # (x, y) vị trí chuột
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):  # người dùng đã nhấp vào cùng một hình vuông hai lần
                        sqSelected = ()  # bỏ chọn
                        playerClicks = []  # xóa số lần nhấp chuột của người chơi
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # nối thêm cho cả lần nhấp thứ 1 và thứ 2
                    if len(playerClicks) == 2:  # sau lần nhấp thứ 2
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMovies)):
                            if move == validMovies[i]:
                                gs.makeMove(move)
                                moveMade = True
                                sqSelected = () #đặt lại số lần nhấp chuột của người dùng
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # sử lý key
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # hoàn tác khi nhấn 'z'
                    gs.undoMove()
                    moveMade = True
        # AI move finder
        if not humanTurn:
            AImove = SmartMoveFinder.findBestMove(gs, validMovies)
            if AImove is None:
                AImove = SmartMoveFinder.findRandomMove(validMovies)
            gs.makeMove(AImove)
            moveMade = True

        if moveMade:
            validMovies = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

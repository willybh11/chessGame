# do not run this file
import turtle
class Graphics():

    class Draw():

        def __init__(self, T):
            self.T = T

        def box(self):
            self.coords = self.T.pos()
            self.T.goto(self.coords[0] - 30, self.coords[1] - 24)
            self.T.seth(0)
            self.T.pd()
            self.T.begin_fill()
            for i in range(2):
                self.T.fd(60)
                self.T.rt(90)
                self.T.fd(11)
                self.T.rt(90)
            self.T.end_fill()
            self.T.pu()

        def king(self):
            self.box()
            self.T.goto(self.coords[0] + 13, self.coords[1] + 9)
            self.T.seth(90)
            self.T.pd()
            self.T.begin_fill()
            self.T.circle(13)
            self.T.goto(self.coords[0] - 2, self.coords[1] + 21)
            self.T.seth(360)
            for i in range(4):
                self.T.fd(4)
                self.T.lt(90)
                self.T.fd(7)
                self.T.rt(90)
                self.T.fd(7)
                self.T.lt(90)
            self.T.end_fill()

        def queen(self):
            self.box()
            self.T.goto(self.coords[0] + 13, self.coords[1] + 9)
            self.T.seth(90)
            self.T.pd()
            self.T.begin_fill()
            self.T.circle(13)
            self.T.end_fill()
            self.T.seth(360)
            for coords in [(self.coords[0] - 20, self.coords[1] + 24),
                           (self.coords[0] - 8, self.coords[1] + 29),
                           (self.coords[0] + 8, self.coords[1] + 29),
                           (self.coords[0] + 20, self.coords[1] + 24)]:
                self.T.pu()
                self.T.goto(coords)
                self.T.begin_fill()
                self.T.pd()
                self.T.circle(5)
                self.T.end_fill()

        def bishop(self):
            self.box()
            self.T.goto(self.coords[0], self.coords[1] + 35)
            self.T.pd()
            self.T.begin_fill()
            for heading in [250, 290, 70, 110]:
                self.T.seth(heading)
                self.T.fd(25)
            self.T.end_fill()

        def knight(self):
            self.box()
            self.T.goto(self.coords[0] + 2, self.coords[1] + 5)
            self.T.begin_fill()
            self.T.pd()
            self.T.circle(15, 180)
            self.T.end_fill()
            self.T.pu()
            self.T.goto(self.coords[0] - 2, self.coords[1] + 25)
            self.T.seth(180)
            self.T.begin_fill()
            self.T.circle(20, 180)
            self.T.end_fill()

        def pawn(self):
            self.box()
            self.T.seth(90)
            self.T.goto(self.coords[0] + 15, self.coords[1] + 20)
            self.T.begin_fill()
            self.T.pd()
            self.T.circle(15)
            self.T.end_fill()

        def rook(self):
            self.box()
            self.T.goto(self.coords[0] - 15, self.coords[1] + 17)
            self.T.begin_fill()
            self.T.pd()
            self.T.fd(30)
            self.T.lt(90)
            self.T.fd(15)
            for i in range(2):
                self.T.lt(90)
                self.T.fd(6)
                self.T.lt(90)
                self.T.fd(4)
                self.T.rt(90)
                self.T.fd(6)
                self.T.rt(90)
                self.T.fd(4)
            self.T.lt(90)
            self.T.fd(6)
            self.T.lt(90)
            self.T.fd(15)
            self.T.seth(270)
            self.T.circle(15, 180)
            self.T.end_fill()

    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(724, 724)
        self.window.bgpic("background.png")
        self.window.tracer(0, 0)
        self.T = turtle.Turtle()
        self.T.speed(10)
        self.T.ht()
        self.write = self.Draw(self.T)
        self.draw = {"P": self.write.pawn,
                     "R": self.write.rook,
                     "K": self.write.king,
                     "Q": self.write.queen,
                     "B": self.write.bishop,
                     "N": self.write.knight}

    def mouseCoords(x,y):
        self.board.clickCoords = (x,y) 
        print "coords reCOORDed"

    def turtleUpdate(self,grid):
        self.T.clear()
        for row in range(8):
            for col in range(8):
                square = grid[col][row]
                coords = (row * 90 - 315,  col * 90 - 315)
                self.T.pu()
                self.T.goto(coords)
                color = "white" if "w" in square else "black"
                self.T.fillcolor(color)
                self.T.pencolor(color)
                try:
                    self.draw[square[0]]()
                except IndexError:
                    pass  # empty square
        turtle.update()

if __name__ == "__main__":
    print "you werent supposed to do that"
import javax.swing.*;
import java.awt.Graphics;
import java.awt.Color;

public class JavaGraphics extends JFrame
{

   public void paint(Graphics g)
   {
      int row,col,x,y;

      for ( row = 0;  row < 9;  row++ )
      {
         for ( col = 0;  col < 8;  col++)
         {
            x = col * 100;
            y = row * 100;
            if ((row % 2) == (col % 2)) {
               g.setColor(Color.WHITE);
            } else {
               g.setColor(Color.BLACK);
            }

            g.fillRect(x, y, 100, 100);
         }
      }
   }

   public static void main(String args[]) {
        JavaGraphics board = new JavaGraphics();
        board.setTitle("CheckerBoard");
        board.setSize(800, 800);
        board.setDefaultCloseOperation(EXIT_ON_CLOSE);
        board.setVisible(true);
    }
}

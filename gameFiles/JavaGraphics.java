/*  worked on by Leo Kastenberg
 *  Java seems like a cool language
 *  I am worried for when I have to actually weave this into the python and C code
 */

import javax.swing.*;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.*;

import javax.swing.JPanel;
import javax.imageio.ImageIO;

public class JavaGraphics extends JFrame
{

   public void paint(Graphics g)
   {
      try {
        int row,col,x,y;
        BufferedImage pawnImage;
        pawnImage = ImageIO.read(getClass().getResourceAsStream("/pawnTest.jpg"));

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
              g.drawImage(pawnImage,x,y,50,50,null);

           }
        }
      } catch(IOException e) { e.printStackTrace(); }
   }

   public static void main(String[] args) {
        JavaGraphics board = new JavaGraphics();
        board.setTitle("ChessBoard");
        board.setSize(800, 800);
        board.setDefaultCloseOperation(EXIT_ON_CLOSE);
        board.setVisible(true);

        Screen screen = new Screen();

    }

}

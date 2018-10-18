#include <windows.h>
#include <cstdio>
#include "GL/glut.h"
#include "GL/glext.h"
#include "GL/gl.h"
#include "GL/glu.h"
#include <math.h>
#include <iostream>
#include <fstream>
using namespace std;

typedef struct Piece {
    GLint numOfPoint;
    GLdouble* _x;
    GLdouble* _y;
} Piece;


int numOfSector;
Piece *pieces;

void loadFile (string name);


void drawDot( GLint x, GLint y )  {

}


void myInit( void )  {
  glClearColor( 1.0, 1.0, 1.0, 0.0 );
  glColor3f( 0.0, 0.0, 0.0 );
  glPointSize( 1.0 );
  glMatrixMode( GL_PROJECTION );
  glLoadIdentity( );
  gluOrtho2D( 0.0, 700.0, 0.0, 600.0 );

}


void thuvh_display2 ( void ){
     glClear (GL_COLOR_BUFFER_BIT );


     for (int i = 0; i < numOfSector; i++){
              glBegin (GL_LINE_STRIP);
         int n = pieces[i].numOfPoint;
         for (int j = 0; j < n; j++){
             glVertex2f (pieces[i]._x[j], pieces[i]._y[j]);
         }
              glEnd ();
     }

     glFlush ();
}

void thuvh_display ( Piece p ){

  glBegin (GL_LINE_STRIP);
  int n = p.numOfPoint;

  for (int i = 0; i < n; i++){
      glVertex2f (p._x[i], p._y[i]);
  }

  glEnd();

}



void myDisplay( void )  {
     
//  glClear( GL_COLOR_BUFFER_BIT );
//  glBegin (GL_LINE_STRIP);
//  glVertex2i (100, 50);
//  glVertex2i (100, 130);
//  glVertex2i (150, 130);
//  glVertex2i (100, 50);
  for (int i = 0; i < numOfSector; i++){
      thuvh_display (pieces[i]);
  }
//  glEnd();

//  glFlush();
}

void tillThuvh ( void ){
     glClear ( GL_COLOR_BUFFER_BIT );
     for (int i = 0; i < 5; i++){
         for (int j = 0; j < 5; j++){
             glViewport (i * 70, j * 60, 70, 60);

             myDisplay ();
         }
     }

     glFlush ();
}


int main( int argc, char *argv[] )  {

  loadFile("dinosaur.dat");
  
  glutInit( &argc, argv );
 
  glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB );
  
  glutInitWindowSize( 640, 480 );
 
  glutInitWindowPosition( 100, 150 );
  
  glutCreateWindow( "Lab5" );

 // glutDisplayFunc( myDisplay );
  //glutDisplayFunc( tillThuvh );
  glutDisplayFunc (thuvh_display2);
  
  myInit( );
  
  glutMainLoop( );


}


void loadFile (string name){
     ifstream fi (name.c_str ());

     fi >> numOfSector;
     pieces = new Piece [numOfSector];

     for (int i = 0; i < numOfSector; i++){
         int tmp = 0;
         fi >> tmp;
         pieces[i].numOfPoint = (GLint)tmp;
         pieces[i]._x = new GLdouble[tmp];
         pieces[i]._y = new GLdouble[tmp];

         for (int j = 0; j < tmp; j++){
             double a = 0.0;
             double b = 0.0;

             fi >> a;
             fi >> b;

             pieces[i]._x[j] = a;
             pieces[i]._y[j] = b;
         }
     }

     fi.close ();
}

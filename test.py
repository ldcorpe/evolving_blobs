import time
import curses
import random as r



def pbar(window):
   for j in range(10):
      speed=[r.gauss(0,1),r.gauss(0,1),r.gauss(0,1)]
      sizes=[r.gauss(0,10),r.gauss(0,10),r.gauss(0,10)]
      colour=['red','blue','yellow']
       "blob  |  size | colour  | speed  ")
      window.addstr(1, 10, "---------------------------------")
      for i in range(len(speed)):
         window.addstr(2*i+1, 10, "%.2f | %.2f  | %s  |  %.2f "%(i,sizes[i],colour[i],speed[i]))
      window.refresh()
      time.sleep(2)

curses.wrapper(pbar)

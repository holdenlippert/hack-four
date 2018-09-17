#!/usr/bin/env python
import game

try:
    game.Game().mainloop()

except Exception as e:
    print "Got exception", e

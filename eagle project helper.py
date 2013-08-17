#!/usr/bin/env python2

import sys
import os
from subprocess import call


# Recursively generate images in given directory
def genImages(path):
  if (os.path.isdir(path)):
    for name in os.listdir(path):
      path_plus_name = os.path.join(path, name)
      if os.path.isdir(path_plus_name):
        # Directory found
        genImages(path_plus_name)
      else:
        if ".brd" in name:
          # Export Board Image Preview
          if os.path.isfile(os.path.join(path, "board.png")):
            png_mtime = os.path.getmtime(os.path.join(path, "board.png"))
            brd_mtime = os.path.getmtime(path_plus_name)

            if (brd_mtime > png_mtime):
              print " Regenerating board.png for", name
              call(["rm", os.path.join(path, "board.png")])
              call(["eagle", "-C", "ratsnest; export image '" + os.path.join(path, "board.png") + "' 600; quit;", path_plus_name])
          else:
            print " Generating board.png for", name
            call(["eagle", "-C", "ratsnest; export image '" + os.path.join(path, "board.png") + "' 600; quit;", path_plus_name])


        elif ".sch" in name:
          # Export Schematic Image Preview
          if os.path.isfile(os.path.join(path, "schematic.png")):
            png_mtime = os.path.getmtime(os.path.join(path, "schematic.png"))
            sch_mtime = os.path.getmtime(path_plus_name)

            if (sch_mtime > png_mtime):
              print " Regenerating board.png for", name
              call(["rm", os.path.join(path, "schematic.png")])
              call(["eagle", "-C", "export image '" + os.path.join(path, "schematic.png") + "' 600; quit;", path_plus_name])
          else:
            print " Generating schematic.png for", name
            call(["eagle", "-C", "export image '" + os.path.join(path, "schematic.png") + "' 600; quit;", path_plus_name])


        elif ".dri" in name:
          # Collect Gerber files into .zip
          if os.path.exists(os.path.splitext(name)[0] + ".dri"):
            print " Generating Archive for", os.path.splitext(name)[0][0:-7]
            os.chdir(path)
            call(["rm *.zip"], shell=True)
            call(["zip '" + os.path.splitext(name)[0][0:-7] + ".zip' *.ger *.dri *.xln"], shell=True)
            call(["rm *.ger *.gpi *.dri *.xln *\#*"], shell=True)



# CMD Args are directories
for arg in sys.argv:
  genImages(arg)


#!/usr/bin/env python2

import sys
import os
from subprocess import call

# TODO
# Parse Upload Path


uploadDir = "~/Projects/CAD/Eagle/toUpload/"

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
              call(["eagle", "-C", "ratsnest; export image '" + os.path.join(path, "board.png") + "' 300; quit;", path_plus_name])
          else:
            print " Generating board.png for", name
            call(["eagle", "-C", "ratsnest; export image '" + os.path.join(path, "board.png") + "' 300; quit;", path_plus_name])

          call(["rm *.b\#*"], shell=True)


        elif ".sch" in name:
          # Export Schematic Image Preview
          if os.path.isfile(os.path.join(path, "schematic.png")):
            png_mtime = os.path.getmtime(os.path.join(path, "schematic.png"))
            sch_mtime = os.path.getmtime(path_plus_name)

            if (sch_mtime > png_mtime):
              print " Regenerating board.png for", name
              call(["rm", os.path.join(path, "schematic.png")])
              call(["eagle", "-C", "export image '" + os.path.join(path, "schematic.png") + "' 300; quit;", path_plus_name])
          else:
            print " Generating schematic.png for", name
            call(["eagle", "-C", "export image '" + os.path.join(path, "schematic.png") + "' 300; quit;", path_plus_name])

          call(["rm *.s\#*"], shell=True)


        elif ".dri" in name:
          # Collect Gerber files into .zip
          if os.path.exists(os.path.join(path, name[:-4] + ".dri")):
            if os.path.exists(os.path.join(uploadDir, name[:-11] + ".zip")):
              print " Warning. Duplicate project found for", name[:-11]
            else:
              print " Generating Archive for", name[:-11]
              os.chdir(path)
              call(["rm *.zip"], shell=True)
              call(["zip '" + name[:-11] + ".zip' *.ger *.dri *.xln"], shell=True)
              call(["rm *.b\#* *.s\#*"], shell=True)
              call(["rm *.ger *.gpi *.dri *.xln"], shell=True)
              call(["mv *.zip "+ uploadDir], shell=True)


# CMD Args are directories
for arg in sys.argv:
  genImages(arg)


import json
import processXML
import matplotlib.pyplot as plt
import sys, ReadTextLines0
import timeit
import VD2
import os
assert(len(sys.argv)==5)
def main():
  outfolder, imagename, xmlname, outname = sys.argv[1:5]
  outname = outfolder + '/' + outname.split('/')[-1]
  if os.path.isfile(outname):
    exit()
  '''
  *** Step 0: Fetch Strips from XML ***'''
  scrapedname = xmlname+'.scraped.txt'
  ReadTextLines0.readxml(xmlname,imagename,scrapedname)
  vdclass = VD2.VerticalDominance()
  vdclass.parse(scrapedname)
  vdclass.getstrips()
  '''
  *** Step 1: Write to IntermediateFormat: *** '''
  anns = []
  for j, (y,x,Y,X) in enumerate(vdclass.coors):
     anns.append({"class": "title",
                  "id": j,
                  "height": Y-y,
                  "type": "rect",
                  "width": X-x,
                  "x": x,
                  "y": y})
  intermediate_format = [{
          "annotations": anns,
        }]

  with open(outname, 'w') as f:
    json.dump(intermediate_format, f, indent=4)
if __name__=='__main__':
  main()
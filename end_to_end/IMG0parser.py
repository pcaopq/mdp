# python ImgSeg.py ../../output/segment ../../images/0003.jpg ../../images/0003.xml ../../images/0003.textblocksBS.py.result.json
import os, sys
def main():
  outfolder, imgname, xmlname, outname = sys.argv[1:5]
  outname = outfolder + '/' + outname.split('/')[-1]
  if os.path.isfile(outname):
  	exit()
  os.system('./ImgSeg_parser %s %s'%(imgname, outname))

if __name__=='__main__':
  main()

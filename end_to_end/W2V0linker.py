import os, sys
import json
import VD2, ReadTextLines0
import string
import math
import timeit

GloVe = {}
def cos_distance(coors1, coors2):
	nomin = dot(coors1, coors2)  
	denomin = math.sqrt(dot(coors1, coors1))*math.sqrt(dot(coors2, coors2))
	return 1 - nomin/denomin
def dot(coors1, coors2):
	return sum([i[0]*i[1] for i in zip(coors1, coors2)])	
def explain(lines):
  if(len(lines) == 51):
    text = lines[0]
    coor = lines[1:]
    yield text, coor 
def check_in(a, b):  
	#xmin, ymin, xmax, ymax
	if (a[0] >= b[0]) and (a[1] >= b[1]) and (a[2] <= b[2]) and (a[3]<=b[3]):
		return True  
	else: return False
def get_article_vector(word_vectors):
	article_vector = [0]*50; effect = 0
	word_vectors = [i[1] for i in word_vectors]
	with open('glove.6B.50d.txt','r') as f:
		for lines in f.read().split('\n'):
		 	for seg, coor in explain(lines.split(' ')):
				GloVe[seg] = map(float, coor)
	f.close()	
	for word in word_vectors:
		word = [j for j in word.lower() if j not in string.punctuation]
		word = ''.join(word)
		if word not in GloVe.keys(): 
			# print word+' is not found!'
			continue
		article_vector = [j[0]+j[1] for j in zip(article_vector, GloVe[word])]
		effect += 1
	if effect ==0: return None
	article_vector = [i*1.0/effect for i in article_vector]
	return article_vector
def Merge(a, b):
	#xmin ymin xmax ymax
	blk = []
	blk.append(min(a[0], b[0]))
	blk.append(min(a[1], b[1]))
	blk.append(max(a[2], b[2]))
	blk.append(max(a[3], b[3]))
	blk.append(a[4])
	blk.append(a[5])
	return blk
def main():
	# os.system('cp /Users/Bruce/Documents/xcode/ImgSeg/build/Debug/0005.json /Users/Bruce/Documents/GloVe/end_to_end_precise')
	# start_time = timeit.default_timer()
	outfolder, outname, infolder,inname = sys.argv[1:][:4]
	filename = '/'.join(inname.split('/')[0:3])+'/'+inname.split('/')[3].split('.')[0]
	outname = outfolder+'/'+outname.split('/')[-1]
	inname = infolder+'/'+inname.split('/')[-1]
	if os.path.isfile(outname):
		exit()
	# filename = sys.argv[1].split('.')[0]
	with open(inname) as f:
		img_blks = json.load(f)
		f.close()
	tmap = ReadTextLines0.readxml(filename+'.xml',filename+'.jpg', filename+'.xml'+'.scraped.txt')
	blocks = []
	for blk in img_blks[0][u'annotations']:
		blocks.append([blk['x'], blk['y'], blk['x']+blk['width'], blk['y']+blk['height'], blk['class'], blk['id']])
	link = [[] for i in range(len(blocks))]
	for i in tmap.keys():
		find = False
		for index, j in enumerate(blocks):
			if check_in(i, j): find = True; break
		if find: link[index].append([i, tmap[i]])
	article_vectors = []
	for ii, k in enumerate(link):
		if len(k) == 0: continue
		article_vector = get_article_vector(k)
		if article_vector is None: continue	
		else: article_vectors.append(article_vector)
	CosDMat = [[0 for i in range(len(article_vectors))] for j in range(len(article_vectors))]
	Mergelist = {i:[] for i in range(len(article_vectors))}
	threshold = 0.5
	for i in range(len(article_vectors)):
		for j in range(i+1, len(article_vectors)):
			CosDMat[i][j] = cos_distance(article_vectors[i], article_vectors[j])
			if (CosDMat[i][j]>0) and (CosDMat[i][j]<threshold):
				Mergelist[i].append(j)
	# print Mergelist
	for i in range(len(Mergelist))[::-1]:
		if len(Mergelist[i])==0: continue
		for j in Mergelist[i]:
			if(blocks[i][4] == blocks[j][4]):
				blocks[i] = Merge(blocks[i], blocks[j])
				del blocks[j]
	anns = []
	# with open('output.txt','w') as f:
	# 	for i in blocks:
	# 		f.write('%f %f %f %f\n'%(i[0], i[2], i[1], i[3]))
	# 	f.close()	
	for k in blocks:
		anns.append({"class": k[4],
				  "id": k[5],
		          "height": k[3]-k[1],
		          "type": "rect",
		          "width": k[2]-k[0],
		          "x": k[0],
		          "y": k[1]})		
	seg = [{
	        "annotations": anns,
	      }]		
	with open(outname,'w') as f:
		json.dump(seg, f, indent=4)
		f.close()
	# print timeit.default_timer()-start_time
if __name__=='__main__':
	main()















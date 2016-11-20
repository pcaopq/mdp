import sys

sys.path.insert(0, '..')
from metrics.EvalOneToMany import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from readJSON import *

import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
#import seaborn as sns


scale_factor = 13
img_width = 4796.0
img_height = 7216.0

scaled_width = img_width / scale_factor
scaled_height = img_height / scale_factor

class ImageViewer(QLabel):
	seg_path = ''
	should_paint = False

	def __init__(self, text=''):
		QLabel.__init__(self, text)
		self.text = text

	def paintEvent(self, event):
		super(ImageViewer, self).paintEvent(event)
		
		if (len(self.seg_path) > 0):
			qp = QPainter()
			qp.begin(self)
			self.plot_segment(qp)
			qp.end()

	def plot_segment(self, qp):
		alpha = 127
		colors = [QColor(255, 0, 0, alpha), QColor(0, 255, 0, alpha), \
		 		  QColor(0, 0, 255, alpha), QColor(255, 255, 0, alpha), \
		 		  QColor(255, 0, 255, alpha), QColor(0, 255, 255, alpha), \
		 		  QColor(102, 185, 255, alpha)]
		count = 0
		color_map = {}
		rect = rect_from_json(self.seg_path)
		
		color = QColor(0, 0, 0)
		color.setNamedColor('#d4d4d4')
		qp.setPen(color)

		for r in rect:
			if 'id' not in r:
				continue
			if not r['id'] in color_map:
				color_map[r['id']] = colors[count % len(colors)]
				count += 1
			qp.setBrush(color_map[r['id']])
			rx = r['x'] / scale_factor
			ry = r['y'] / scale_factor
			rw = r['width'] / scale_factor
			rh = r['height'] / scale_factor
			qp.drawRect(rx, ry, rw, rh)

class Visualizer(QMainWindow):
	seg_path = ''
	gt_path = ''
	last_folder = '.'
	def __init__(self):
		super(Visualizer, self).__init__()

		self.initUI()

	def initUI(self):
		self.setGeometry(100, 100, 1200, 650)
		self.setWindowTitle('Visualizer')
		self.initButton()
		self.initImageViewer()
		self.initLabel()
		self.initText()
		self.show()

	def initLabel(self):
		self.precisionLabel = QLabel(self)
		self.precisionLabel.move(900, 50)
		self.precisionLabel.setText('Precision')

		self.recallLabel = QLabel(self)
		self.recallLabel.move(900, 150)
		self.recallLabel.setText('Recall')

		self.fscoreLabel = QLabel(self)
		self.fscoreLabel.move(900, 250)
		self.fscoreLabel.setText('Fscore')

		self.segmentNameLabel = QLabel(self)
		self.segmentNameLabel.move(900, 350)
		self.segmentNameLabel.setText('Segment file')

		self.gtNameLabel = QLabel(self)
		self.gtNameLabel.move(900, 450)
		self.gtNameLabel.setText('Ground truth file')
	def initText(self):
		self.precisionText = QLineEdit(self)
		self.precisionText.move(900, 80)
		self.precisionText.setReadOnly(True)

		self.recallText = QLineEdit(self)
		self.recallText.move(900, 180)
		self.recallText.setReadOnly(True)

		self.fscoreText = QLineEdit(self)
		self.fscoreText.move(900, 280)
		self.fscoreText.setReadOnly(True)

		self.segmentNameText = QLineEdit(self)
		self.segmentNameText.setGeometry(900, 380, 250, 20)
		self.segmentNameText.setReadOnly(True)

		self.gtNameText= QLineEdit(self)
		self.gtNameText.setGeometry(900, 480, 250, 20)
		self.gtNameText.setReadOnly(True)
		
	def initButton(self):
		self.openImg = QPushButton('Select image', self)
		self.openImg.setGeometry(20, 10, 150, 20)
		self.openImg.clicked.connect(self.getImage)

		self.openSeg = QPushButton('Select segmentation', self)
		self.openSeg.setGeometry(220, 10, 150, 20)
		self.openSeg.clicked.connect(self.getSegPath)

		self.openGt = QPushButton('Select ground truth', self)
		self.openGt.setGeometry(420, 10, 150, 20)
		self.openGt.clicked.connect(self.getGtPath)

		self.checkBox = QCheckBox('Use block level eval', self)
		self.checkBox.setGeometry(620, 10, 150, 20)
		self.checkBox.stateChanged.connect(self.evaluate)

	def initImageViewer(self):
		self.segViewer = ImageViewer(self)
		self.segViewer.setGeometry(20, 50, scaled_width, scaled_height)
		self.gtViewer = ImageViewer(self)
		self.gtViewer.setGeometry(520, 50, scaled_width, scaled_height)

	def getImage(self):
		f_name = QFileDialog.getOpenFileName(self, 'Open file', self.last_folder)
		self.last_folder = f_name.mid(0, f_name.lastIndexOf('/'))
		f = open(f_name, 'r')
		with f:
			image = QPixmap(f_name).scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)
			self.segViewer.setPixmap(image)
			self.gtViewer.setPixmap(image)

	def getSegPath(self):
		f_name = QFileDialog.getOpenFileName(self, 'Open file', self.last_folder)
		self.segmentNameText.setText(f_name.mid(f_name.lastIndexOf('/') + 1, len(f_name)))
		self.last_folder = f_name.mid(0, f_name.lastIndexOf('/'))
		if (len(f_name) > 0):
			self.segViewer.seg_path = self.seg_path = f_name
			self.segViewer.update()
			if (len(self.gt_path) > 0):
				self.evaluate()

	def getGtPath(self):
		f_name = QFileDialog.getOpenFileName(self, 'Open file', self.last_folder)
		self.gtNameText.setText(f_name.mid(f_name.lastIndexOf('/') + 1, len(f_name)))
		self.last_folder = f_name.mid(0, f_name.lastIndexOf('/'))
		if (len(f_name) > 0):
			self.gtViewer.seg_path = self.gt_path = f_name
			self.gtViewer.update()
			if (len(self.seg_path) > 0):
				self.evaluate()

	def evaluate(self):
		evaluator = EvalOneToMany()
		is_block_level = False
		if self.checkBox.isChecked():
			is_block_level = True
		f_score, precision, recall = evaluator.evaluate(str(self.seg_path), str(self.gt_path), is_block_level)
		self.precisionText.setText('%.3f' % precision)
		self.recallText.setText('%.3f' % recall)
		self.fscoreText.setText('%.3f' % f_score)

	def changeEval(self, state):
		self.evaluate()
            
	def getOverallScore(self):
		evaluator = EvalOneToMany()
		is_block_level = False
		if self.checkBox.isChecked():
			is_block_level = True
		segPath = "/Users/dylanlu/mdp2016/xiaofei/"
		gtPath = "/Users/dylanlu/mdp2016/stefan/"
		totalf = 0
		totalprecision = 0
		totalrecall = 0
		num = 0;
		fscoreset = []
		precisionset = []
		recallset = []
		for filename in os.listdir(segPath):
			if filename.endswith(".json"):
				#print filename
				for filename2 in os.listdir(gtPath):
					if filename==filename2: 
						#print segPath+str(filename)
						f_score, precision, recall = evaluator.evaluate(segPath+str(filename), gtPath+str(filename2), is_block_level)					
						if f_score < 0.5 :
							print segPath+str(filename)
							print gtPath+str(filename2)
						totalf += f_score
						totalprecision += precision
						totalrecall += recall
						fscoreset.append(f_score)
						precisionset.append(precision)
						recallset.append(recall)
						num = num + 1
						break
					else:
						continue

		segPath = "/Users/dylanlu/mdp2016/lian/"
		gtPath = "/Users/dylanlu/mdp2016/stefan/"
		for filename in os.listdir(segPath):
			if filename.endswith(".json"):
				#print filename
				for filename2 in os.listdir(gtPath):
					if filename==filename2: 
						#print segPath+str(filename)
						f_score, precision, recall = evaluator.evaluate(segPath+str(filename), gtPath+str(filename2), is_block_level)					
						if f_score < 0.5 :
							print segPath+str(filename)
							print gtPath+str(filename2)
						totalf += f_score
						totalprecision += precision
						totalrecall += recall
						fscoreset.append(f_score)
						precisionset.append(precision)
						recallset.append(recall)
						num = num + 1
						break
					else:
						continue
		segPath = "/Users/dylanlu/mdp2016/panfeng/"
		gtPath = "/Users/dylanlu/mdp2016/stefan/"
		for filename in os.listdir(segPath):
			if filename.endswith(".json"):
				#print filename
				for filename2 in os.listdir(gtPath):
					if filename==filename2: 
						#print segPath+str(filename)
						f_score, precision, recall = evaluator.evaluate(segPath+str(filename), gtPath+str(filename2), is_block_level)					
						if f_score < 0.5 :
							print segPath+str(filename)
							print gtPath+str(filename2)
						totalf += f_score
						totalprecision += precision
						totalrecall += recall
						fscoreset.append(f_score)
						precisionset.append(precision)
						recallset.append(recall)
						num = num + 1
						break
					else:
						continue

		segPath = "/Users/dylanlu/mdp2016/xiaofei/"
		gtPath = "/Users/dylanlu/mdp2016/lian/"
		for filename in os.listdir(segPath):
			if filename.endswith(".json"):
				#print filename
				for filename2 in os.listdir(gtPath):
					if filename==filename2: 
						#print segPath+str(filename)
						f_score, precision, recall = evaluator.evaluate(segPath+str(filename), gtPath+str(filename2), is_block_level)					
						if f_score < 0.5 :
							print segPath+str(filename)
							print gtPath+str(filename2)
						totalf += f_score
						totalprecision += precision
						totalrecall += recall
						fscoreset.append(f_score)
						precisionset.append(precision)
						recallset.append(recall)
						num = num + 1
						break
					else:
						continue

		segPath = "/Users/dylanlu/mdp2016/xiaofei/"
		gtPath = "/Users/dylanlu/mdp2016/panfeng/"
		for filename in os.listdir(segPath):
			if filename.endswith(".json"):
				#print filename
				for filename2 in os.listdir(gtPath):
					if filename==filename2: 
						#print segPath+str(filename)
						f_score, precision, recall = evaluator.evaluate(segPath+str(filename), gtPath+str(filename2), is_block_level)					
						if f_score < 0.5 :
							print segPath+str(filename)
							print gtPath+str(filename2)
						totalf += f_score
						totalprecision += precision
						totalrecall += recall
						fscoreset.append(f_score)
						precisionset.append(precision)
						recallset.append(recall)
						num = num + 1
						break
					else:
						continue

		segPath = "/Users/dylanlu/mdp2016/lian/"
		gtPath = "/Users/dylanlu/mdp2016/panfeng/"
		for filename in os.listdir(segPath):
			if filename.endswith(".json"):
				#print filename
				for filename2 in os.listdir(gtPath):
					if filename==filename2: 
						#print segPath+str(filename)
						f_score, precision, recall = evaluator.evaluate(segPath+str(filename), gtPath+str(filename2), is_block_level)					
						if f_score < 0.5 :
							print segPath+str(filename)
							print gtPath+str(filename2)
						totalf += f_score
						totalprecision += precision
						totalrecall += recall
						fscoreset.append(f_score)
						precisionset.append(precision)
						recallset.append(recall)
						num = num + 1
						break
					else:
						continue

		
		f_score = totalf/float(num)
		precision = totalprecision/float(num)
		recall = totalrecall/float(num)
		self.precisionText.setText('%.3f' % f_score)
		self.recallText.setText('%.3f' % precision)
		self.fscoreText.setText('%.3f' % recall)
		#plt.hist(fscoreset,bins=20,range=[0,1])
		plt.hist(precisionset,bins=20, color='r', alpha=0.5,range=[0,1])
		#plt.hist(recallset,bins=20, color='g',alpha=0.3,range=[0,1])
		plt.ylim((0,10))
		plt.xlabel("Score")
		plt.ylabel("Number")
		plt.title("Precision distribution")
		#plt.legend(('fscore','precision','recall'))
		plt.show()
#sns.set(color_codes=True)
#np.random.seed(sum(map(fscoreset, "distributions")))
            #print totalf/float(num)
            #print totalprecision/float(num)
            #print totalrecall/float(num)
		#f_score, precision, recall = evaluator.evaluate()


def main():
	app = QApplication(sys.argv)
	vis = Visualizer()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

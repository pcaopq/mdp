import os, sys
import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from readJSON import *
from memory_profiler import profile
from memory_profiler import memory_usage
import pdb
import timeit
import time
sys.path.insert(0, './latex_generator')
from report_generator import *

class EndToEnd:
    ''' assumes segmentation algo.s take command line arguments as follows:
         python dilate_segmenter.py <imagename> <segmentation_output_path>
         <xmlname> <outname>
        e.g.
         python textblocksBS.py 1115.jp2 ../../output/segment
         1115.xml 1115.result.json

        assumes evaluation metric takes command line arguments as follows:
         python evaluation_metric.py <evaluation_output_path>
         <segmentation_output_path> <ground_truth> <segmentation_result>
         <imagename> <xmlname>
         e.g.
         python evaluation.py ../../output/eval ../../output/segment
         1115.json 1115.result.json 1115.jpg 1115.xml
    '''
    def __init__(self, config_filename='config.txt'):
        with open(config_filename) as f:
            mydict = eval(f.read())
            self.metrics = mydict['Metrics']
            self.implementations = mydict['Implementations']
            self.files = mydict['Files']
            self.seg_out_path = mydict['Output'][0]
            if not os.path.isdir(self.seg_out_path):
                os.system('mkdir self.seg_out_path')
            self.eval_out_path = mydict['Output'][1]
            if not os.path.isdir(self.eval_out_path):
                os.system('mkdir self.eval_out_path')
            self.eval_results = {}
            self.outlier_good = []
            self.outlier_bad = []
            self.filter_good = 0.7
            self.filter_bad = 0.4

    # fp = open('memory_profiler.log','w+')        
    # @profile(stream = fp)        
    def segment(self):
        if os.path.isfile(self.seg_out_path+'/'+'W2V0linker.py111VD0parser.py.time'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'W2V0linker.py111VD0parser.py.time')
        if os.path.isfile(self.seg_out_path+'/'+'W2V0linker.py111hist0parser.py.time'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'W2V0linker.py111hist0parser.py.time')
        if os.path.isfile(self.seg_out_path+'/'+'VD0linker.py111hist0parser.py.time'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'VD0linker.py111hist0parser.py.time')
        if os.path.isfile(self.seg_out_path+'/'+'VD0linker.py111VD0parser.py.time'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'VD0linker.py111VD0parser.py.time')      
        if os.path.isfile(self.seg_out_path+'/'+'VD0linker.py111IMG0parser.py.time'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'VD0linker.py111IMG0parser.py.time')  
        if os.path.isfile(self.seg_out_path+'/'+'W2V0linker.py111IMG0parser.py.time'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'W2V0linker.py111IMG0parser.py.time')                   
        if os.path.isfile(self.seg_out_path+'/'+'VDnewtime'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'VDnewtime')     
        if os.path.isfile(self.seg_out_path+'/'+'VD1newtime'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'VD1newtime')    
        if os.path.isfile(self.seg_out_path+'/'+'ImgSeg'):
            os.system('rm %s'%(self.seg_out_path,)+'/'+'ImgSeg')            
        for fname in self.files:
            if os.path.isdir(fname):
                for f in os.listdir(fname):
                    temp = f.split('.')
                    if temp[-1] == 'jpg':
                        f = temp[0]
                        for j, imp_name in enumerate(self.implementations):
                            if not os.path.isfile(imp_name):
                                print('invalid implementation file name ',imp_name)
                                continue
                            if imp_name.split('0')[-1] == 'parser.py':
                                print f+' PARSER: '+imp_name.split('0')[0]                                
                                command = 'python %s %s %s %s %s' % ((imp_name, self.seg_out_path,) +
                                      tuple(fname+'/'+f+ext for ext in ('.jpg','.xml','.'+imp_name.split('0')[0]+'.intermediate.json')))
                                os.system(command)
                                #make sure the intermediate file is created
                            elif imp_name.split('0')[-1] == 'linker.py':
                                print f+' LINKER: '+imp_name.split('0')[0]                          
                                tmp_name = self.implementations[j]+'111'+self.implementations[j-1]     
                                # command = 'python %s %s %s %s %s %s %s' % ((imp_name, self.seg_out_path, f+'.'+self.implementations[j]+'.result.json', self.seg_out_path, fname+'/'+f+'.'+imp_name.split('_')[0]+'.intermediate.json',)+
                                #  tuple(fname+'/'+f+ext for ext in ('.xml', '.jpg')))
                                command = 'python %s %s %s %s %s' % (imp_name, self.seg_out_path, f+'.'+tmp_name+'.result.json', self.seg_out_path, fname+'/'+f+'.'+self.implementations[j-1].split('0')[0]+'.intermediate.json')
                                # print command
                                start = timeit.default_timer()
                                os.system(command)
                                with open('../../output/segment'+'/'+tmp_name+'.time', 'a+') as f1:
                                    f1.write("%f"%(timeit.default_timer() - start,))   
                                    f1.write(' ')
                                f1.close()                                
            else:
                f = fname.split('.')[0]
                for imp_name in self.implementations:
                    if not os.path.isfile(imp_name):
                        print('invalid implementation file name', imp_name)
                        continue
                    command = 'python %s %s %s %s %s' % ((imp_name, self.seg_out_path,) +
                          tuple(f+ext for ext in ('.jpg','.xml','.'+imp_name+'.result.json')))
                    #print# command
                    os.system(command)

    def evaluate(self):
        '''assumes format groundtruth - ....gt.json'''
        # pdb.set_trace()
        for j,imp_name1 in enumerate(self.implementations):
            if imp_name1.split('0')[-1] == 'parser.py': continue
            imp_name = self.implementations[j]+'111'+self.implementations[j-1]
            for fname in self.files:
                if os.path.isdir(fname):
                    for f in os.listdir(fname):
                        temp = f.split('.')
                        if temp[-1] == 'jpg':
                            f = temp[0]
                            for metric_name in self.metrics:
                                if not os.path.isfile(metric_name):
                                    print('invalid implementation file name', metric_name)
                                    continue
                                command = 'python %s %s %s %s %s %s %s %s' % ((metric_name, self.eval_out_path, self.seg_out_path,) +
                                      tuple(fname+'/'+f+ext for ext in ('.json', '.'+imp_name+'.result.json', '.jpg', '.xml'))+(imp_name,))
                                # print command
                            os.system(command)
                else:
                    f = fname.split('.')[0]
                    for metric_name in self.metrics:
                        if not os.path.isfile(metric_name):
                            print('invalid implementation file name',metric_name)
                            continue
                        command = 'python %s %s %s %s %s %s %s %s' % ((metric_name, self.eval_out_path, self.seg_out_path,) +
                              tuple(f+ext for ext in ('.json', '.'+imp_name+'.result.json', '.jpg', '.xml'))+(imp_name,))
                        #print# command
                    os.system(command)

    def collect_data(self):
        ''' read in output data from evaluation metrics
            e.g. assume we have an image file named 1115.jpg, and segmentation algorithm
            textblocksBS.py, then this function will read data from 1115.jpg.textblcoksBS.py
            data will be saved in a dictionary in the following format:
            {"textblocksBS.py":
                {
                    precision:
                    recall:
                    score:
                    num_images:
                    history:
                    {
                        (precision1, recall1, score1),
                        (precision2, recall2, score2)
                    }
                }
        '''
        # pdb.set_trace()
        for i, imp_name1 in enumerate(self.implementations):
            if imp_name1.split('0')[-1] == 'parser.py': continue
            imp_name = self.implementations[i]+'111'+self.implementations[i-1]
            alg_result = {} # a dictionary contains precision, recall, score, history
            imp_pre, imp_rec, imp_score = 0.0, 0.0, 0.0
            eval_history = [] # precision, recall, score average for each image
            filter_good = self.filter_good
            filter_bad = self.filter_bad
            nfiles = len(self.files)
            for fname in self.files:
                if os.path.isdir(fname):
                    nfiles = 0
                    for f in os.listdir(fname):
                        temp = f.split('.')
                        if temp[-1] == 'jpg':
                            nfiles += 1
                            history_path = self.eval_out_path+'/'+f+'.'+imp_name+'.out'
                            if not os.path.isfile(history_path):
                                print('no evaluation history', history_path)
                                return

                            img_pre, img_rec, img_score = 0.0, 0.0, 0.0
                            with open(history_path) as hf:
                                lines = hf.read().rstrip().split('\n')
                                for line in lines:
                                    numbers = line.split(' ')
                                    img_pre += float(numbers[0])
                                    img_rec += float(numbers[1])
                                    img_score += float(numbers[2])
                                if (img_score / len(lines)> filter_good):
                                    self.outlier_good.append((f,imp_name,img_score / len(lines)))
                                if (img_score / len(lines) < filter_bad):
                                    self.outlier_bad.append((f,imp_name,img_score / len(lines)))
                                eval_history.append((img_pre / len(lines), img_rec / len(lines), \
                                    img_score / len(lines), f))
                else:
                    f = fname.split('/')[-1]
                    history_path = self.eval_out_path+'/'+f+'.'+imp_name+'.out'
                    if not os.path.isfile(history_path):
                        #print# 'no evaluation history', history_path
                        return

                    img_pre, img_rec, img_score = 0.0, 0.0, 0.0
                    with open(history_path) as f:
                        lines = f.read().rstrip().split('\n')
                        for line in lines:
                            numbers = line.split(' ')
                            img_pre += float(numbers[0])
                            img_rec += float(numbers[1])
                            img_score += float(numbers[2])
                        if (img_score / len(lines) > filter_good):
                            self.outlier_good.append((f,imp_name,img_score / len(lines)))
                        if (img_score / len(lines) < filter_bad):
                            self.outlier_bad.append((f,imp_name,img_score / len(lines)))
                        eval_history.append((img_pre / len(lines), img_rec / len(lines), \
                            img_score / len(lines)))

            # calculate the precision, recall, score average for each algorithm
            #print# eval_history
            for r in eval_history:
                imp_pre += r[0]
                imp_rec += r[1]
                imp_score += r[2]
            imp_pre /= nfiles
            imp_rec /= nfiles
            imp_score /= nfiles

            eval_history = sorted(eval_history, key=lambda tup: tup[2])

            alg_result['num_images'] = nfiles
            alg_result['precision'] = imp_pre
            alg_result['recall'] = imp_rec
            alg_result['fscore'] = imp_score
            alg_result['history'] = eval_history
            global tmp
            tmp = 0
            if(imp_name == "W2V0linker.py111VD0parser.py"):
                with open("../../output/segment/W2V0linker.py111VD0parser.py.time") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp
                f.close()
            elif(imp_name == "W2V0linker.py111hist0parser.py"):
                tmp = 0
                with open("../../output/segment/W2V0linker.py111hist0parser.py.time") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp
                f.close()
            elif(imp_name == "VD0linker.py111hist0parser.py"):
                tmp = 0
                with open('../../output/segment/VD0linker.py111hist0parser.py.time', 'r') as f:
                    for i in f.read().rstrip().split(' '):
                        # print i
                        tmp += float(i)
                    alg_result['time'] = tmp                
                f.close() 
            elif(imp_name == "VD0linker.py111VD0parser.py"):
                tmp = 0
                with open('../../output/segment/VD0linker.py111VD0parser.py.time', 'r') as f:
                    for i in f.read().rstrip().split(' '):
                        # print i
                        tmp += float(i)
                    alg_result['time'] = tmp         
                f.close()     
            elif(imp_name == "VD0linker.py111IMG0parser.py"):
                tmp = 0
                with open("../../output/segment/VD0linker.py111IMG0parser.py.time") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp         
                f.close()                           
            elif(imp_name == "W2V0linker.py111IMG0parser.py"):
                tmp = 0
                with open("../../output/segment/W2V0linker.py111IMG0parser.py.time") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp         
                f.close()
            elif(imp_name == "VerticalDominance2.py"):
                tmp = 0
                with open("../../output/segment/VD2oldtime") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp         
                f.close()                           
            elif(imp_name == "VerticalDominance2New.py"):
                tmp = 0
                with open("../../output/segment/VD2newtime") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp         
                f.close()   
            elif(imp_name == "ImgSeg.py"):
                tmp = 0
                with open("../../output/segment/ImgSeg") as f:
                    for i in f.read().rstrip().split(' '):
                        tmp += float(i)
                    alg_result['time'] = tmp         
                f.close()
            self.eval_results[imp_name] = alg_result

    def generate_performance_curve(self):
        line_colors = ['r', 'g', 'b']
        plt.hold(True)
        for i, imp_name1 in enumerate(self.implementations):
            if imp_name1.split('0')[-1] == 'parser.py': continue
            imp_name = self.implementations[i]+'111'+self.implementations[i-1]
            eval_history = self.eval_results[imp_name]['history']
            count = 0
            x = []
            y = []
            last_record = eval_history[0][2]
            for record in eval_history[1:]:
                count += 1
                if record[2] > last_record:
                    y.append(last_record)
                    last_record = record[2]
                    x.append(count)
            y.append(last_record)
            x.append(len(eval_history))

            for j in range(len(x)):
                x[j] /= float(len(eval_history))

            plt.plot(x,y)
            plt.xlabel('percentage of data')
            plt.ylabel('F score')
            plt.line = plt.plot(x, y, line_colors[i % len(line_colors)], label=imp_name)
            plt.legend(loc='upper left')
        plt.hold(False)
        plt.gca().invert_xaxis()
        plt.savefig('./performance.png')
        plt.close()

    def generate_outlier(self):
        for imp_name, result in self.eval_results.items():
            if imp_name[-2:] == 'NA': continue
            worst_name = ''
            best_name = ''
            worst_val, best_val = 20, 0
            for record in result['history']:
                # record is (precision, recall, fscore, filename)
                if record[2] > best_val:
                    best_val = record[2]
                    best_name = record[3]
                if record[2] < worst_val:
                    worst_val = record[2]
                    worst_name = record[3]

            worst_out_path = self.seg_out_path+'/'+worst_name.split('.')[0]+'.'+imp_name+'.result.json'
            worst_gt_path = self.files[0]+'/'+worst_name.split('.')[0]+'.json'
            worst_img_path = self.files[0]+'/'+worst_name.split('.')[0]+'.jpg'
            best_out_path = self.seg_out_path+'/'+best_name.split('.')[0]+'.'+imp_name+'.result.json'
            best_gt_path = self.files[0]+'/'+best_name.split('.')[0]+'.json'
            best_img_path = self.files[0]+'/'+best_name.split('.')[0]+'.jpg'

            worst_out_fig_path = './'+imp_name+'.worst.png'
            worst_gt_fig_path = './'+imp_name+'.gt.worst.png'
            best_out_fig_path = './'+imp_name+'.best.png'
            best_gt_fig_path = './'+imp_name+'.gt.best.png'
            self.generate_segment_plot(worst_img_path, worst_out_path, worst_out_fig_path)
            self.generate_segment_plot(worst_img_path, worst_gt_path, worst_gt_fig_path)
            self.generate_segment_plot(best_img_path, best_out_path, best_out_fig_path)
            self.generate_segment_plot(best_img_path, best_gt_path, best_gt_fig_path)

    def generate_segment_plot(self, img_path, f_path, out_path):
        colors = ['r', 'g', 'b', 'y', 'c', 'm', '#4488ee', '#66ccff']
        count = 0
        color_map = {}
        rect = rect_from_json(f_path)
        currentAxis = plt.gca()
        img = mpimg.imread(img_path)
        plt.imshow(img, cmap='Greys_r')
        for r in rect:
            if not r['id'] in color_map:
                color_map[r['id']] = colors[count % len(colors)]
                count += 1
            currentAxis.add_patch(Rectangle((r['x'], r['y']), r['width'], r['height'], facecolor=color_map[r['id']], alpha=0.5))
        plt.axis([0, len(img[0]), 0, len(img)])
        plt.gca().invert_yaxis()
        plt.xlabel(f_path.split('.')[0])
        plt.savefig(out_path)

    # generate the file in latex form to plot the graphs
    def generate_report(self):
        r = Report_generator('./latex_generator/template.tex', './latex_generator/report.tex')
        r.generate_report(self.implementations, self.eval_results,self.outlier_good,self.outlier_bad,self.filter_good,self.filter_bad)
        os.system('pdflatex ./latex_generator/report.tex')
        os.system('open ./report.pdf')

def main():
   # pdb.set_trace()
   config_filename = sys.argv[1]
   end_to_end = EndToEnd(config_filename)
   end_to_end.segment()
   end_to_end.evaluate()
   end_to_end.collect_data()
   end_to_end.generate_performance_curve()
   end_to_end.generate_outlier()
   end_to_end.generate_report()
if __name__ == '__main__':
   main()


'''
A_0, A_1, ...

A_1 := A_1 minus A_0
A_2 := (A_2 minus A_1) minus A_0
.
.
.


'''

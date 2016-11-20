//
//  main.cpp
//  VD
//
//  Created by Panfeng Cao on 16/6/1.
//  Copyright © 2016年 Panfeng Cao. All rights reserved.
//

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include "VD.h"
using namespace std;
vector<float> VerticalDominance::tocorners(float y, float x, float h, float w){
    vector<float> a(4, 0);
    a[0] = y;
    a[1] = x;
    a[2] = y + h;
    a[3] = x + w;
    return a;
}

float VerticalDominance::vector_sum(vector<float> v){
    float sum = 0;
    for(auto i:v)
        sum += i;
    return sum/v.size();
}

vector<float> VerticalDominance::join_hori(vector<vector<float>>& coordinates){
    float sum0 = 0;
    float sum2 = 0;
    float min_1 = float(INT_MAX);
    float max_3 = float(INT_MIN);
    int len = coordinates.size();
    for(auto i:coordinates){
        sum0 += i[0];
        sum2 += i[2];
        if(min_1 > i[1])
            min_1 = i[1];
        if(max_3 < i[3])
            max_3 = i[3];
    }
    return vector<float>{sum0/len, min_1, sum2/len, max_3};
}
//care len(coors)
vector<float> VerticalDominance::join_hori2(vector<float> coors1, vector<float> coors2){
    vector<float> ret;
    ret.push_back((coors1[0]+coors2[0])/2.0);
    ret.push_back(min(coors1[1], coors2[1]));
    ret.push_back((coors1[2]+coors2[2])/2.0);
    ret.push_back(max(coors1[3], coors2[3]));
    return ret;
}

vector<float> VerticalDominance::join_verti(vector<vector<float>>& coordinates){
    vector<float> ret;
    if(coors.empty())
        return vector<float>(4, 0);
    float max_2 = float(INT_MIN);
    float max_3 = max_2;
    float min_0 = float(INT_MAX);
    float min_1 = min_0;
    for(auto i:coordinates){
        if(i[0] < min_0)
            min_0 = i[0];
        if(i[1] < min_1)
            min_1 = i[1];
        if(i[2] > max_2)
            max_2 = i[2];
        if(i[3] > max_3)
            max_3 = i[3];
    }
    return vector<float>{min_0, min_1, max_2, max_3};
}

void VerticalDominance::parse(const char* scrapedname){
    ifstream inputFile(scrapedname);
    string line;
    vector<vector<float>> coors_tmp;
    vector<float> floatmp;
    vector<string> contents_tmp;
    
    bool first;
    while(getline(inputFile, line, '-')){
        stringstream tmp(line);
        string ln;
        while(getline(tmp, ln, '\n')){
            stringstream tmpln(ln);
            string temp;
            first = true;
            while(getline(tmpln, temp, ' ')){
                if(first){
                    if(temp[0]<='9' && temp[0]>='0')
                    {
                        if(!contents_tmp.empty()){
                            contents.push_back(contents_tmp);
                            coors.push_back(join_hori(coors_tmp));
                            contents_tmp.clear();
                            coors_tmp.clear();
                        }
                        continue;
                    }
                    contents_tmp.push_back(temp);
                    first = false;
                }
                else{
                    floatmp.push_back(stof(temp));
                    if(floatmp.size() == 4){
                        coors_tmp.push_back(tocorners(floatmp[0], floatmp[1], floatmp[2], floatmp[3]));
                        floatmp.clear();
                    }
                }
            }
        }
    }
    coors.push_back(join_hori(coors_tmp));
    float minx = float(INT_MAX); float maxx = float(INT_MIN);
    float miny = minx; float maxy = maxx;
    int count = 0;
    for(auto i:coors){
        minx = min(minx, min(i[1], i[3]));
        maxx = max(maxx, max(i[1], i[3]));
        miny = min(miny, min(i[0], i[2]));
        maxy = max(maxy, max(i[0], i[2]));
        height.push_back(i[2] - i[0]);
        count++;
        cout<<count<<":"<<i[2]<<" - "<<i[0]<<" = " <<i[2] - i[0]<<endl;
    }
    cout<<"vpos ranges in ["<<miny<<","<<maxy<<"] "<<"hpos ranges in ["<<minx<<","<<maxx<<"]"<<endl;
}

float VerticalDominance::findtitleheight(vector<float> ht, float bins){
    float m = *min_element(ht.begin(), ht.end());
    float M = *max_element(ht.begin(), ht.end());
    cout<<m<<" "<<M<<endl;
    float r = M - m;
    float step = r/bins;
    float maxx = float(INT_MIN);
    int label = 0;
    vector<int> freqs(bins + 1, 0);
    for(auto h:ht){
        freqs[int(float(h-m)/step)]+=1;
    }
    for(int i = 0; i <= bins; i++){
        if(maxx < freqs[i]){
            label = i;
            maxx = freqs[i];
        }
    }
    while(label < bins && freqs[label] > freqs[label+1])
        label += 1;
    return m + label*step;
}

bool VerticalDominance::adjoins(vector<float>a, vector<float>b){
    float centerb = (b[0]+b[2])/2.0;
    float centera = (a[0]+a[2])/2.0;
    auto ayy = [=](int yy){return a[0]<yy<a[2];};
    auto byy = [=](int yy){return b[0]<yy<b[2];};
    return (ayy(centerb) && ayy(centera) && (a[1]-b[3] < 500) && (0<a[1]-b[3])) || (byy(centerb) && byy(centera) && (b[1]-a[3] < 500) && (0<b[1]-a[3]));
}

void VerticalDominance::getstrips(){
    float TH = findtitleheight(height, 20);
    cout<<"titleheights = "<<TH<<endl;
    for(auto i:coors){
        if(i[2] - i[0] < TH)
            textcoors.push_back(i);
        else
            titlecoors.push_back(i);
    }
}

void VerticalDominance::gettitleblocks(){
    titleblocks = titlecoors;
    long num_titles = titleblocks.size();
    vector<bool> flag(num_titles, true);
    vector<int> todel;
    for(int it = 0;it < num_titles;it++){
        if(flag[it])
            continue;
        for(int it0 = it+1;it0 < num_titles;it0++){
            if(flag[it0])
                continue;
            if(adjoins(titleblocks[it], titleblocks[it0])){
                flag[it0] = true;
                todel.push_back(it0);
                titleblocks[it] = join_hori2(titleblocks[it], titleblocks[it0]);
            }
        }
    }
    sort(todel.begin(), todel.end());
    for(int i = todel.size() - 1; i >= 0; i--)
        titleblocks.erase(titleblocks.begin() + todel[i] - 1);
}

bool VerticalDominance::dominates(vector<float> a, vector<float> b){
    float centerb0 = (b[1]+3*b[3])/4.0;
    float centerb1 = (3*b[1]+b[3])/4.0;
    auto axx = [=](int xx){return a[1] < xx && xx < a[3];};
    return a[0]<b[2] and (axx(centerb0) or axx(centerb1));
}

bool VerticalDominance::supports(vector<float> a, vector<float> b){
    float centerb0 = (1*b[1]+3*b[3])/4.0;
    float centerb1 = (3*b[1]+1*b[3])/4.0;
    auto axx = [=](int xx){return a[1] < xx && xx < a[3];};
    return a[2]>=b[0] and (axx(centerb0) or axx(centerb1));
}

void VerticalDominance::assign_textblocks(){
    vector<vector<vector<float>>> ret(titlecoors.size(), vector<vector<float>>());
    float max_title = float(INT_MIN);
    int max_label = -1;
    for(auto i:textcoors){
        for(int j = 0;j < titlecoors.size();j++){
            if(!dominates(titlecoors[j], i))
                continue;
            if(titlecoors[j][2] > max_title){
                max_title = titlecoors[j][2];
                max_label = j;
            }
        }
        if(max_label > 0)
            ret[max_label].push_back(i);
        else
            cout<<"no title dominates ["<<i[0]<<","<<i[1]<<","<<i[2]<<","<<i[3]<<"]"<<endl;        max_label = -1;
    }
    assignments = ret;
}

void VerticalDominance::group_textblocks(){
    long title_number = assignments.size();
    vector<vector<vector<float>>> tmp(title_number, vector<vector<float>>());
    vector<int> todel;
    vector<vector<float>> ws;
    for(int i = 0; i < title_number; i++){
        while(!assignments[i].empty()){
            vector<float> lowest = assignments[i][0];
            for(int j = 1;j < assignments[i].size();j++){
                if(supports(assignments[i][j], lowest))
                    lowest = assignments[i][j];
            }
            for(int k = 0;k < assignments[i].size();k++){
                if(supports(lowest, assignments[i][k])){
                    ws.push_back(assignments[i][k]);
                    todel.push_back(k);
                }
            }
            tmp[i].push_back(join_verti(ws));
            for(int l = todel.size() - 1;l >= 0;l--)
                assignments[i].erase(assignments[i].begin() + todel[l] -1);
            todel.clear();
            ws.clear();
        }
    }
    articleblocks = tmp;
}
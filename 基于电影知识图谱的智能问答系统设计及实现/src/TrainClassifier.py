# -*- coding: utf-8 -*-
# @Time    : 2019/5/3 18:17
# @Author  : Weiyang
# @File    : TrainClassifier.py
'''
训练一个朴素贝叶斯分类器，用于分类我们定义的14类问题

模型原始输入：经过槽位标记处理后的文本数据，例如：[word1,nnt,ng,nm,x,word2,...]
模型用于训练的输入：one-hot词向量，词包路径在配置文件config.ini中trainData一节
模型输出：问题类别标签，例如[0],[1],....，共14类

模型训练数据：可查看配置文件config.ini中trainData一节
'''

import configparser
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score

def getVocab(cfg):
    '获取词包，构建单词到编码的词典，如:{word:code,...}'
    'cfg是configparser.ConfigParser()对象'
    from collections import defaultdict
    word2code = defaultdict(int)
    with open(cfg.get('trainData','vocabulary_path'),encoding='utf-8') as fi:
        for line in fi:
            line = line.strip().split(':')
            word2code[line[1]] = int(line[0])
    return word2code

def transformData(data,word2code):
    '将输入数据转换为one-hot向量'
    'data是一个词列表，word2code是单词到编码的映射词典'
    word2vec = [0]*len(word2code) # 初始的one-hot词向量
    for word in data:
        # 判断word是否在词包里
        if word not in word2code:
            continue
        word2vec[word2code[word]] = 1
    return word2vec

def getData(cfg,epoch,rate=0.8):
    '获取训练数据，并将数据转为one-hot向量,最后返回训练集和测试集'
    'cfg是configparser.ConfigParser().read()对象,epoch是迭代次数，rate是训练集占全部数据的比例'
    import jieba as jb
    # 存储训练数据和标签数据
    all_data = []
    all_label = []

    #加载自定义词典
    jb.load_userdict(cfg.get('trainData','trainDictPath'))
    # 创建单词到编码的映射表
    word2code = getVocab(cfg)
    # 读取每个数据集的路径
    options = cfg.options('trainData')

    # 读取训练数据,循环遍历每个类的数据集
    for label,path in enumerate(options[:14]):
        with open(cfg.get('trainData',path),'r',encoding='utf-8-sig') as fi:
            for line in fi:
                words = list(jb.cut(line.strip()))
                word2vec = transformData(words,word2code)
                all_data.append(word2vec)
                all_label.append(label)
    # 混洗数据
    import numpy as np
    data = np.array(all_data*epoch)
    label = np.array(all_label*epoch)
    shuffle_index = np.random.permutation(np.arange(len(label)))
    data = data[shuffle_index]
    label = label[shuffle_index]

    # 切分训练集和测试集
    rate = int(len(label)*rate)
    train_data = data[:rate]
    test_data = data[rate:]
    train_label = label[:rate]
    test_label = label[rate:]

    return train_data,train_label,test_data,test_label

def saveModel(clf,cfg):
    '保存训练好的模型'
    'clf是训练好的模型,cfg是configparser.ConfigParser().read()对象'
    from sklearn.externals import joblib
    save_path = cfg.get('modelSave','model_path')
    joblib.dump(clf,save_path)

def getEveryLabelMetrics(y_true,y_pred,label_count):
    '获取多分类中，每个类别的准招率'
    'y_true是真实类别，y_pred是预测类别，label_count是类别总数'
    from sklearn.metrics import precision_score
    from sklearn.metrics import recall_score
    import numpy as np

    label_true = [] # 存储真实类别
    # 循环计算每个类别的准招率,i表示当前类别
    for i in range(label_count):
        index = [] # 记录类别实例的索引
        for j in range(len(y_true)):
            # 判断真实标签集合中的类别，是否是当前类别
            if i == y_true[j] :
                label_true.append(1) # 将当前类别的真实实例添加到真实标签集合里,这里用1表示正类
                index.append(j) # 记录下当前实例的索引
        pred = np.array(y_pred)
        label_pred = pred[np.array(index)].tolist() # 获取当前类别的预测实例
        # 将负类用0表示
        for k in range(len(label_pred)):
            if label_pred[k] == i:
                label_pred[k] = 1
            else:
                label_pred[k] = 0
        accuracy = precision_score(label_true,label_pred)
        recall = recall_score(label_true,label_pred)
        print('label: {0},Precision: {1},Recall: {2}'.format(i,accuracy,recall))
        label_true = []

def main(cfg):
    '训练模型主程序入口'
    'cfg是configparser.ConfigParser().read()对象'
    Epochs = 1000 # 迭代次数,这里我们直接将数据集复制1000倍以达到相同的结果

    # 获取训练数据
    train_data,train_label,test_data,test_label = getData(cfg,epoch=Epochs)
    clf = MultinomialNB()
    clf.fit(train_data,train_label) # 训练模型
    #y_pred = clf.predict_proba(test_data) # 预测结果,输出每个类的概率
    y_pred = clf.predict(test_data) # 预测结果，输出类别
    accuracy = accuracy_score(test_label,y_pred)
    recall = recall_score(test_label,y_pred,average='macro')
    print('所有类别的Accuracy: ',accuracy)
    print('所有类别的Recall: ',recall)
    # 获取每个类别的准招率
    getEveryLabelMetrics(test_label,y_pred,label_count=cfg.getint('classifierLabelCount','label_count'))
    # 保存训练好的模型
    saveModel(clf,cfg)

if __name__ == '__main__':
    # 读取配置
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')
    main(cfg)

    '''
    所有类别的Accuracy:  0.9050490196078431
    所有类别的Recall:  0.9326104857548566
    label: 0,Precision: 1.0,Recall: 1.0
    label: 1,Precision: 1.0,Recall: 1.0
    label: 2,Precision: 1.0,Recall: 1.0
    label: 3,Precision: 1.0,Recall: 1.0
    label: 4,Precision: 1.0,Recall: 1.0
    label: 5,Precision: 1.0,Recall: 0.9023136246786633
    label: 6,Precision: 1.0,Recall: 1.0
    label: 7,Precision: 1.0,Recall: 0.5855101034992607
    label: 8,Precision: 1.0,Recall: 0.6337958374628345
    label: 9,Precision: 1.0,Recall: 0.934927234927235
    label: 10,Precision: 1.0,Recall: 1.0
    label: 11,Precision: 1.0,Recall: 1.0
    label: 12,Precision: 1.0,Recall: 1.0
    label: 13,Precision: 1.0,Recall: 1.0
    '''
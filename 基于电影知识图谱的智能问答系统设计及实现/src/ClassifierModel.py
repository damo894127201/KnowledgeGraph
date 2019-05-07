# -*- coding: utf-8 -*-
# @Time    : 2019/5/3 21:10
# @Author  : Weiyang
# @File    : ClassifierModel.py

class ClassifierModel(object):
    '''
    分类器：加载训练好的模型，分类问题
    程序输入：经过槽位标记处理后的文本数据,是一个单词列表，例如:[word1,word2,...]
    程序输出：类别，以及类别的概率 label , proba
    '''
    def __init__(self,cfg):
        self.cfg = cfg # cfg是configparser.ConfigParser().read()对象
        self.model = self.load_model()  # 存储模型

    def __getVocab(self):
        '获取词包，构建单词到编码的词典，如:{word:code,...}'
        'cfg是configparser.ConfigParser().read()对象'
        from collections import defaultdict
        word2code = defaultdict(int)
        with open(self.cfg.get('trainData', 'vocabulary_path'), encoding='utf-8') as fi:
            for line in fi:
                line = line.strip().split(':')
                word2code[line[1]] = int(line[0])
        return word2code

    def __transformData(self,data, word2code):
        '将输入数据转换为one-hot向量'
        'data是一个词列表，word2code是单词到编码的映射词典'
        word2vec = [0] * len(word2code)  # 初始的one-hot词向量
        for word in data:
            # 判断word是否在词包里
            if word not in word2code:
                continue
            word2vec[word2code[word]] = 1
        return word2vec

    def getData(self,words_sentence):
        '获取训练数据，并将数据转为one-hot向量,最后返回预测类别和其相应的概率'
        'cfg是configparser.ConfigParser().read()对象,words_sentence输入单词列表'
        import numpy as np

        # 创建单词到编码的映射表
        word2code = self.__getVocab()
        # 将输入单词数据转换为ont-hot向量
        word2vec = self.__transformData(words_sentence,word2code)
        # 由于模型训练数据是二维的，因此将one-hot向量转为二维，第一个维度表示数据记录的个数，第二维度是特征数
        word2vec = np.array([word2vec])
        return word2vec

    def load_model(self):
        '加载模型,返回模型'
        from sklearn.externals import joblib
        # 读取模型存储路径
        path = self.cfg.get('modelSave','model_path')
        model = joblib.load(path)
        return model

    def predict(self,word2vec):
        '获取预测标签和其概率'
        'word2vec是self.getData()返回的对象'
        label = self.model.predict(word2vec)
        proba = self.model.predict_proba(word2vec)

        return label[0],round(max(proba[0]),2)

if __name__ == "__main__":
    # 读取配置文件
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')

    text = ['nm','ng'] # 待预测文本词列表
    clf = ClassifierModel(cfg) # 创建分类器
    word2vec = clf.getData(text) # 输入数据转为向量表示
    label,proba = clf.predict(word2vec) # 预测
    print(label)
    print(proba)

    '''
    3
    0.22
    '''
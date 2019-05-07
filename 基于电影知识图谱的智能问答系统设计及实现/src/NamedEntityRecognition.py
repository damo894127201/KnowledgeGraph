# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 17:47
# @Author  : Weiyang
# @File    : NamedEntityRecognition.py
'''
命名实体识别：
这里采用字典匹配的方式进行识别
我们定义了如下几种实体：
1. nm：槽位标记，指具体的电影名
2. nnt：槽位标记，指具体的演员名
3. ng：槽位标记，指具体的体裁名
4. x ：槽位标记，指具体的电影评分值

程序输入：单词列表
程序输出：
1. 单词列表中的实体经过槽位标记替换后的单词列表,如[word1,nnt,word2,nm,..]
2. 槽位标记对应的单词的映射表，例如：{nnt:[word1,word2,..],ng:[word1,word2,..],nm:[word1,word2,..],x:[word1,word2,..]}
3. 槽位标记的数量
'''

class NamedEntityRecognition(object):
    '命名实体识别，并返回槽位标记后的列表'
    def __init__(self,cfg):
        self.cfg = cfg # cfg是configparser.ConfigParser().read()对象
        self.genreDict = self.__getGenre() # 存储电影体裁名
        self.movieDict = self.__getMovie() # 存储电影名
        self.scoreDict = self.__getScore() # 存储得分值
        self.actorDict = self.__getActor() # 存储演员名

    def __getGenre(self):
        '获取电影体裁名'
        genre = []
        with open(self.cfg.get('customDict','genreDictPath'),'r',encoding='utf-8-sig') as fi:
            for line in fi:
                genre.append(line.strip())
        return genre

    def __getMovie(self):
        '获取电影名'
        movie = []
        with open(self.cfg.get('customDict','movieDictPath'),'r',encoding='utf-8-sig') as fi:
            for line in fi:
                movie.append(line.strip())
        return movie

    def __getScore(self):
        '获取电影评分值'
        score = []
        with open(self.cfg.get('customDict','scoreDictPath'),'r',encoding='utf-8-sig') as fi:
            for line in fi:
                score.append(line.strip())
        return score

    def __getActor(self):
        '获取演员名'
        actor = []
        with open(self.cfg.get('customDict','actorDictPath'),'r',encoding='utf-8-sig') as fi:
            for line in fi:
                actor.append(line.strip())
        return actor

    def __getDict(self):
        '获取值是列表的词典'
        from collections import defaultdict
        mydict = defaultdict(list)
        return mydict

    def getSlot(self,wordlst):
        '将单词列表中的实体用槽位标记,并返回结果'
        'wordlst输入的单词列表'

        # 返回的单词列表
        words = []
        # 存储槽位标记的实体
        slotDict = self.__getDict()
        # 记录槽位标记的数量
        count = 0

        # 遍历单词列表
        for word in wordlst:
            # 至于 电影名 体裁名 演员名 三者重合的情况，我们不考虑
            # ng
            if word in self.genreDict:
                # 存储实体
                slotDict['ng'].append(word)
                words.append('ng')
                count += 1
                continue
            # nm
            if word in self.movieDict:
                slotDict['nm'].append(word)
                words.append('nm')
                count += 1
                continue
            # nnt
            if word in self.actorDict:
                slotDict['nnt'].append(word)
                words.append('nnt')
                count += 1
                continue
            # x
            if word in self.scoreDict:
                slotDict['x'].append(word)
                words.append('x')
                count += 1
                continue
            # 若不是预定义的实体，则保留
            words.append(word)
        return words,slotDict,count

if __name__ == '__main__':
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read('../config/config.ini', encoding='utf-8')

    ner= NamedEntityRecognition(cfg)

    print(ner.movieDict)
    print('-'*100)
    print(ner.genreDict)
    print('*'*100)
    print(ner.actorDict)
    print('='*100)
    print(ner.scoreDict)
    print('o'*100)

    wordlst = ['刘德华','参演','了','天下无贼','吗']
    words,slotDict,count = ner.getSlot(wordlst)
    print(words)
    print(slotDict)
    print(count)

    '''
    ['Forrest Gump', 'Kill Bill: Vol. 1', '英雄', 'Miami Vice', 'Indiana Jones and the Temple of Doom', '卧虎藏龙', "Pirates of the Caribbean: At World's End", 'Kill Bill: Vol. 2', 'The Matrix Reloaded', 'The Matrix Revolutions', 'Harry Potter and the Chamber of Secrets', 'Harry Potter and the Prisoner of Azkaban', 'Harry Potter and the Goblet of Fire', 'Harry Potter and the Order of the Phoenix', 'The Last Emperor', 'Harry Potter and the Half-Blood Prince', '花样年华', '2046', 'Lethal Weapon 4', 'Hannibal Rising', 'TMNT', '무사', 'Anna and the King', '满城尽带黄金甲', 'Teenage Mutant Ninja Turtles III', 'The Forbidden Kingdom', 'The Mummy: Tomb of the Dragon Emperor', 'Memoirs of a Geisha', 'Shakespeare in Love', 'Lara Croft Tomb Raider: The Cradle of Life', 'Wu Ji', 'Romeo Must Die', 'Rush Hour', '巴尔扎克与小裁缝', '风云雄霸天下', 'Kiss of the Dragon', 'Stardust', 'The Long Run', '暗战', '最佳拍档', 'Zuijia paidang daxian shentong', 'Zuijia paidang zhi nuhuang miling', 'Zuijia paidang zhi qianli jiu chaipo', '新最佳拍档', 'The Transporter', '色‧戒', 'Mimic', 'Rush Hour 3', 'Rush Hour 2', 'Shanghai Knights', 'Australia', '文雀', '霍元甲', 'Samsara', 'The Gods Must Be Crazy', 'A Cock and Bull Story', 'Shanghai Noon', '我是谁', '一半海水一半火焰', '倩女幽魂III：道道道', '倩女幽魂II人间道', 'DOA: Dead or Alive', '警察故事', '饺子', '警察故事4之简单任务', 'The Borrowers', 'The Corruptor', '黑侠', 'Enter the Dragon', '功夫', "Charlie's Angels: Full Throttle", 'Kung Fu Panda', '十面埋伏', '全职杀手', 'Double Impact', 'Koroshiya 1', 'Unleashed', 'High Heels and Low Lifes', '福星高照', '小白龙情海翻波', 'Around the World in 80 Days', 'Kickboxer', 'Chin Kei Bin 2 - Fa Tou Tai Kam', '韩城攻略', 'Shao Lin Si', '霹雳火', '荆轲刺秦王', '大红灯笼高高挂', 'War', '饮食男女', 'The Medallion', 'Sat sau ji wong', '黄飞鸿', '黄飞鸿之二男儿当自强', '黄飞鸿之三狮王争霸', '黄飞鸿之西域雄狮', '一个好人', 'Cradle 2 the Grave', 'Mulan', '七剑', '警察故事续集', 'The Tuxedo', '无间道', 'The One', '喋血双雄', '倚天屠龙记之魔教教主', '赤裸特工', '琉璃樽', '龙兄虎弟', '飞鹰计划', "L'Amant", '霸王别姬', 'Year of the Dragon', '重庆森林', '警察故事 III：超级警察', '太极张三丰', '城市猎人', '快餐车', '堕落天使', '醉拳', 'The Cannonball Run', '8 ½ Women', '英雄本色', '盲井', '蛇形刁手', '千禧曼波', '最好的时光', '师弟出马', '新警察故事', '无间道II', 'Shen hua', 'Bloodsport', 'The Replacement Killers', '精武门', '少林足球', '辣手神探', 'Bulletproof Monk', '少林卅六房', '特务迷城', 'Kung Pow: Enter the Fist', '牒血街头', 'The Gods Must Be Crazy II', 'Cannonball Run II', 'Fu Zi', '醉拳二', 'Highlander: Endgame', 'Монгол', '我的父亲母亲', 'Chi bi', '荡寇', 'Harry Potter and the Deathly Hallows: Part 1', 'Harry Potter and the Deathly Hallows: Part 2', '唐山大兄', 'Dai si gin', '"New York, I Love You"', '少年黄飞鸿之铁马骝', 'Dak ging san yan lui', '杀破狼', '西游记第壹佰零壹回之月光宝盒', 'A Room with a View', '鬼域', '黄石的孩子', 'Wu du', 'Jin bei tong', '豪侠', '长江七号', '放‧逐', 'Race to Witch Mountain', '神探', 'Ji jie hao / Assembly', 'Dragonball Evolution', 'Wake of Death', 'The Painted Veil', 'The Red Violin', '无间道III: 终极无间', '投名状', 'Ye yan', '三国之见龙卸甲', '江山美人', 'The Matrix Revisited', 'Anita and Me', 'Boarding Gate', '叶问', 'Tian di ying xiong', '墨攻', '狗咬狗', 'The Guyver', '黑社会2：以和为贵', '夕阳天使', '赤壁 2', '鬼打鬼', 'Zhong hua ying xiong', '牯岭街少年杀人事件', '龙虎门', 'Bodyguard: A New Beginning', '双子神偷', '鬼马天师', 'Du shen', 'Shu shan zheng zhuan', 'Dragon Lord', 'Tau man ji D', 'Oh Schucks...! Here Comes UNTAG', '门徒', 'Wushu', '神枪手 / Sun cheung sau', 'Gong fu guan lan', 'They Wait', '颐和园', '千机变', '力王', '方世玉', 'Hua pi', 'Jing wu ying xiong', 'Fong Sai Yuk juk jaap', 'Dark Matter', '証人', '非诚勿扰', 'Ying hung boon sik II', '阿飞正传', '春光乍洩', 'He ni zai yi qi', '데이지', 'Horsemen', '鼠胆龙威', '新精武门', '东方不败之风云再起', 'Hong Xi Guan: Zhi Shao Lin wu zu', '笑傲江湖II东方不败', 'Zhong Nan Hai bao biao', '파이란', '夏日福星', '给爸爸的信', '黄飞鸿之铁鸡斗蜈蚣', '飞渡捲云山', '龙腾虎跃', '黑社会', 'Jian hua yan yu Jiang Nan', '拳精', '龙的心', '双龙会', '火烧岛', 'Lin Shi Rong', '龙之忍者', 'Liu zhi qin mo', 'Mang lung', '白发魔女传', 'Xilu xiang', 'Huo Yuan-Jia', '蠍子战士', '重案组', '笑傲江湖', '招半式闯江湖', '伤城', '复仇', '十八般武艺', 'The Big Brawl', '笑拳怪招', 'Mo hup leung juk', '赌神2', '男儿本色', 'Bo chi tung wah', '蝴蝶', 'Chandni Chowk To China', '新宿事件', '如来神掌', '不能说的秘密', 'Ha Yat Dik Mo Mo Cha', '龙行天下', 'Shao Lin yu Wu Dang', '南京!南京!', 'A计划', 'A计划续集', 'Da lao ai mei li', 'Ding tian li di', '十四女英豪', '조폭 마누라 2: 돌아온 전설', 'Fei lung mang jeung', '西游记大结局之仙履奇缘', '天下第一拳', 'The Man from Hong Kong', 'Encrypt', '洪熙官', 'Ga yau hei si 2009', 'Shôrin shôjo', 'โลงต่อตาย', 'Feng Yun Jue', 'Shi ying xiong chong ying xiong', 'Kinamand', 'The Spy Next Door', 'Ten Minutes Older: The Trumpet', 'Mai dou xiang dang dang', 'Iron And Silk', '旺角卡门', 'Seventh Moon', '新座头市\u3000破れ！唐人剣', 'Into the Sun', 'Andy Lau Wonderful World Concert Tour Shanghai 2008', 'Gin gwai 2', '窃听风云', '伊波拉病毒', 'Fei chang wan mei', 'Kickboxer 2:  The Road Back', '奇蹟', 'Gong fu chu shen', 'Joi sun ho', 'Irma Vep', 'Bai fa mo nu zhuan II', 'Kung Fu Killer', '笑太极', 'Yi ngoi', 'PTU', '一一', '奇谋妙计五福星', '建国大业', 'Wing Chun', '缘份', 'Duo shuai', 'Hung kuen dai see', '柔道龙虎榜', 'Bo bui gai wak', 'Mor gwai tin si', '鬼子来了', 'Long nga', '秘岸', 'Duo biao', '大醉侠', 'The Pillow Book', 'The Legend of the 7 Golden Vampires', 'Muk lau hung gwong', 'Hu bao long she ying', 'Zhui Ying', '陆阿采与黄飞鸿', 'Qin Song', '天涯明月刀', '赤裸羔羊', 'Dai noi muk taam 009', 'Mei shao nian zhi lian', 'Lan Yu', '侠盗高飞', 'The Expendables', '六壮士', 'Xin du bi dao', 'House of Fury', 'Shamo', '旺角黑夜', '群龙戏凤', '宋家皇朝', '天下无贼', '虎鹤双形', 'Tai-Pan', '飞虎雄心2傲气比天高', '二十四城记', 'Pou hark wong', 'Legend of the Dragonslayer Sword', 'Adventures of Power', '苹果', 'Chinese Box', '倩女幽魂', '十月围城', '麦田', '黑拳', 'Mao xian wang', 'Baiyin diguo', '活着', 'Ching toi', 'Heaven & Earth', 'Prisoner 701: Sasori', 'The Touch', '铁三角', '黑白战场', '三岔口', 'Bau lit do see', '大只佬', 'Gong yuan 2000 AD', '金燕子', '金瓶梅2 爱的奴隶', '审死官', '五郎八卦棍', 'Women From Mars', 'Feng sheng', '满清十大酷刑', '风云Ⅱ', '花木兰', 'Ma Yong Zhen', '摩登保镳', '硬汉', 'Chin Long Chuen Suet', '红番区', '龙凤斗', '"쓰리, 몬스터"', 'Jin Yi Wei', '孔子', '战·鼓', '我的最爱', '紫蝴蝶', '搏命单刀夺命抢', 'Mit moon', '刁手怪招', 'Leui ting jin ging', '龙在天涯', '金瓶梅', '决战紫禁之顚', '大兵小将', 'Snake and Crane Arts of Shaolin', '"Sing kung chok tse yee: Ngor but mai sun, ngor mai chi gung"', '导火线', 'Luo ye gui gen', 'Ngo liu poh lut gau ching', 'Dead or Alive: Final', '极道黒社会', '十三太保', 'Xích lô', 'Hyôryû-gai', 'Qing feng xia', '半支烟', 'Blade II', 'One Last Dance', 'Die Another Day', '合气道', 'Hak bak do', 'Shao Lin xiao zi', '南北少林', 'Su Qi-Er', 'Tian mi mi', 'The Final Curtain', '全城热恋', '叶问2: 宗师传奇', 'Sham moh', 'Jump', '摇啊摇，摇到外婆桥', "Bruce Lee: A Warrior's Journey", '大内密探零零发', '唐伯虎点秋香', 'オペレッタ狸御殿', 'Ai qing hu jiao zhuan yi', 'Ci Ling', 'Wo de tangchao xiongdi', '同门', 'A Serious Shock! Yes Madam!', 'Keep Cool', '跟踪', 'Invisible Waves', '江湖', '女警察', 'Sijie', 'Ouran', '铁汉柔情', '宝葫芦的秘密', 'Nu zi tai quan qun ying hui', '少林门', 'Fa qian han', '秋菊打官司', 'Zu: The Warriors from the Magic Mountain', '吴清源', 'For lung', 'Shanghai', '迷你特攻队', 'The Karate Kid', 'Huang cun ke zhan', '超级计划', 'Kickboxer 3: The Art of War', 'Li Xiao Long zhuan qi', 'All About Women', 'Sam hoi tsam yan', '满清十大酷刑之赤裸凌迟2', 'Hunting Venus', 'Huang jia shi jie', '蜈蚣咒', '杜拉拉升职记', '岁月神偷', '醉马骝', '刀马旦', '古惑仔之人在江湖', 'Eros', 'Clean', '皇家师姐IV直击证人', '八仙饭店之人肉叉烧饱', 'Di yu wu men', 'San De huo shang yu Chong Mi Liu', 'She sha shou', '原振侠与卫斯理', '杂家小子', '青蛇', 'Mi tao cheng shu shi 1997', 'Mei nui sik sung', '奇逢敌手', 'Lik goo lik goo dui dui pong', '撕票风云', 'Ninja Terminator', '女集中营', '尸妖', '乌鼠机密档案', 'Wu zhao shi ba fan', 'Zhong gui', 'Bin lim mai ching', '残缺', '羔羊医生', 'Hu meng wei long', '천사몽']
    ----------------------------------------------------------------------------------------------------
    ['冒险片', '奇幻片', '动画片', '剧情片', '恐怖片', '动作片', '喜剧片', '历史片', '西部片', '惊悚片', '犯罪片', '纪录片', '科幻片', '悬疑片', '音乐片', '爱情片', '家庭片', '战争片', '电视电影片', '冒险', '奇幻', '动画', '剧情', '恐怖', '动作', '喜剧', '历史', '西部', '惊悚', '犯罪', '纪录', '科幻', '悬疑', '音乐', '爱情', '家庭', '战争', '电视电影']
    ****************************************************************************************************
    ['巩俐', '乔宏', '李连杰', '梁朝伟', '张曼玉', '章子怡', 'Chen Dao-Ming', '甄子丹', '周润发', 'Cheng Pei-Pei', '鲍德熹', '曾江', '吴宇森', '张耀扬', 'Paulyn Sun', 'Carina Lau', '成龙', '袁和平', '任达华', '陈凯歌', '张柏芝', '刘烨', 'Hong Chen', 'Mark Williams', '王文隽', '郭富城', '杨恭如', '舒淇', '方中信', 'Christopher Kubheka', '杜琪峰', '张学友', '刘德华', 'Waise Lee', '林雪', '曾志伟', 'Karl Maka', '许冠杰', 'Teddy Robin Kwan', 'Sylvia Chang', '林子祥', 'Tsui Hark', 'Ringo Lam', '刘家良', '陈雅伦', '李修贤', 'Nina Li Chi', '黄锦燊', '潘恒生', 'Corey Yuen Kwai', 'Anita Mui', 'Bill Tung', '林熙蕾', 'Collin Chou', '锺丽缇', 'N!xau', 'Lau Siu-Ming', '黄霑', 'Michelle Reis', '林青霞', '梁家辉', '周星驰', '元华', 'Jeffrey Lau', '莫文蔚', '洪金宝', '黄炳耀', '吴耀汉', 'Stanley Fung', '胡慧中', '林正英', 'Dick Wei', '吴镇宇', '任贤齐', '陈国新', '袁咏仪', 'Jacklyn Wu', '谷德昭', '梁咏琪', 'John Ching', 'James Wong', 'Lau Shun', 'Yuen Cheung-Yan', 'Yuen Shun-Yi', 'Ng See-Yuen', '姜大卫', '关之琳', 'Paul Fonoroff', '莫少聪', 'Alfred Cheung Kin-Ting', '黄秋生', '黎明', 'Sally Yeh', '张敏', '邱淑贞', '黎姿', '程小东', '谭咏麟', '王祖贤', '葛民辉', '林海峰', '温翠苹', '邬君梅', 'Ti Lung', '张国荣', 'Emily Chu', '吴孟达', 'Teresa Mo', '陈欣健', '罗烈', '徐少强', 'Ken Lo', '陈德森', '王宝强', '张家辉', '孙红雷', '李滨', 'Huang Lei', '张雨绮', '葛优', 'Jiang Wen', '王学圻', '赵薇', '吕良伟', 'Xing Yu', '徐玟晴', 'Mai Kei', '萧芳芳', '郑少秋', '陈惠敏', '张卫健', 'Anthony Chan', '刘松仁', 'Lam Wai', '徐锦江', '黄圣依', '罗美薇', 'Christine Ng', '柯受良', '惠英红', 'Sammi Cheng', 'Pauline Yeung', '叶德娴', '朱茵', '罗行堂', 'Yammie Lam Kit-Ying', '蔡少芬', 'Johnnie Kong', '陈观泰', '吴君如', 'Vincent Wan Yeung-Ming', '苑琼丹', '洪欣', '楚原', '刘仪伟', 'Yonfan', '胡军', 'Ann Bridgewater', '张涵予', '邓超', '金燕玲', 'Mabel Cheung', '向华强', '谷祖琳', '许冠文', '吴家丽', '杨菁菁', '黄晓明', '陈坤', 'Xu Jiao', '林国斌', 'Carman Lee', '黄子华', '郑丹瑞', 'Feng Yuanzheng', '陈玉莲', 'Tien Niu', '鲍汉琳', '沈殿霞', '郭晓冬', 'Ricky Ho Kwok-Kit', 'John Shum Kin-Fun', 'Cheung Tat-Ming', '刘以达', '李力持', '苗圃', 'Fung Hak-On', '元秋', '成奎安', '西瓜刨', 'Mars', '吴辰君', '于荣光', '田丰', '李美凤', 'Lee Siu-Kei', '吴启华', 'Kwong Leung Wong', '刘天兰', 'Wang Hsieh', 'Wong Chung', 'Maria Cordero', 'Candice Yu On-On', 'Felix Lok Ying-Kwan', 'Henry Fong Ping', '周海媚', '徐帆', '刘宝贤', 'Yuen Tak', 'Bradley James Allan', '柯俊雄', '午马', '叶进', 'Lau Kong', '龚蓓苾', '张智霖', '周慧敏', '梁曼仪', '钱嘉乐', 'Alex Man Chi-Leung', 'Lee Heung-Kam', 'Michael McFall', '锺镇涛', 'Leung Wing-Chung', 'Elaine Eca Da Silva', '龙方', '李蕙敏', '陈法蓉', '锺景辉', '郑裕玲', '梁家仁', '杨丽菁', 'Suki Kwan', '谷峰', '周文健', 'Jessica Hsuan', 'Amy Yip', 'Ha Chi-Chun', 'Lee Kin-Yan', '卢冠廷', '楼南光', '任世官', 'Billy Chow', 'Meg Lam Kin-Ming', '李丽丽', '刘家辉', '黄百鸣', 'Aman Chang', 'Chun Wong', '赵雅芝', '王伍福', '张国立', '王学兵', 'Patrick Tse Yin', '林子聪', 'Wong Kam-Kong', 'Ga-Ling Gung', '鬼媾人', 'Chiang Tao', 'Wilson Lam', '陈豪', 'Bowie Lam', 'Parkman Wong', 'Fan Wei Yee', '叶蕴仪', 'Tam Sin-Hung', '陈加玲', 'James Ha', '唐国强', 'Sheila Chan', '胡枫', '何东', '叶荣祖', 'Bruce Leung Siu-Lung', 'Nadia Chan', '袁洁莹', 'Lei Yu', '王羽', '陈晓东', 'Karel Wong Chi-Yeung', 'Joanna Chan', '刘劲', 'Wong Wan-Si', '秦沛', '高雄', 'Michelle Bestbier', '陈建斌', 'Emil Chow', 'Chi Fai Chan', 'Joe Cheng', '雷宇扬', 'Lung Tin-sang', '黄一飞', '陈松勇', 'Wyman Wong Wai-Man', 'Nancy Sit Ka-Yin', '童爱玲', 'Natalis Chan', 'Lam Kau', '吴志雄', '宁静', 'Catherine Lau', 'Chan Fai-Hung', 'Wan Chi-Keung', '张同祖', '佟大为', 'Matthew Wong Hin-Mung', 'Joe Cheng Cho', 'Ho Pak-Kwong', 'Josephine Koo', '陈数', 'Helen Ma Hoi-Lun', 'Deric Wan Siu-Lun', 'Pauline Kwan', '吴刚', 'Lee Hoi-Sang', 'Yao Wen-Xue', 'Han Yong-Hua', 'Hau Woon-Ling', '陈旭初', 'Tam Bing-Man', '黄新', '田青', 'Wong Ching-Ho', '何家驹', 'John Ching Tung', 'Jamie Luk Kim-Ming', '陈宝莲', 'Stuart Ong', '程守一', '李家声', 'Cheung Kwok-Leung', 'Rachel Lee', 'James Lai Wing-Keung', '关海山', '黄光亮', '黄贯中', '黄家驹', '黄家强', '叶世荣', 'Mimi Chu Mai-Mai', 'Cheng Man-Fai', 'Steven Fung Min-Hang', 'Tenky Tin Kai-Man', 'Leung Ming', 'Edmond So Chi-Wai', 'Wong Hung', 'Alex Lam Chi-Sin', '陈德容', '卢海鹏', '钱似莺', 'Albert Lai', '梁本熙', '黄斌', '植敬雯', 'Maggie Li Lin-Lin', 'Tony Leung Siu-Hung', 'Lee Ka-Ting', 'Go Wang', 'Tam Suk-Mooi', 'Samuel Leung Cheuk-Moon', 'Dung Chi-Wa', '惠天赐', 'Lee Sheung-Ching', 'Chiu Chi-Ling', '陈国坤', 'Jia Kang-Xi', '江欣燕', '陈龙', 'Victor Chew', '林小楼', 'Sunny Fang Kang', 'Michael Dinga', 'Paul Che Biu-Law', '许英秀', 'Chan Ging-Cheung', 'Lau Tin-Chi', '单立文', '陶泽如', 'Cho Ging-Man', 'Leung Sap-Yat', 'Peter Lai Bei-Dak', '吴大维', 'Ben Wong Chi-Yin', 'Chan Chi-Fai', 'Baat Leung-Gam', 'Mak Hiu-Wai', 'Cheng Ka-Sang', 'Pomson Shi', '施介强', 'Ha Chi-Jan', 'Yvonne Yung Hung', 'Chen Baoguo', 'Jimmy White', '汤镇业', 'Law Ho-Kai', 'Chan Ging', 'Mok Mei-Lam', 'Pak Man-Biu', '杨群', 'Alex Ng Hong-Ling', 'Tse Wai-Kit', 'Kam Hing-Yin', '冯小刚', 'Zhao Lei', '梁克逊', 'Dai Lung', '冯元炽', 'Kirk Wong Chi-Keung', '黄一山', 'May Law Koon-Lan', 'You Liping', 'Radium Cheung', '梁锦燊', '刘永', 'Sarah Lee Lai-Yui', 'Andrew Wu Ying-Kin', 'So Hon-Sang', '段伟伦', 'Yip San', 'Ricky Yi Fan-Wai', '石燕子', 'Lung Ming-Yan', '陈国邦', '黄杏秀', 'Maggie Chan Mei-Kei', 'Pang Chi-Ching', '卢宛茵', 'Jackson Ng Yuk-Sue', '邓浩光', 'Yiu Wai', 'Nancy Lan Sai', 'Gilbert Lam Wai-San', '古巨基', 'Cutie Mui Siu-Wai', 'Vivian Lai Shui-Yan', 'Joey Leung Wing-Chung', 'Garry Chan Chi-Shing', 'Chang Gan-Wing', 'Celia Sze Lim-Tse', 'Chow Chi-Fai', 'Wong Chi-Keung', 'Ben Wong Tin-Dok', '简达华', '雷达', 'Chang Kin-Ming', 'Vindy Chan', 'Lo Hung', 'Chow Yee-Fan', 'Jacky Cheung Chun-Hung', 'Bruce Law Lai-Yin', '李强', 'Chan San-Hiu', 'Saul Bamberger', 'Peter Mahlangu', 'Bo Kaesje', 'Elias Meintjies', 'Chow Mei-Yan', 'Heung Dip', '谭淑梅', 'Jonathan Chik Gei-Yee', 'Cheng Kwun-Min', 'Elaine Law Suet-Ling', 'Chan Tung', '王书麒', '刘仪伟', '梁韵蕊', '朱铁和', 'Leung Yuen-Jing', '颜丽如', 'Lau Cheun', '左颂昇', '陈明君', 'Tung Chi', '古明华', '黄贻青', '林琪欣', 'Wong Kwan-Hong', '陆树铭', '张武孝', 'Tse Ning', 'Chan Kim-Wan', 'Charles Shen', 'Sing Yan', '刘沙', 'Wang Jian', 'Jin Xin', 'Wong Bing', '修宗迪', '杨晓丹', 'Donald Freeman', '司马燕', 'Joyce Chan Yin-Hang', 'Mei Yee', '黄美琪', 'Kwok Kwan-Shing', 'Leung Shiu-Choi', 'Kwok Chi-Ho', 'Wong Chak-Man', 'Dave Lam Ching', 'Jacqueline Li', 'Kai Shi Chen', 'Phillip Ko', 'Cally Kwong', 'Chia Yung Liu']
    ====================================================================================================
    ['0', '0.0', '1', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2', '2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '3', '3.0', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '4', '4.0', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '5', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '6', '6.0', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7', '7.0', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '8', '8.0', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '9', '9.0', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '10']
    oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    ['nnt', '参演', '了', 'nm', '吗']
    defaultdict(<class 'list'>, {'nnt': ['刘德华'], 'nm': ['天下无贼']})
    2
    '''
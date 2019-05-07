# -*- coding: utf-8 -*-
# @Time    : 2019/5/3 18:05
# @Author  : Weiyang
# @File    : ImportDataToNeo4j.py
'''
加载数据到neo4j，构建知识图谱，前提是首先在命令行启动neo4j服务

数据存储在./data/source/ 中，你需要首先将此数据拷贝到neo4j的安装文件夹下的neo4j-community-3.5.5\import\里
然后再执行此程序
'''

from py2neo import Graph
import configparser

cfg = configparser.ConfigParser()
cfg.read('../config/config.ini', encoding='utf-8')
username = cfg.get('neo4j','username')
password = cfg.get('neo4j','password')

graph = Graph('http://localhost:7474',username=username,password=password)

# 创建Genre类节点：电影体裁类
statement = 'load csv with headers from "file:///genre.csv" as line merge (p:Genre{gid:toInteger(line.gid),name:line.gname})'
graph.evaluate(statement)
print('加载genre.csv成功........')

# 创建Actor类节点：演员类
statement = 'load csv with headers from "file:///person.csv" as line merge(p:Actor{pid:toInteger(line.pid),birth:line.birth,death:line.death,name:line.name,biography:line.biography,birthplace:line.birthplace})'
graph.evaluate(statement)
print('加载person.csv成功........')

# 创建Movie类节点：电影类
statement = 'load csv with headers from "file:///movie.csv" as line merge(p:Movie{movie_id:toInteger(line.movie_id),title:line.title,introduction:line.introduction,rating:toFloat(line.rating),releasedate:line.releasedate})'
graph.evaluate(statement)
print('加载movie.csv成功........')

# 创建关系：is
statement = 'load csv with headers from "file:///movie_to_genre.csv" as line match(from:Movie{movie_id:toInteger(line.movie_id)}),(to:Genre{gid:toInteger(line.gid)}) merge (from)-[r:is{movie_id:toInteger(line.movie_id),gid:toInteger(line.gid)}]->(to)'
graph.evaluate(statement)
print('加载movie_to_genre.csv成功........')

# 创建关系：参演
statement = 'load csv with headers from "file:///person_to_movie.csv" as line match(from:Actor{pid:toInteger(line.pid)}),(to:Movie{movie_id:toInteger(line.movie_id)}) merge (from)-[r:参演{pid:toInteger(line.pid),movie_id:toInteger(line.movie_id)}]->(to)'
graph.evaluate(statement)
print('加载person_to_movie.csv成功........')
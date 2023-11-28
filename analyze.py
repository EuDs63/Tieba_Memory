# 对posts.josn文件进行分析

import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取json文件
data = json.load(open("posts.json", encoding="utf-8"))

# 将文本数据拼接成一个长字符串
text_data = " ".join(post["text"] for post in data)

# 使用jieba分词
text_data = " ".join(jieba.cut(text_data))

# 读取停用词
# 停用词基于[stopwords/cn_stopwords.txt at master · goto456/stopwords](https://github.com/goto456/stopwords/blob/master/cn_stopwords.txt)
# 添加了贴吧常用的表情符号
stopwords = set()
content = [line.strip() for line in open('resources/cn_stopwords.txt','r',encoding="utf8").readlines()]
stopwords.update(content)

# 创建 WordCloud 对象
wordcloud = WordCloud(width=800,
                      height=400,
                      background_color="white",
                      font_path='C:\Windows\Fonts\STZHONGS.ttf',
                      stopwords=stopwords
                     ).generate(text_data)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# 保存词云图
wordcloud.to_file("wordcloud.png")
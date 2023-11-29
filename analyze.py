# 对posts.josn文件进行分析

import json
import jieba
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image #处理图片

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
# image_mask = Image.open("resources/huaji.jpg")
# print(f"蒙版图片mode: {image_mask.mode}")
# mask = np.array(image_mask)

# 创建 WordCloud 对象
wordcloud = WordCloud(width=480,
                      height=480,
                      #mask=mask,
                      background_color="white",
                      mode="RGB",
                      font_path='C:\Windows\Fonts\STZHONGS.ttf',
                      stopwords=stopwords,
                      max_words=100,
                      relative_scaling=0.8,
                      #contour_width=1,
                     ).generate(text_data)

# image_color = ImageColorGenerator(mask)
# wordcloud.recolor(color_func=image_color)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# 保存词云图
wordcloud.to_file("wordcloud.png")
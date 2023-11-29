# 对posts.josn文件进行分析
import asyncio
import json
import jieba
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image #处理图片
import datetime
from concurrent.futures import ProcessPoolExecutor

# 生成词云
def generate_word_cloud(file_path):
    # 读取json文件
    data = json.load(open(file_path, encoding="utf-8"))

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
                          #mode="RGB",
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
    wordcloud.to_file(f"output/wordcloud_{file_path}.png")

# 根据年份拆分数据,输出到不同的json文件中
def split_data_by_year(file_path):
    # 读取json文件
    with open('output/posts.json', encoding='utf-8') as f:
        data = json.load(f)

    files_data = {}

    def process(item):
        # 由时间戳转换为datetime对象
        create_date = datetime.datetime.fromtimestamp(item["create_time"])
        year = create_date.year
        if year not in files_data.keys():
            files_data[year] = []
        files_data[year].append(item)

    for item in data:
        process(item)

    # 输出到对应的json文件中
    for k,v in files_data.items():
        with open(f"output/post_{k}.json", "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=2)

    # 输出到总的json文件中
    with open(f"output/post_all.json", "w", encoding="utf-8") as f:
        json.dump(files_data, f, ensure_ascii=False, indent=2)

# 根据data生成饼状图
def generate_pie_chart_by_data(data):
    # 统计在每个贴吧的回复数
    stats = {}

    for item in data:
        name = item['forum_name']
        if name not in stats:
            stats[name] = 0
        stats[name] += 1

    # 出于显示美观考虑，将占比小的贴吧合并为其他
    num_labels = 7  # 需要显示的标签数
    # 当贴吧数大于num_labels时
    if len(stats) > num_labels:
        sorted_counts = sorted(stats.values())
        min_count = sorted_counts[-num_labels]
        other_count = 0

        new_stats = {
            k: v for k, v in stats.items() if v >= min_count
        }
        for v in stats.values():
            if v < min_count:
                other_count += v
        new_stats['其他'] = other_count
        stats = new_stats

    # 绘制饼状图
    labels = list(stats.keys())
    sizes = list(stats.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,
            labels=labels,
            #autopct='%1.1f%%',
            pctdistance=0.1,
            labeldistance=1.1,
            shadow=False,
            startangle=90)
    ax1.axis('equal')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # 创建图例
    #plt.legend(labels, loc="best", bbox_to_anchor=(0.5, 0, 0.5, 1))
    return plt

# 由文件生成饼状图
def generate_pie_chart_from_file(file_path):
    # 读取json文件
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    result_plt = generate_pie_chart_by_data(data)
    result_plt.show()

# 为每年的数据生成饼状图
def generate_pie_chart_every_year():
    # 读取json文件
    with open("output/post_all.json", encoding='utf-8') as f:
        data = json.load(f)
    for k,v in data.items():
        result_plt = generate_pie_chart_by_data(v)
        # 设置标题
        result_plt.title(f"{k}年回复贴吧分布")
        # 保存图片
        result_plt.savefig(f"output/pie_{k}.png")
        result_plt.show()


#split_data_by_year("output/posts.json")
#generate_pie_chart_from_file("output/post_2017.json")
generate_pie_chart_every_year()
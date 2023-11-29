from analyze import *

# 处理数据
#split_data_by_year("output/posts.json")

# 从文件生成词云图
#generate_word_cloud_from_file("output/post_2017.json")

# 为每年的数据生成词云图
generate_word_cloud_every_year()

# 从文件生成饼状图
#generate_pie_chart_from_file("output/post_2017.json")

# 为每年的数据生成饼状图
# generate_pie_chart_every_year()
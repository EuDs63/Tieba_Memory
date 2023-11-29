# 数据导出

import asyncio
import json
import aiotieba as tb


async def export():
    async with tb.Client("default") as client:

        # 定义一个异步函数，用于获取fid对应的fname
        async def get_fname_by_fid(fid):
            # 维护一个fid和fname的字典
            fid2fname = {}
            # 如果字典中没有fid对应的fname则获取并添加到字典中
            if fid not in fid2fname:
                fname = await client.get_fname(fid)
                fid2fname[fid] = fname
            # 如果字典中有fid对应的fname则直接返回
            return await client.get_fname(fid)

        # user, posts = await asyncio.gather(client.get_self_info(), client.get_self_posts(200))
        user = await client.get_self_info()
        print(f"当前用户: {user}")

        # 尝试获取用户所有的回复
        # 创建一个空列表，用于存储回复信息的字典
        posts_data = []

        # 初始化页数
        i = 1
        posts = await client.get_self_posts(i)
        # 判断posts是否为空
        while posts:
            # 遍历当前页的所有回复
            for post in posts:
                fid = post.fid  # forum_id 贴吧ID
                #tid = post.tid  # thread_id 主题帖ID
                #pid = post._objs[0].pid  # post_id 回复ID
                text = post._objs[0].text  # 回复内容
                create_time = post._objs[0].create_time  # 回复时间
                # 通过贴吧名获取forum_id
                #forum_name = await client.get_fname(fid)
                forum_name = await get_fname_by_fid(fid)
                # 创建包含回复信息的字典
                post_info = {
                    "forum_name": forum_name,
                    "text": text,
                    "create_time": create_time,
                }

                # 添加字典到列表
                posts_data.append(post_info)

                # 输出至json文件中
                with open(f"output/posts.json", "w", encoding="utf-8") as f:
                    json.dump(posts_data, f, ensure_ascii=False, indent=2)
                # 打印
                #print(f"贴吧: {forum_name}: {text} ")
            print(f"第{i}页的回复获取完成")
            # 页数加1
            i += 1
            # 获取下一页的回复
            print(f"正在获取第{i}页的回复")
            posts = await client.get_self_posts(i)

# 使用asyncio.run执行协程main
asyncio.run(export())
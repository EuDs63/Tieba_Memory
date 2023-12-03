# Function: export thread to json file
# todo：支持图片
# todo：支持楼中楼回复

import asyncio
import json
import aiotieba as tb


def parse_post(post):
    simplified_post = {
        "text": post.contents.text,
        "floor": post.floor
    }
    return simplified_post


async def export_thread(tid, is_only_thread_author=False):
    async with tb.Client("default") as client:
        # 从第一页开始
        pn = 1
        simplified_posts = []
        posts = await client.get_posts(tid,
                                       with_comments=True,
                                       pn=pn,
                                       only_thread_author=is_only_thread_author)
        title = posts.thread.title
        for post in posts:
            simplified_posts.append(parse_post(post))
        pn += 1
        new_posts = await client.get_posts(tid,
                                           with_comments=True,
                                           pn=pn,
                                           only_thread_author=is_only_thread_author)
        # 如果new_posts不与前面的posts相同则继续获取
        while new_posts[-1] != posts[-1]:
            print(posts)
            for post in posts:
                simplified_posts.append(parse_post(post))
            pn += 1
            posts = new_posts
            new_posts = await client.get_posts(tid,
                                               with_comments=True,
                                               pn=pn,
                                               only_thread_author=is_only_thread_author)

        thread = {"title": title, "tid": tid, "posts": simplified_posts}

        # 输出至json文件中
        with open(f"output/thread_{tid}.json", "w", encoding="utf-8") as f:
            json.dump(thread, f, ensure_ascii=False, indent=2)

# asyncio.run(export_thread(8688304649,False))
# asyncio.run(export_thread(8760385814, False))
# asyncio.run(export_thread(8740044935, True))
# asyncio.run(export_thread(8724035093, True))
# asyncio.run(export_thread(8517032917))
# asyncio.run(export_thread(8235788209))

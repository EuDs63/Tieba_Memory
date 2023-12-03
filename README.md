# Tieba_Memory

## 说明
本项目基于以下项目进行修改
[Starry-OvO/aiotieba: Asynchronous I/O Client for Baidu Tieba✨](https://github.com/Starry-OvO/aiotieba)

## 使用方法
1. 安装依赖
  ```shell
  pip install -r requirements.txt
  ```
2. 配置文件 参考[准备工作 - aiotieba](https://aiotieba.cc/tutorial/start/#_6)
3. 导出数据,
  ```shell
  python export.py
  ```
4. 分析数据,根据自己的需要修改`main.py`中的`main`函数
  ```shell
  python main.py
  ```

## todo
- [x] 获取自己近期的贴吧回复，并持久化存储
- [ ] 对回复记录进行统计，
   - [x] 生成“词云”图片
   - [x] 生成“饼状图”图片（按照贴吧进行分类）
   - [ ] 可选择时间段生成图片
- [ ] 导出自己的发帖记录
- [ ] 使用Github Actions定时执行
- [ ] 导出特定帖子的回复记录并进行一定的处理

## Python异步编程
- 参考： [异步编程入门教程 - aiotieba](https://aiotieba.cc/tutorial/async_start/)
- `await`关键字的作用就是执行右侧的可等待对象，并让其当前所处的执行流程挂起以等待右侧的可等待对象给出结果。
- `async`关键字的作用就是将一个函数声明为异步函数，添加了`async`标记的函数都会返回一个可等待对象。
- 异步函数的执行结果是一个协程对象，协程对象可以被`await`关键字挂起。
- 协程（Coroutine）就是可以在中途挂起和恢复执行的函数流程。调用异步函数main所得到的可等待对象main()就是一个协程。

## 参考链接
- [Starry-OvO/aiotieba: Asynchronous I/O Client for Baidu Tieba✨](https://github.com/Starry-OvO/aiotieba)
- [amueller/word_cloud: A little word cloud generator in Python](https://github.com/amueller/word_cloud)
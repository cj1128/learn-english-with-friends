# Learn English with \`Friends\`

**排版好看并且内容准确**的老友记剧本 PDF 文件，用于打印下来学习英语。晚上看剧，早上读英语，幸福生活~

最近开始重温老友记，感觉里面的对话很适合用来练习口语，很地道，早晨读一读更是再好不过。网上搜了一圈，找到的资料排版都很难看，So, Why not 自己弄一个呢。

生成好的 PDF 文件都在 `result` 目录中，注意，因为 [Prince] 的缘故，PDF 文件第一页有 Prince 的水印，虽然可以通过技术手段去除，但是我觉得保留下来更好。

## 剧本参考

- https://fangj.github.io/friends/
- http://www.tvsubtitles.net/tvshow-65-1.html

我在网上并没有找到完全正确的剧本，都有或多或少的瑕疵和错误。因此，最终我使用的剧本是在上面资源的基础上，通过反复听录音一遍遍校对得来的。

一个人的精力实在有限，**欢迎大家 Contribute!**

## 音频

推荐网易云音乐 [老友记全 10 季](https://music.163.com/#/playlist?id=102769145&userid=127057191)。


## PDF 生成

剧本文件名规范：`SxxExx.txt`，例如 `S01E01.txt`。

调用 `generate.py`，输入为文件或目录，结果写入到 `result` 目录中。

```bash
# 输入为某个具体文件
$ ./generate.py src/S01/S01E01.txt
# 输入也可以为一个目录，递归处理目录中的每一个文件
$ ./generate.py src/S01
```

[Prince]: https://www.princexml.com/

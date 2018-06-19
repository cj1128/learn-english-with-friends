# Learn English with \`Friends\`

排版好看的老友记剧本PDF文件，用于打印下来学习英语，晚上看剧，早上朗读，生活多美好。

最近开始重温老友记，感觉里面的对话很适合用来练习口语，很地道，早晨读一读更是再好不过。网上搜了一圈，找到的资料排版都很难看，So, Why not自己弄一个呢。

生成好的PDF文件和音频都在`dist`目录中，注意，因为[Prince]的缘故，PDF文件第一页有Prince的水印，虽然可以通过技术手段去除，但是我觉得保留下来也无伤大雅。

## 资源

- 剧本: https://fangj.github.io/friends/
- 音频: http://x8.tingvoa.com//Sound/meiju/laoyouji/tingvoa.com_{target}.mp3

## PDF生成

调用`generate.py`，输入为文件或目录，结果写入到`dist`目录中，内部使用[Prince]完成PDF渲染。

```bash
# 输入为某个具体文件
$ ./generate.py src/S01/S01E01.txt
# 输入也可以为一个目录，递归处理目录中的每一个文件
$ ./generate.py src/S01
```

## 音频下载

以第一季第一集为例。

```bash
$ wget http://x8.tingvoa.com//Sound/meiju/laoyouji/tingvoa.com_101.mp3 -O dist/S01E01.mp3
```

[Prince]: https://www.princexml.com/

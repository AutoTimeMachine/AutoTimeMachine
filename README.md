# AutoTimeMachine

##这是什么What's this:
这个程序可以根据输入的正确时间轴的SRT文件自动调整输入的ASS文件的时间轴
This program can automatically adjust the timeline of an ASS document by a SRT file.

##For English Users:
I don't think this program is useful for English users LOL

##环境准备
>* 安装python2或3最新版 设置环境变量（python2、3最新64位版本亲测可用）
>* 安装wxpython(方法自己找)
>* 命令提示符里输入 ```pip install chardet```
>* 准备完毕 可以开始使用了

##使用方法
>* 双击```运行.bat```，出现一个窗口
>* 单击窗口顶部第一个按钮，选择时间轴正确的Srt文件
>* 单击第二个按钮，选择待调整的Ass文件
>* 单击第三个按钮，开始转换
>* 转换完毕会弹出窗口可以选择保存位置与文件名
>* 成功

##如何判断是否成功
运行时命令提示符里会出现一些信息，转换完成时会出现succeeded xxx ignored xxx的信息，一般来说succeeded占据1/4左右以上就没问题了

##可以调整的参数
请参考```Core.py```里用```■■■```醒目突出的三条注释部分

##Bug
很可能有bug

##开原协议 Open SourceLicense
WTFPL

##免责
使用本程序一切后果由使用者承担，本软件作者不负任何责任



#声明:
## 1 下载ffmpeg,
下载完到安装目录bin下 将ffmpeg.exe,ffprobe.exe复制到当前目录  
链接 http://ffmpeg.org/download.html
## 2 下载 imagemagick
 https://imagemagick.org/script/download.php#windows  
安装好，修改moviepy包（\Lib\site-packages\moviepy\）中的config_defaults.py文件
改为实际安装路径如
IMAGEMAGICK_BINARY = r"D:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"

安装依赖
pip install -r requirements.txt 


将bgm文件放入bgm目录
将视频文件放入video 
支持多个文件,反正随机选择

运行程序
python mpegGenerator.py



# 思路：

## 生成文案人声文件
人声拼接
ffmpeg -y -ss 00:00:00.0 -t 00:00:59 -i output0.mp3 {} -filter_complex "[1]adelay=0000|0000[del1],[2]adelay=4000|4000[del2],[3]adelay=11000|11000[del3],[4]adelay=15000|15000[del4],[5]adelay=23000|23000[del5],[6]adelay=29000|29000[del6],[7]adelay=34000|34000[del7],[8]adelay=40000|40000[del8], [0][del1][del2][del3][del4][del5][del6][del7][del8]amix=9" test.mp3'
## 合成文案人声语音文件 参数音量大小设置

## 合成bgm
## 混音人声+bgm
## 给视频加背景音乐
## 给视频加字幕


ffmpeg -i in.mp4 -c:v copy -an -y nosound.mp4
用无声音的添加bgm
>ffmpeg -i nosound.mp4 -i test.mp3 -t 43 -c:v copy  -y out_bgm.mp4

收集人声后先拼接:
ffmpeg -y -ss 00:00:00.0  -i temp0.mp3 -i temp1.mp3 -i temp2.mp3 -i temp3.mp3 -i temp4.mp3 -i temp5.mp3 -i temp6.mp3 -i temp7.mp3 -i temp8.mp3 -filter_complex "[0]adelay=4000|4000[del0],[1]adelay=7000|7000[del1],[2]adelay=10000|10000[del2],[3]adelay=11000|12000[del3],[4]adelay=15000|15000[del4],[5]adelay=23000|23000[del5],[6]adelay=29000|29000[del6],[7]adelay=34000|34000[del7],[8]adelay=40000|40000[del8],[del0][del1][del2][del3][del4][del5][del6][del7][del8]amix=9" test.mp3
增加音量
ffmpeg  -i test.mp3  -filter:a "volume=20dB" -y speech.mp3
与bgm合并
ffmpeg -y -i speech.mp3  -i bgm_volume.mp3   -filter_complex amix=inputs=2:duration=first:dropout_transition=2  000.mp3



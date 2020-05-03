# -*- encoding: utf-8 -*-
'''
@File    :   mpegGenerator.py
@Time    :   2020/05/02 20:43:17
@Author  :   JiahuaLink
@Version :   1.0
@Contact :   840132699@qq.com
@License :   (C)Copyright 2020, Liugroup-NLPR-CASIA
@Desc    :  营销号生成器
'''


import json
import random
import shutil
import subprocess
import threading

from moviepy.editor import *

from huaweicloud_sis.bean.sis_config import SisConfig
from huaweicloud_sis.bean.tts_request import TtsRequest
from huaweicloud_sis.client.tts_client import TtsClient
from huaweicloud_sis.exception.exceptions import (ClientException,
                                                  ServerException)


def text2speech(text, out_file):
    """ 语音合成demo """
    ak = 'GVOC7YSBOBAO3VZ38TPW'
    sk = 'EpbGXUHTHoffHjj07W8UNWsGhxNEnEPESp7Gr6Qj'
    region = 'cn-north-1'     # region，如cn-north-1
    path = out_file       # 保存路径，需要具体到音频文件，如D:/test.wav，可在设置中选择不保存本地

    # step1 初始化客户端
    config = SisConfig()
    config.set_connect_timeout(10)       # 设置连接超时
    config.set_read_timeout(10)         # 设置读取超时
    # 设置代理，使用代理前一定要确保代理可用。 代理格式可为[host, port] 或 [host, port, username, password]
    # config.set_proxy(proxy)
    tts_client = TtsClient(ak, sk, region, sis_config=config)

    # step2 构造请求
    tts_request = TtsRequest(text)
    # 设置请求，所有参数均可不设置，使用默认参数
    # 设置发声人，默认xiaoyan，xiaoqi 正式女生xiaoyu正式男生xiaoyan情感女生xiaowang童声
    tts_request.set_voice_name('xiaoyan')
    # 设置采样率，默认8k
    tts_request.set_sample_rate('8k')
    # 设置音量，[-20, 20]，默认0
    tts_request.set_volume(0)
    # 设置音高, [-500, 500], 默认0
    tts_request.set_pitch_rate(2)
    # 设置音速, [-500, 500], 默认0
    tts_request.set_speech_speed(-10)
    # 设置是否保存，默认False
    tts_request.set_saved(True)
    # 设置保存路径，只有设置保存，此参数才生效
    tts_request.set_saved_path(path)

    # # step3 发送请求，返回结果,格式为json. 如果设置保存，可在指定路径里查看保存的音频
    try:
        result = tts_client.get_tts_response(tts_request)
    except ClientException as e:
        print(e)
    except ServerException as e:
        print(e)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    print("已合成"+path)


def generate_copywriting_text():
    body = '罗志祥'
    thing = '经常多人运动'
    other_word = '王者五排开黑'
    text = '''{0}{1}是怎么回事呢？
{0}相信大家都很熟悉
但是{0}{1}是怎么回事呢？
下面就让小编带大家一起了解吧
{0}{1}，其实就是{2}
大家可能会很惊讶{0}怎么会{1}呢？
但事实就是这样
小编也感到非常惊讶
这就是关于{0}{1}的所有事情了
大家有什么想法呢？
欢迎在评论区告诉小编,一起讨论吧！
'''.format(body, thing, other_word)
    with open(copywriting_text, encoding='utf-8-sig', mode='w') as f:
        f.write(text)


def generate_speech_audio(volume):
    '''合成人声 参数 :音量大小'''
    speech_infos = []
    # 语音播放的时间坐标:毫秒
    play_index = 1000
    # 停顿时间:毫秒
    pause = 1000
    input_files = ''
    delindex = ''
    filter_complex = ''
    tempfile = os.path.join(temp_path, 'speech.wav')
    with open(copywriting_text, encoding='utf-8-sig') as f:
        for index, line in enumerate(f.readlines()):
            speechfile = os.path.join(temp_path, 'speech{}.wav'.format(index))
            text2speech(line, speechfile)
            seconds = int(get_audio_length(speechfile)*1000)
            # 语音文本信息 文件，开始播放时间，持续时间，播放内容
            temp = [speechfile, play_index, seconds, line]
            speech_infos.append(temp)
            play_index += seconds + pause

    # 合成人声
    for index, speech_info in enumerate(speech_infos):
        input_files += ' -i {}'.format(speech_info[0])
        delindex += '[del{}]'.format(index)
        play_index = speech_info[1]
        filter_complex += '[{0}]adelay={1}|{1}[del{0}],'.format(
            index, play_index)

    compose_cmd = 'ffmpeg -y -ss 00:00:00.0 {} -filter_complex "{} {}amix={}" -b:a 320k {}'.format(
        input_files, filter_complex, delindex, len(speech_infos), speech_file)
    # print(mixing_cmd)
    subprocess.call(compose_cmd, shell=True)
    print("已合成人声"+tempfile)

    # 调节人声音量
    print("调节人声音量")
    cmd = 'ffmpeg -y -i {tempfile} -vcodec copy -af "volume={volume}dB" -b:a 320k {speech_vol}'.format(
        tempfile=tempfile, volume=volume, speech_vol=speech_vol)
    subprocess.call(cmd, shell=True)

    return speech_infos


def get_audio_length(filename):
    # wav时间长度
    #print('获取音频文件长度'+ filename)
    command = ["ffprobe.exe", "-loglevel", "quiet", "-print_format",
               "json", "-show_format", "-show_streams", "-i", filename]
    result = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    temp = str(out.decode('utf-8'))
    data = json.loads(temp)["format"]['duration']
    return float(data)


def getLength(filename):
    command = ["ffprobe.exe", "-loglevel", "quiet", "-print_format",
               "json", "-show_format", "-show_streams", "-i", filename]
    result = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    temp = str(out.decode('utf-8'))
    try:
        data = json.loads(temp)['streams'][1]['width']
    except:
        data = json.loads(temp)['streams'][0]['width']
    return data


def getLenTime(filename):
    command = ["ffprobe.exe", "-loglevel", "quiet", "-print_format",
               "json", "-show_format", "-show_streams", "-i", filename]
    result = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    temp = str(out.decode('utf-8'))
    data = json.loads(temp)["format"]['duration']
    return data


def generate_bgm_audio(volume):
    '''参数 :音量大小'''

    cut_temp = os.path.join(temp_path, 'cut_temp.wav')
    total_time = getLenTime(speech_file)
    print("剪切bgm的长度和人声长度一致")
    cmd = 'ffmpeg -y -i {wav} -ss 00:00:00.0 -t {time} -acodec copy {cut_temp}'.format(
        wav=bgmfile, time=total_time, cut_temp=cut_temp)
    subprocess.call(cmd, shell=True)
    # 调节bgm音量
    print("获取bgm_vol.wav完成")
    cmd = 'ffmpeg -y -i {cut_temp} -vcodec copy -af "volume={volume}dB" -b:a 320k {bgm_vol}'.format(
        cut_temp=cut_temp, volume=volume, bgm_vol=bgm_vol)
    subprocess.call(cmd, shell=True)


def mix_audio():
    '''合成音频  背景音乐+人声'''
    cmd = 'ffmpeg -y -i {speech} -i {bgm} -filter_complex amix=inputs=2:duration=first:dropout_transition=2 -b:a 320k {output_wavfile}'.format(
        speech=speech_vol, bgm=bgm_vol, output_wavfile=output_wavfile)
    subprocess.call(cmd, shell=True)


def video_add_bgm():
    nosound_file = os.path.join(temp_path, 'nosound.mp4')
    total_time = getLenTime(speech_file)
    # 先把视频无声
    nosound_cmd = 'ffmpeg -i {input_file} -c:v copy -an -y {nosound_file}'.format(
        input_file=input_file, nosound_file=nosound_file)
    subprocess.call(nosound_cmd, shell=True)
    # 再将无声音的添加bgm
    mixing_cmd = 'ffmpeg -i {output_wavfile} -i {nosound_file}  -t {time} -y {video_notext_file}'.format(
        output_wavfile=output_wavfile, nosound_file=nosound_file, time=total_time, video_notext_file=video_notext_file)
    subprocess.call(mixing_cmd, shell=True)


def video_add_subtitle(speech_infos):
    '''生成字幕文件'''
    # 字幕颜色
    color = 'white'
    # 字体
    font = 'SimHei'
    # 水平对齐方式
    align = 'center'
    # 字幕位置
    position = ("center", "bottom")
    # 字体大小
    fontsize = 25
    # 字幕
    txts = []
    # z字幕偏移值 单位秒
    offset = 0
    # 台词列表
    sentences = []
    # 剪辑的源视频
    video1 = VideoFileClip(video_notext_file)
    for speech_info in speech_infos:
        start = int(speech_info[1]/1000 + offset)
        span = int(speech_info[2]/1000)
        sentence = speech_info[3]
        txt = (TextClip(sentence, fontsize=fontsize, align=align, color=color, font=font)
               .set_position(position).set_duration(span).set_start(start))
        txts.append(txt)
    video2 = CompositeVideoClip([video1, *txts])
    video2.write_videofile(ouput_file)


def random_choose_file(path):
    fileList = os.listdir(path)
    filePath = os.path.join(path, random.sample(fileList, 1)[0])
    print("choose :"+filePath)
    return filePath


def clean_tempfile():
    '''清理临时文件'''
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

def init(temp_path):
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)


if __name__ == '__main__':
    # 文案生成
    
    root_dir = os.path.abspath('.')
    bgm_path = os.path.join(root_dir, 'bgm')
    video_path = os.path.join(root_dir, 'video')
    temp_path = os.path.join(root_dir, 'temp')
    output_Path = os.path.join(root_dir, 'output')

    init(temp_path)

    copywriting_text = os.path.join(temp_path, "copywriting")
    speech_file = os.path.join(temp_path, "speech.wav")
    output_wavfile = os.path.join(temp_path, 'mixed.wav')
    video_notext_file = os.path.join(temp_path, 'video_notext.mp4')
    speech_vol = os.path.join(temp_path, 'speech_vol.wav')
    bgm_vol = os.path.join(temp_path, 'bgm_vol.wav')

    bgmfile = random_choose_file(bgm_path)
    input_file = random_choose_file(video_path)

    ouput_file = os.path.join(output_Path, 'output.mp4')
    # 生成文案人声文件
    generate_copywriting_text()
    # 合成文案人声语音文件 参数音量大小设置
    speech_infos = generate_speech_audio(20)
    # 合成bgm
    generate_bgm_audio(0)
    # 混音人声+bgm
    mix_audio()
    # 给视频加背景音乐
    video_add_bgm()
    # 给视频加字幕
    video_add_subtitle(speech_infos)
    # 清理缓存
    clean_tempfile()

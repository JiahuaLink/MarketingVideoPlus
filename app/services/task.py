from os import path

from loguru import logger

from app.config import config
from app.models.schema import VideoParams, VoiceNames
from app.services import llm, material, voice, video, subtitle
from app.utils import utils


def _parse_voice(name: str):
    # "female-zh-CN-XiaoxiaoNeural",
    # remove first part split by "-"
    if name not in VoiceNames:
        name = VoiceNames[0]

    parts = name.split("-")
    _lang = f"{parts[1]}-{parts[2]}"
    _voice = f"{_lang}-{parts[3]}"

    return _voice, _lang


async def start(task_id, params: VideoParams):
    """
    {
        "video_subject": "",
        "video_aspect": "横屏 16:9（西瓜视频）",
        "video_sources": "douyin",
        "voice_name": "女生-晓晓",
        "enable_bgm": false,
        "font_name": "STHeitiMedium 黑体-中",
        "text_color": "#FFFFFF",
        "font_size": 60,
        "stroke_color": "#000000",
        "stroke_width": 1.5
    }
    """
    logger.info(f"开始任务: {task_id}")
    video_subject = params.video_subject
    video_aspect = params.video_aspect
    video_sources = params.video_sources
    video_amounts = params.video_amounts
    logger.info(f"视频比例：{video_aspect}")
    logger.info(f"视频素材来源：{video_sources}")
    voice_name, language = _parse_voice(params.voice_name)
    logger.info(f"声音音色：{voice_name} 语言：{language}")
    paragraph_number = params.paragraph_number
    logger.info(f"生成段落数：{paragraph_number}")
    n_threads = params.n_threads
    logger.info(f"执行线程数：{paragraph_number}")
    logger.info("\n\n## llm生成视频脚本文案")
    script = llm.generate_script(video_subject=video_subject, language=language, paragraph_number=paragraph_number)
    logger.info("\n\n## 生成视频文案关键词")
    search_terms = llm.generate_terms(video_subject=video_subject, video_script=script,video_sources=video_sources, amount=video_amounts)
    script_file = path.join(utils.task_dir(task_id), f"script.json")
    script_data = {
        "script": script,
        "search_terms": search_terms
    }
    logger.info("\n\n## 保存视频文案至script.json")
    with open(script_file, "w") as f:
        f.write(utils.to_json(script_data))
    logger.info("\n\n## 保存视频文案成功")
    audio_file = path.join(utils.task_dir(task_id), f"audio.mp3")
    subtitle_path = path.join(utils.task_dir(task_id), f"subtitle.srt")

    logger.info("\n\n## 生成视频文案音频")
    sub_maker = await voice.tts(text=script, voice_name=voice_name, voice_file=audio_file)
    subtitle_provider = config.app.get("subtitle_provider", "").strip().lower()
    logger.info(f"\n\n## 开始拆分文本生成字幕，采用模式: {subtitle_provider}")
    if subtitle_provider == "edge":
        voice.create_subtitle(text=script, sub_maker=sub_maker, subtitle_file=subtitle_path)
    if subtitle_provider == "whisper":
        subtitle.create(audio_file=audio_file, subtitle_file=subtitle_path)
        logger.info("\n\n## 更正字幕ing")
        subtitle.correct(subtitle_file=subtitle_path, video_script=script)
    logger.info("\n\n## 下载视频ing...")
    video_paths = material.download_videos(task_id=task_id, search_terms=search_terms,
                                           video_aspect=params.video_aspect,
                                           video_sources=params.video_sources,
                                           wanted_count=20,
                                           minimum_duration=5,
                                           video_amounts=video_amounts)

    logger.info("\n\n## 组合视频片段")
    combined_video_path = path.join(utils.task_dir(task_id), f"combined.mp4")
    video.combine_videos(combined_video_path=combined_video_path,
                         video_paths=video_paths,
                         audio_file=audio_file,
                         video_aspect=params.video_aspect,
                         max_clip_duration=5,
                         threads=n_threads)

    final_video_path = path.join(utils.task_dir(task_id), f"final.mp4")

    bgm_file = video.get_bgm_file(bgm_name=params.bgm_name)
    logger.info("\n\n## 生成视频")
    # Put everything together
    video.generate_video(video_path=combined_video_path,
                         audio_path=audio_file,
                         subtitle_path=subtitle_path,
                         output_file=final_video_path,
                         video_aspect=params.video_aspect,
                         threads=n_threads,
                         font_name=params.font_name,
                         fontsize=params.font_size,
                         text_fore_color=params.text_fore_color,
                         stroke_color=params.stroke_color,
                         stroke_width=params.stroke_width,
                         bgm_file=bgm_file
                         )
    logger.start(f"视频任务 {task_id} 已完成")
    return {
        "video_file": final_video_path,
    }

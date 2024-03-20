import json
import random
import re
import time
from urllib.parse import quote

import requests
from typing import List
from loguru import logger

from app.config import config
from app.models.schema import VideoAspect, VideoSource
from app.utils import utils

requested_count = 0
pexels_api_keys = config.app.get("pexels_api_keys")
if not pexels_api_keys:
    raise ValueError("pexels_api_keys is not set, please set it in the config.toml file.")


def round_robin_api_key():
    global requested_count
    requested_count += 1
    return pexels_api_keys[requested_count % len(pexels_api_keys)]


def search_videos(search_term: str,
                  wanted_count: int,
                  minimum_duration: int,
                  video_aspect: VideoAspect = VideoAspect.portrait,
                  video_sources: VideoSource = VideoSource.pexels,

                  locale: str = "zh-CN"
                  ) -> List[str]:
    aspect = VideoAspect(video_aspect)
    video_orientation = aspect.name
    video_width, video_height = aspect.to_resolution()
    if video_sources == VideoSource.pexels.value:
        return search_video_by_pexels(search_term, video_orientation, locale, wanted_count, minimum_duration,
                                      video_width, video_height)
    elif video_sources == VideoSource.douyin.value:
        return search_video_by_douyin(search_term, video_orientation, locale, wanted_count, minimum_duration,
                                      video_width, video_height)


def search_video_by_pexels(search_term: str,
                           video_orientation: str,
                           locale: str,
                           wanted_count: int,
                           minimum_duration: int,
                           video_width: int,
                           video_height: int):
    """"""
    headers = {
        "Authorization": round_robin_api_key()
    }
    proxies = config.pexels.get("proxies", None)
    # Build URL
    query_url = f"https://api.pexels.com/videos/search?query={search_term}&per_page=15&orientation={video_orientation}&locale={locale}"
    logger.info(f"搜索视频素材: {query_url}")
    # Send the request
    r = requests.get(query_url, headers=headers, proxies=proxies, verify=False)

    # Parse the response
    response = r.json()
    video_urls = []

    try:
        videos_count = min(len(response["videos"]), wanted_count)
        # loop through each video in the result
        for i in range(videos_count):
            # check if video has desired minimum duration
            if response["videos"][i]["duration"] < minimum_duration:
                continue
            video_files = response["videos"][i]["video_files"]
            # loop through each url to determine the best quality
            for video in video_files:
                # Check if video has a valid download link
                # if ".com/external" in video["link"]:
                w = int(video["width"])
                h = int(video["height"])
                if w == video_width and h == video_height:
                    video_urls.append(video["link"])
                    break

    except Exception as e:
        logger.error(f"search videos failed: {e}")

    return video_urls


def save_video(video_url: str, save_dir: str) -> str:
    video_id = f"vid-{str(int(time.time() * 1000))}"
    video_path = f"{save_dir}/{video_id}.mp4"
    proxies = config.pexels.get("proxies", None)
    with open(video_path, "wb") as f:
        f.write(requests.get(video_url, proxies=proxies, verify=False).content)

    return video_path


def search_video_by_douyin(search_term: str,
                           video_orientation: str,
                           locale: str,
                           wanted_count: int,
                           minimum_duration: int,
                           video_width: int,
                           video_height: int):
    video_urls = []
    keywords = search_term
    print(f'下载抖音短视频 {search_term}')
    search_keywords = quote(search_term)
    url = f'https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&sort_type=0&publish_time=0&keyword={search_keywords}&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=15&pc_client_type=1&version_code=190600&version_name=19.6.0&cookie_enabled=true&screen_width={video_width}&screen_height={video_height}&browser_language={locale}&browser_platform=MacIntel&browser_name=Chrome&browser_version=113.0.0.0&browser_online=true&engine_name=Blink&engine_version=113.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=1.5&effective_type=3g&round_trip_time=550&webid=7238040438824306235'
    headers = {
        'authority': 'www.douyin.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'referer': 'https://www.douyin.com/search/%E7%83%AD%E9%97%A8?publish_time=0&sort_type=0&source=switch_tab&type=video',
        'cookie': 'douyin.com; s_v_web_id=verify_la7udy4g_4IJtmDpB_v6m8_4L0B_Bsm6_JAEMoLsxhKys; passport_csrf_token=186b7bcfd87f579c60a67d35f19fe9c1; passport_csrf_token_default=186b7bcfd87f579c60a67d35f19fe9c1; csrf_session_id=4f9475d4dbe24d70951c1ada6262a645; n_mh=WZp_FTaGhpNn8yHatnPpROsyat9W3gqOXXseck3zZew; passport_assist_user=CkGpXg5PjkXenQdbIfAgyoZnxyLMvFdP9N558Zx5Nak4vHJQmG27Tw9zZGbXr7VwzxaofcX1d7h6vGroV0fCIEa3yRpICjwBAfTlznkiNfqFj7y2NZ7yGaxIfiKBrB1YZCC1s_o4FmDJGO0VHqijEoigOJmrSbL55xijP2-5wFcx-vgQgvqgDRiJr9ZUIgEDWoDktQ%3D%3D; sso_uid_tt=11a6396bb5f53d6368b87fb650c85097; sso_uid_tt_ss=11a6396bb5f53d6368b87fb650c85097; toutiao_sso_user=6b166f85e829446968ce4fe951c6382b; toutiao_sso_user_ss=6b166f85e829446968ce4fe951c6382b; sid_ucp_sso_v1=1.0.0-KGNhZjYwNTY2NmI0MWQ5ZGVkNzI4YWExYTNlMGE4NDVjNmU1ZjUwMmUKHwjN8OCa7o39BRDyprmbBhjvMSAMMJbsuJcGOAZA9AcaAmxmIiA2YjE2NmY4NWU4Mjk0NDY5NjhjZTRmZTk1MWM2MzgyYg; ssid_ucp_sso_v1=1.0.0-KGNhZjYwNTY2NmI0MWQ5ZGVkNzI4YWExYTNlMGE4NDVjNmU1ZjUwMmUKHwjN8OCa7o39BRDyprmbBhjvMSAMMJbsuJcGOAZA9AcaAmxmIiA2YjE2NmY4NWU4Mjk0NDY5NjhjZTRmZTk1MWM2MzgyYg; passport_auth_status=040a2071608b8cf84c84b159c68dcd13%2Cd3437ad9218fc0a4fdaf64f3ae07cea9; passport_auth_status_ss=040a2071608b8cf84c84b159c68dcd13%2Cd3437ad9218fc0a4fdaf64f3ae07cea9; sid_guard=0e9c88492704dba9770c668cfb3ad65d%7C1668174708%7C5183998%7CTue%2C+10-Jan-2023+13%3A51%3A46+GMT; uid_tt=e3bf5c655838577b69114b35d1fc1835; uid_tt_ss=e3bf5c655838577b69114b35d1fc1835; sid_tt=0e9c88492704dba9770c668cfb3ad65d; sessionid=0e9c88492704dba9770c668cfb3ad65d; sessionid_ss=0e9c88492704dba9770c668cfb3ad65d; sid_ucp_v1=1.0.0-KDZiZDgxN2Q0YTc4NzZhY2ZhN2Y1OTMzMDQ2MjU5MmYyYzE0Yjc5NjEKGQjN8OCa7o39BRD0prmbBhjvMSAMOAZA9AcaAmhsIiAwZTljODg0OTI3MDRkYmE5NzcwYzY2OGNmYjNhZDY1ZA; ssid_ucp_v1=1.0.0-KDZiZDgxN2Q0YTc4NzZhY2ZhN2Y1OTMzMDQ2MjU5MmYyYzE0Yjc5NjEKGQjN8OCa7o39BRD0prmbBhjvMSAMOAZA9AcaAmhsIiAwZTljODg0OTI3MDRkYmE5NzcwYzY2OGNmYjNhZDY1ZA; ttwid=1%7CZJz8d7FMqSJauHQkZnXbfmEtX7U7VowfL4lrIHwxIrE%7C1669004154%7C1107c4182cf17778481cd718ed28fb50f32ef9d098167791279861fe527ee897; __ac_nonce=0637c2160001170e5b63a; __ac_signature=_02B4Z6wo00f01V9PI7AAAIDA1AS4U-D7XYVfbycAADSzKczKBkyLvUAJNT6gj4DHSBXo3JZ5DGKB3F2LjzMBzivdhNTUAWMwnPtZsqawVprpEIRbHLmyEM-dJB1PI1V6UatVyuQfUM-HZZ2wd3; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAlQ5yVlHkiaeoD0B0cS8JhPr3Rxq5X_L0rDXxt7DzRz13Mi6zuxv-Ig7cdtGdafPu%2F1669132800000%2F0%2F1669079409144%2F0%22; odin_tt=f7aa3135bb330c04a7d48dabecf474e0f2b15128c53fddb3ffbe4dc6098c583f2fb44d4dc8585abfaf0e9e18e0166bad; download_guide=%223%2F20221122%22; SEARCH_RESULT_LIST_TYPE=%22single%22; strategyABtestKey=%221669079772.107%22; msToken=G0-VTpRTq_f0OfV55_jAA5SMdpLeJy2zaB9NTjYB9SaSBRZfuNgcJ24UvdlIhKbb0ZN_f3YPxNcDfnShM4DI2unCBrPSycENSffVdHSphvcbqmxvZpwxLw==; msToken=Tj_LIlFpENGTrN5F0qzmbEe_bKv9OehazbEF4OEiRR_JKzAwNME_ZcsPzpI4CYqnVtzQppea9wjeYwhFNLtF4Xq3YliI2fliX_lxrtMu1K8AwXW_WWOfCA==; tt_scid=XdZaOsCXffhbGXRHfYqV3ZH7u538K.HV-IMI4C1koLPSjUCKCdu2QvefnvhkeFEL64f5; home_can_add_dy_2_desktop=%220%22'
    }
    res = simple_get(url=url, headers=headers)
    # del cookies['douyin.com']
    # print(cookies)
    # with open('tiktok.json', 'w', encoding='utf-8')as f:
    #     f.write(res)
    # input(':::')
    has_more = 0
    if res is not None:
        target = json.loads(res)
        if target['status_code'] < 300:
            if 'has_more' in target.keys():
                if target['has_more'] == 1:
                    has_more = 1
            videos = target['data']
            results = []
            videos_count = min(len(videos), wanted_count)
            for video in videos[:videos_count]:
                video = video.get('aweme_info')
                if not video:
                    continue
                temp = {}
                temp['keywords'] = keywords
                temp['video_id'] = video['aweme_id']
                temp['video_pic'] = video['video']['cover']['url_list'][0]
                temp['video_title'] = video['desc']
                if re.search(r'(.+?)#', video['desc']):
                    temp['video_title'] = re.search(r'(.+?)#', video['desc']).group(1)
                elif re.search(r'(.+?)@', video['desc']):
                    temp['video_title'] = re.search(r'(.+?)@', video['desc']).group(1)
                else:
                    pass
                temp['video_playtime'] = None
                temp['video_watch_num'] = video['statistics']['digg_count']
                temp['video_h5_url'] = video['video']['play_addr']['url_list'][-1]
                temp['width'] = video['video']['play_addr']['width']
                temp['height'] = video['video']['play_addr']['height']
                format = video['video'].get('format')
                w = int(temp["width"])
                h = int(temp["height"])
                temp['video_datafrom'] = '抖音'
                temp['video_update_time'] = time.time()
                temp['audio_url'] = None
                temp['video_url'] = temp['video_h5_url']
                if w == video_width and h == video_height:
                    video_urls.append(temp['video_h5_url'])
                    # print(f'抖音获取视频素材链接成功! {url}')
                    results.append(temp)
            return video_urls
        else:
            raise Exception(f'tiktok: 更新: {search_keywords} 失败!!! 接口返回异常')
    else:
        raise Exception(f'tiktok: 更新: {search_keywords} 失败!!! 请检查接口')


def simple_get(url, headers, cookies=None, proxy=None):
    # url = url.replace('https://', 'http://')
    for i in range(3):
        try:
            if proxy:
                if cookies:
                    res = requests.get(url=url, headers=headers, cookies=cookies)
                else:
                    res = requests.post(url=url, headers=headers, proxies=proxy)
            else:
                if cookies:
                    res = requests.get(url=url, headers=headers, cookies=cookies)
                else:
                    res = requests.get(url=url, headers=headers)
            if res.status_code < 300:
                # data = json.loads(res.text)
                # if data['status'] == 0 or data['status'] == '0':

                # print('res.text: ', res.text)
                return res.text
                # else:
                #     print(f'请求 {url} 响应异常: {res.text}, 开始重试, 重试次数:{i + 1}')
                #     continue
            else:
                print(f'抖音下载请求响应异常  {url} 状态码为: {res.status_code} {res.text}, 开始重试, 重试次数:{i + 1}')
                time.sleep(random.uniform(0.5, 1))
                continue
        except Exception as e:
            print(f'douyin请求 {url} 发生错误, 开始重试, 重试次数:{i + 1} error: {e}')
            time.sleep(random.uniform(0.5, 1))
            continue
    raise Exception(f'接口: {url} 异常, 终止任务!')


def download_videos(task_id: str,
                    search_terms: List[str],
                    video_aspect: VideoAspect = VideoAspect.portrait,
                    video_sources: VideoSource = VideoSource.pexels,
                    wanted_count: int = 15,
                    minimum_duration: int = 5,
                    video_amounts: int = 5
                    ) -> List[str]:
    valid_video_urls = []
    video_concat_mode = config.pexels.get("video_concat_mode", "")

    for search_term in search_terms:
        # logger.info(f"searching videos for '{search_term}'")
        video_urls = search_videos(search_term=search_term,
                                   wanted_count=wanted_count,
                                   minimum_duration=minimum_duration,

                                   video_aspect=video_aspect,
                                   video_sources=video_sources)
        logger.info(f"关键词 {search_term} 发现 {len(video_urls)} 个视频素材")

        i = 0
        for url in video_urls:
            if video_concat_mode == "random":
                url = random.choice(video_urls)

            if url not in valid_video_urls:
                valid_video_urls.append(url)
                i += 1

            if i >= 3:
                break

    logger.info(f"获取视频素材: {len(valid_video_urls)}个")
    video_paths = []
    save_dir = utils.task_dir(task_id)
    for video_url in valid_video_urls:
        try:
            logger.info(f"下载视频素材: {video_url}")
            saved_video_path = save_video(video_url, save_dir)
            video_paths.append(saved_video_path)
            logger.info(f"下载视频素材完成，已保存路径: {video_paths}")
        except Exception as e:
            logger.error(f"下载视频失败: {video_url}, {e}")
    logger.success(f"已下载视频素材完成 {len(video_paths)} 个")
    return video_paths

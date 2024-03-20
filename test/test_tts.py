# -- coding: utf-8 --
# @Time : 2024/3/18 10:14
# @Author : JiahuaLInk
# @Email : 840132699@qq.com
# @File : test_tts.py
# @Software: PyCharm
#!/usr/bin/env python3

"""
Basic example of edge_tts usage.
"""

import asyncio

import edge_tts

TEXT = "注意看这个男人叫做小帅!"
VOICE = "zh-CN-YunjianNeural"
OUTPUT_FILE = "test.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()
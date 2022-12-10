import time
import speech_recognition as sr
import logging
from multiprocessing import Process, Value
from aip import AipSpeech
from tkinter import *

logging.basicConfig(level=logging.DEBUG)


def function(n):
    # n.value = 1
    root = Tk()
    numIdx = 6  # gif的帧数
    # 填充6帧内容到frames
    frames = [PhotoImage(file='fan.gif', format='gif -index %i' % i) for i in range(numIdx)]

    def update(idx):  # 定时器函数
        frame = frames[idx]
        idx += int(n.value)  # 下一帧的序号：在0,1,2,3,4,5之间循环(共6帧)
        label.configure(image=frame)  # 显示当前帧的图片
        root.after(100, update, idx % numIdx)  # 0.1秒(100毫秒)之后继续执行定时器函数(update)

    label = Label(root)
    label.pack()
    root.after(0, update, 0)  # 立即启动定时器函数(update)
    root.mainloop()


if __name__ == '__main__':
    Switch = Value('d', 0)
    p = Process(target=function, args=(Switch,))
    p.start()
    # 此处填写百度短语音在线识别平台的AppID,API Key,Secret Key
    BAIDU_APP_ID = '28728033'
    BAIDU_API_KEY = 'byG5yX4YPPYZg09oD9ixbmKF'
    BAIDU_SECRET_KEY = '4vFLMVeNBof1Qw821bQPjUWFGjuZ3kjy'
    aip_speech = AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
    r = sr.Recognizer()
    # 麦克风
    mic = sr.Microphone(sample_rate=16000)
    while True:
        logging.info('录音中...')
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        logging.info('录音结束，识别中...')
        start_time = time.time()
        #print(type(audio))
        audio_data = audio.get_wav_data()
        #print(type(audio_data))
        # 识别本地文件
        ret = aip_speech.asr(audio_data, 'wav', 16000, {'dev_pid': 1536, })
        # print(ret)
        if ret and ret['err_no'] == 0:
            result = ret['result'][0]
            print("语音识别结果为:" + str(result))
            if result in ["开机", "开启风扇", "启动", "开始", "开","开始风扇"]:
                Switch.value = 1
            elif result in ["关机", "关闭风扇", "结束", "关", "关风扇", "关闭","结束风扇"]:
                Switch.value = 0
            end_time = time.time()
            # print(end_time - start_time)
        else:
            print(ret['err_msg'])
        logging.info('end')
    p.join()

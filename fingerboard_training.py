# -*- coding: utf-8 -*-
"""
@author: UndefinedAlan
"""

import pyaudio,threading,queue
import random,time,sys
import numpy as np
from scipy import signal

print('欢迎使用指板精通配套训练\n练习前请校准您的琴弦\n本程序由吉他程序员小伟设计制作并保留最终解释权\n')
print('请选择练习模式:\n1:一弦特训\n2:二弦特训\n3:三弦特训\n4:四弦特训\n5:五弦特训\n6:六弦特训\n7:综合训练\n')
print('说明：按回车查看答案，输入q后回车退出程序!')
mode = ['一弦特训','二弦特训','三弦特训','四弦特训','五弦特训','六弦特训','综合训练']

board = [[ 5, 7, 8,10, 0, 1, 3],
         [10, 0, 1, 3, 5, 6, 8],
         [ 2, 4, 5, 7, 9,10, 0],
         [ 7, 9,10, 0, 2, 3, 5],
         [ 0, 2, 3, 5, 7, 8,10],
         [ 5, 7, 8,10, 0, 1, 3]]

scales = ['A','B','C','D','E','F','G']

board_freq = np.array([[329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.26],  #1
                       [246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],  #2
                       [196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00],  #3
                       [146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66],      #4
                       [110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00],      #5
                       [ 82.41,  87.31,  92.50,  98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81] ] )    #6

freq_table = np.array([   82.41,  87.31,  92.50,  98.00, 103.83, 110.00, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56,
                          164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13,
                          329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25,
                          659.26, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77,1046.50,1108.73,1174.66,1244.51] )

board_dict = ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb',
              'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb',
              'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb',
              'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb']


string_ = 0
scale_ = 0
scale = 0
string = 0
count = 0
max_freq = 0

CHUNK = 20000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
data = []
DF = RATE / CHUNK
frames = []
counter = 1

rt_data = np.arange(0, CHUNK, 1)
fft_data = np.arange(0, CHUNK / 2 + 1, 1)

# pyaudio
p = pyaudio.PyAudio()
q = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    global ad_rdy_ev

    q.put(in_data)
    ad_rdy_ev.set()
    if counter <= 0:
        return (None, pyaudio.paComplete)
    else:
        return (None, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)

stream.start_stream()

# processing block
window = signal.hamming(CHUNK)
def read_audio_thead(q, stream, frames, ad_rdy_ev):
    global rt_data
    global fft_data
    global max_freq

    while stream.is_active():
        ad_rdy_ev.wait(timeout=1000)
        if not q.empty():
            # process audio data here
            data = q.get()
            while not q.empty():
                q.get()
            rt_data = np.frombuffer(data, np.dtype('<i2'))
            rt_data = rt_data * window
            fft_temp_data = (np.fft.fft(rt_data) * 2 / CHUNK).reshape(CHUNK, 1)
            fft_data = np.abs(fft_temp_data[0:int(CHUNK / 2) + 1])
        ad_rdy_ev.clear()


ad_rdy_ev = threading.Event()

t = threading.Thread(target=read_audio_thead, args=(q, stream, frames, ad_rdy_ev))

t.daemon = True
t.start()

try:
    train_mode = int(input('请选择练习模式'))-1
    print('您的选择为 %s 现即将开始'%mode[train_mode])
except:
    sys.exit()
    print('输入不合理!请重启程序')

while(True):
    if(train_mode < 6):
        string = train_mode
    else:
        while string_ == string:
            string = random.randrange(0,6)
    while scale_ == scale:
        scale = random.randrange(0,7)
    pos = board[string][scale]
    check = False
    print('请弹奏 %d 弦的 %s 音'%(string+1,scales[scale]))
    while(check == False):
        if np.max(fft_data) > 100:
            max_freq = np.argmax(fft_data) * DF  # max value index
            minn = np.argmin(np.abs(freq_table - max_freq))

            if board_dict[minn] == scales[scale]:
                count = count + 1
                if count >= 2:
                    break
            else:
                count = 0
                print('\r您弹错了哦，您弹得是%s，需要弹奏的是%s' % (board_dict[minn],scales[scale]),end=' ')
                #dest_freq = board_freq[string][pos]
                #print(max_freq, dest_freq,end=' ')
    print('\n正确',end=' ')
    print('请记住 %s 位置是 %d 弦的 %d 品\n' % (scales[scale] ,string+1, board[string][scale]))
    time.sleep(1)
    print('下一题：',end=' ')
    string_ = string
    scale_ = scale

stream.stop_stream()
stream.close()
p.terminate()
print('吉他程序员小伟祝您生活愉快，琴技飙升！\n')


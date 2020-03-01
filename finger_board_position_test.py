import random,time

scale_board = [
    ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#'],         #一弦
    ['B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#'],         #二弦
    ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#'],         #三弦
    ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#'],         #四弦
    ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],         #四弦
    ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#'],         #六弦
]

answer = False
cnt = 0
amount = 0
amount_time = 0
right = 0
while True:
    string = random.randrange(0,6)
    step = random.randrange(0,12)
    cnt += 1
    while True:
        tic = time.time()
        print('第'+str(amount)+'题：'+ str(string+1) + '弦', end='')
        if step == 0:
            a = input('空弦音名为：')
        else:
            a = input(str(step)+'品音名为：')
        if a == scale_board[string][step]:
            toc = time.time()
            print('回答正确！耗时%.2fs'%(toc-tic))
            amount_time += toc-tic
            amount += 1
            right += 1
            break
        else:
            amount += 1
            print('回答错误！请重新作答！')
    print('已答%d道题，答对%d道题，正确率%2.2f，答对平均用时:%.2fs\n'%(amount,right,right/amount*100,amount_time/right))


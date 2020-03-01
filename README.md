# Guitar_Training_Assistant
作为一个硬件开发攻城狮，兼前任某学生乐队主音吉他手，兼冷门B站UP主( https://space.bilibili.com/22604808 )  等等~
制作了一套基于Python(大概)的吉他辅助练习程序，持续更新中！
后续应该会推出基于electron的集成工具箱或者小程序开发，大概~

Python还需要一些依赖库(主要是scipy)，安装完python之后启动命令行，输入pip install scipy即可，有能力的自己打一下~

<a href="https://github.com/boyoffreedom/Guitar_Training_Assistant/blob/master/finger_board_position_test.py">指板位置对应音名测试</a>   ：计算机提问某弦某品，回答音名
<a href="https://github.com/boyoffreedom/Guitar_Training_Assistant/blob/master/fingerboard_training.py">音名对应指板位置</a>   ：计算机提问某弦上的某音，通过弹奏该弦上的音自动判别，需要打scipy库
<a href="https://github.com/boyoffreedom/Guitar_Training_Assistant/blob/master/scales_table.py">音阶生成</a>    ：采用映射的方式，生成音阶表

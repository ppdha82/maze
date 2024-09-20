# Micro Mouse Simulator with python

2012년 쯤 지인의 추천으로 일본 Micro Mouse 동영상을 보고, 대학 시절 만들었던 마이크로 마우스가 생각나서 Python 언어로 제작한 Micro Mouse Simulator 프로그램이다. 두 바퀴 이동체의 방정식을 사용해서 물리적 이동과 시간 계산을 하고, 실제로 물리좌표에 그리는 방식을 사용하였다. wxPython FloatCanvas(http://wiki.wxpython.org/FloatCanvas) 모듈을 사용하여 floating point 좌표계를 사용하여 정밀하게 그리려다 보니, FloatCanvas 모듈의 드로잉 속도가 너무 느려서 Override 하여 조금 수정하여 사용하였다. 이로 인해 드로잉 속도는 빨라졌으나 확대 축소, 화면 이동, 드로잉 캔버스 이동 등에는 화면이 깨지는 현상이 발생할 수 있다. 독자적인 미로 파일 포멧을 만들고, 16x16 기본 크기와 32x32 half 미로를 지원하고, 미로 편집/저장을 지원한다.

* YouTube
  * [16x16 Maze Video] (https://www.youtube.com/watch?v=iUsBkwjv6jI)
  * [32x32 Maze Video] (https://www.youtube.com/watch?v=m84Ez6tAGA0)
* License
  * [GNU GPLv3]: http://www.gnu.org/licenses/gpl.html

* Troubleshoot
  * python 버전(3.8)과 pip 버전(3.6)이 다를 경우 numpy 에러 발생

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/numpy/core/__init__.py", line 16, in <module>
    from . import multiarray
ImportError: cannot import name 'multiarray' from partially initialized module 'numpy.core' (most likely due to a circular import) (/usr/lib/python3/dist-packages/numpy/core/__init__.py)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "maze.py", line 21, in <module>
    from    scipy import integrate
  File "/usr/lib/python3/dist-packages/scipy/__init__.py", line 61, in <module>
    from numpy import show_config as show_numpy_config
  File "/usr/lib/python3/dist-packages/numpy/__init__.py", line 142, in <module>
    from . import add_newdocs
  File "/usr/lib/python3/dist-packages/numpy/add_newdocs.py", line 13, in <module>
    from numpy.lib import add_newdoc
  File "/usr/lib/python3/dist-packages/numpy/lib/__init__.py", line 8, in <module>
    from .type_check import *
  File "/usr/lib/python3/dist-packages/numpy/lib/type_check.py", line 11, in <module>
    import numpy.core.numeric as _nx
  File "/usr/lib/python3/dist-packages/numpy/core/__init__.py", line 26, in <module>
    raise ImportError(msg)
ImportError: 
Importing the multiarray numpy extension module failed.  Most
likely you are trying to import a failed build of numpy.
If you're working with a numpy git repo, try `git clean -xdf` (removes all
files not under version control).  Otherwise reinstall numpy.

Original error was: cannot import name 'multiarray' from partially initialized module 'numpy.core' (most likely due to a circular import) (/usr/lib/python3/dist-packages/numpy/core/__init__.py)

  * wxPython 설치
    * https://life-is-sad-or-bad.tistory.com/77
    * pip install wxPython

Traceback (most recent call last):
  File "maze.py", line 25, in <module>
    import  wx
ModuleNotFoundError: No module named 'wx'

  * scipy 설치
    * sudo apt install python3-scipy
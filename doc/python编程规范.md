# 经验之谈
- 在元素比较多的时候(超过5个)不要用%表示格式，容易漏，且不好维护
- 在指定输出的长度的时候只能用%
- 在单双引号嵌套的时候用%要方便一些
- 用多行字符串或者列表表示要好维护一些

# import

import module
关键字 模块名

示例：
import math         # 导入math模块
math.floor()        # 调用math模块中的floor()函数


from module import name
关键字 模块名 关键字 方法名

示例：
from math import floor         # 导入math模块中的floor函数方法
floor()                        # 调用floor()函数方法

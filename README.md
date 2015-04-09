# PyTTF
A python library to read TTF font file


Inspired by [https://github.com/ynakajima/ttf.js](https://github.com/ynakajima/ttf.js)

实现了字体一些信息的读取和字体码点的解析。字形等解析都没有做。
打算用在[IconFont](https://github.com/JohnWong/IconFont)项目中，像Android的R类一样生成字体中Unicode列表放到项目里。方便管理字体图标，防止出现缺失的情况。
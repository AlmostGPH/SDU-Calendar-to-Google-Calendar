# SDU-Calendar-to-Google-Calendar
将山东大学课程表加载到谷歌日历的解决办法

# 效果展示

谷歌日历：
![](https://s2.loli.net/2025/02/26/rOAauBiYDeVq1G2.png)

以及所有能应用谷歌日历的场景：
- Notion:
- ![](https://s2.loli.net/2025/02/26/7CH38wzGp2gUaWJ.png)
- Obsidian:
- ![](https://s2.loli.net/2025/02/26/Ja6bTmtxXqu1zYN.png)


# 使用步骤

## 在智慧教学服务平台下载你的课表

![](https://s2.loli.net/2025/02/26/1eKRfMyXk8GSYDT.png)

## 将下载的xls文件保存为csv文件：
![](https://s2.loli.net/2025/02/26/zZi8IvMgTteuadH.png)
**注意保存的时候不要选择带有 `UTF-8` 字样的编码格式**
> 或者你自己去修改脚本中的读取文件的编码格式

## 运行脚本

```bash
python script.py -c 你的csv文件路径
```
脚本会提示你输入本学期第一天的日期，格式为 `2025-02-26`，然后会在当前目录下生成一个 `google_calendar.csv` 文件:

![](https://s2.loli.net/2025/02/26/ZhFAJNT6Wzvkim1.png)

## 将课程文件上传Google Calendar

![](https://s2.loli.net/2025/02/26/DlX962nIiC31uSA.png)

![](https://s2.loli.net/2025/02/26/GhtpIPjeszudHYV.png)

等待上传完毕，你的Google Calendar中就会出现你的山大课程表了
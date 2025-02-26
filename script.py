import csv
import datetime
import re
from dateutil.parser import parse
import argparse

def parse_weeks(week_str):
    """解析周数字符串，返回周数列表"""
    week_str = re.sub(r'第|\s|周', '', week_str)
    weeks = []
    
    for part in week_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            weeks.extend(range(start, end+1))
        elif part:
            weeks.append(int(part))
    
    return sorted(list(set(weeks)))

def get_time_slot(time_slot_name):
    """获取时间段对应的时间"""
    time_map = {
        "第一节\n(01,02小节)": ("08:00 AM", "10:00 AM"),
        "第二节\n(03,04小节)": ("10:00 AM", "12:00 PM"),
        "第三节\n(05,06小节)": ("02:00 PM", "04:00 PM"),
        "第四节\n(07,08小节)": ("04:00 PM", "06:00 PM"),
        "第五节\n(09,10,11小节)": ("07:00 PM", "09:00 PM")
    }
    return time_map.get(time_slot_name.strip(), ("", ""))

def main():
    # 用户输入学期开始日期
    start_date_str = input("请输入学期开始的第一天（格式：YYYY-MM-DD）：")
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    
    events = []
    
    # 读取课表CSV文件
    parser = argparse.ArgumentParser(description='Process course schedule.')
    parser.add_argument('-c', '--csv', type=str, required=True, help='Path to the course schedule CSV file')
    args = parser.parse_args()

    with open(args.csv, 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        
        # 跳过前3行标题
        for _ in range(3): next(reader)
        
        for row in reader:
            if len(row) < 8: continue
            
            time_slot = row[0].strip()
            start_time, end_time = get_time_slot(time_slot)
            if not start_time: continue
            
            # 处理每周的课程
            for day_idx in range(7):  # 0=周一, 6=周日
                cell = row[day_idx + 1].strip()
                if not cell: continue
                
                # 分割不同课程（空行分隔）
                for course_block in cell.split('\n\n'):
                    lines = [l.strip() for l in course_block.split('\n') if l.strip()]
                    if len(lines) < 5: continue
                    
                    # 解析课程信息
                    if len(lines) <= 6:
                        course_name = lines[0]
                        teacher = lines[3] if len(lines) >=4 else ""
                        week_info = lines[4].split('([周])')[0].strip()
                        location = lines[5] if len(lines) >=6 else ""
                    else:
                        course_name = lines[0]
                        teacher = lines[4] if len(lines) >=5 else ""
                        week_info = lines[5].split('([周])')[0].strip()
                        location = lines[6] if len(lines) >=7 else ""

                    
                    # 解析周数
                    try:
                        weeks = parse_weeks(week_info)
                    except:
                        continue
                    
                    # 生成每个周的事件
                    for week in weeks:
                        # 计算日期偏移量
                        date_offset = (week-1)*7 + day_idx
                        event_date = start_date + datetime.timedelta(days=date_offset)
                        
                        events.append({
                            'Subject': course_name,
                            'Start Date': event_date.strftime('%m/%d/%Y'),
                            'Start Time': start_time,
                            'End Date': event_date.strftime('%m/%d/%Y'),
                            'End Time': end_time,
                            'Location': location,
                            'Description': f'教师: {teacher}'
                        })
    
    # 写入Google Calendar CSV
    with open('google_calendar.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 
            'Location', 'Description'
        ])
        writer.writeheader()
        writer.writerows(events)


    print('已生成 google_calendar.csv 文件')

if __name__ == '__main__':
    main()
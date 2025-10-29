import datetime

def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    # ✅ 输入验证：结束时间必须晚于开始时间
    if end_time_s <= start_time_s:
        raise ValueError(f"end_time ({end_time}) must be after start_time ({start_time})")
    # 这一行是计算每个小区间的长度（秒）
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    # 等价于
    # sec_range = []
    # for i in range(number_of_intervals):
    # start = start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s)
    # end   = start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s)
    # sec_range.append((start, end))
    # | i | 计算公式                             | 含义      | 结果       |
    #| - | -------------------------------- | ------- | -------- |
    # | 0 | start = 10:00:00 + (0*d + 0*gap) | 第 1 段开始 | 10:00:00 |
    # |   | end = 10:00:00 + (1*d + 0*gap)   | 第 1 段结束 | 10:10:00 |
    # | 1 | start = 10:00:00 + (1*d + 1*gap) | 第 2 段开始 | 10:11:00 |
    # |   | end = 10:00:00 + (2*d + 1*gap)   | 第 2 段结束 | 10:21:00 |
    # | 2 | start = 10:00:00 + (2*d + 2*gap) | 第 3 段开始 | 10:22:00 |
    # |   | end = 10:00:00 + (3*d + 2*gap)   | 第 3 段结束 | 10:32:00 |
    # 最终结果是
    #[(10:00:00, 10:10:00),
    # (10:11:00, 10:21:00),
    # (10:22:00, 10:32:00)]

    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]

# 把一个时间段（start_time → end_time）分成 number_of_intervals 个小时间段。
# 还可以在每个小时间段之间留出一个“间隔”（gap）。
# 正常的逻辑应该是：每段长度 = 总时长减去所有间隔时间，再除以区间数。
# 例如:d = ((end_time_s - start_time_s).total_seconds() - gap_between_intervals_s * (number_of_intervals - 1)) / number_of_intervals


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            overlap_time.append((low, high))
    return overlap_time
  # 计算两个时间区间集合中每一对区间的重叠时间范围。
  # 它无论是否真的有重叠，都会 append (low, high)。
  # low  = max('10:00', '12:00') → '12:00'
  # high = min('11:00', '13:00') → '11:00'
  # ('2010-01-12 12:00:00', '2010-01-12 11:00:00')
  # 显然是一个无效区间（结束时间比开始时间早



  # 当你执行 python times.py 时 —— 这三行代码会运行。
  # 当你在 test_times.py 里 import times 时 —— 它不会运行。
if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))
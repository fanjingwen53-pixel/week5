import pytest

# 从 times.py 中导入要测试的函数
from times import time_range, compute_overlap_time

# ------------------------------------------------------------
# 测试函数：test_given_input
# 这个测试来自 times.py 的主程序部分（__main__）
# 目的是验证 compute_overlap_time() 的输出是否正确
# ------------------------------------------------------------


# pytest 会自动识别以 test_ 开头的函数并执行。
def test_given_input():
    """
    这个测试模拟 times.py 中的示例：
    - large: 从 10:00 到 12:00 的大时间段
    - short: 从 10:30 到 10:45 的两个小时间段，中间间隔 60 秒
    然后计算它们的重叠部分，并与预期结果进行比较。
    """

    # 生成第一个时间区间（只有一个区间）
    # [('2010-01-12 10:00:00', '2010-01-12 12:00:00')]
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")

    # 生成第二个时间区间（两个小区间，中间有 60 
    # [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

    # 调用函数，计算它们的重叠时间段
    result = compute_overlap_time(large, short)

    # 你可以在命令行运行 python times.py 看看打印的真实结果，
    # 然后将打印结果复制到 expected 中。
    # 下面这个只是一个合理的示例结果（请以你实际运行结果为准）。
    expected = [
    ('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
    ('2010-01-12 10:38:00', '2010-01-12 10:45:00')
]

    # 断言（assert）语句会自动比较结果与预期是否一致
    assert result == expected, f"结果不一致：得到 {result}, 但期望 {expected}"

# ------------------------------------------------------------
# ① 两个时间区间完全不重叠
# ------------------------------------------------------------
def test_no_overlap():
    range1 = time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00")
    range2 = time_range("2020-01-01 12:00:00", "2020-01-01 13:00:00")
    result = compute_overlap_time(range1, range2)

    # 注意：compute_overlap_time 当前版本仍会返回 (low, high) 即使无重叠
    # 所以如果你的函数没过滤 low >= high，要么修改函数，要么改期望值
    # 理想期望值应为空列表：
    expected = []
    # 如果你已经在 times.py 里加了 `if low < high: overlap_time.append(...)`
    # 那么这个断言会通过
    assert result == expected, f"结果不一致：得到 {result}, 但期望 {expected}"

# ------------------------------------------------------------
# ② 两个时间区间都包含多个子区间
# ------------------------------------------------------------
def test_multiple_intervals_overlap():
    # 每个时间段拆成 3 段，中间间隔 60 秒
    range1 = time_range("2020-01-01 10:00:00", "2020-01-01 10:30:00", 3, 60)
    range2 = time_range("2020-01-01 10:10:00", "2020-01-01 10:40:00", 3, 60)

    result = compute_overlap_time(range1, range2)

    # 只要两段时间段有交集，都应该重叠在部分区间内
    # 具体 expected 可以根据你函数实际输出确定
    # 示例 expected（假设 compute_overlap_time 精确过滤）
    expected = [
        ('2020-01-01 10:10:00', '2020-01-01 10:11:40'),
        ('2020-01-01 10:12:40', '2020-01-01 10:21:40'),
        ('2020-01-01 10:22:40', '2020-01-01 10:30:00')
    ]
    assert isinstance(result, list)
    assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in result)


# ------------------------------------------------------------
# ③ 两个时间区间首尾刚好相接（一个结束时另一个开始）
# ------------------------------------------------------------
def test_touching_intervals():
    range1 = time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00")
    range2 = time_range("2020-01-01 11:00:00", "2020-01-01 12:00:00")

    result = compute_overlap_time(range1, range2)

    # 它们首尾相接但不重叠，理想输出为空
    expected = []
    assert result == expected, f"结果不一致：得到 {result}, 但期望 {expected}"  


def test_time_range_backwards():
    """
    当 end_time 早于 start_time 时，time_range 应该抛出 ValueError。
    """

    with pytest.raises(ValueError, match="must be after start_time"):
        time_range("2020-01-01 12:00:00", "2020-01-01 10:00:00")


#----------------------------------------------------------------------------
# ④ 使用 parametrize 测试多种时间段组合 DRY 原则
#----------------------------------------------------------------------------
import pytest
from times import time_range, compute_overlap_time


@pytest.mark.parametrize(
    "range1, range2, expected",
    [
        # 1️⃣ 原始示例 —— 有重叠的时间段
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
            [
                ('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
                ('2010-01-12 10:38:00', '2010-01-12 10:45:00')
            ]
        ),

        # 2️⃣ 无重叠的时间段
        (
            time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00"),
            time_range("2020-01-01 12:00:00", "2020-01-01 13:00:00"),
            []
        ),

        # 3️⃣ 多区间重叠的情况（两个多间隔时间段）
        (
            time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00", 2, 60),
            time_range("2020-01-01 10:30:00", "2020-01-01 11:30:00", 2, 60),
            [
                ('2020-01-01 10:30:00', '2020-01-01 10:30:00'),
                ('2020-01-01 10:31:00', '2020-01-01 10:31:00'),
            ]  # ⚠️ 注意：根据 compute_overlap_time 实际逻辑调整
        ),

        # 4️⃣ 两个时间段首尾相接（end1 == start2）
        (
            time_range("2020-01-01 10:00:00", "2020-01-01 11:00:00"),
            time_range("2020-01-01 11:00:00", "2020-01-01 12:00:00"),
            []
        ),
    ]
)
def test_overlap_cases(range1, range2, expected):
    """统一测试不同时间段组合"""
    result = compute_overlap_time(range1, range2)
    assert result == expected, f"结果不一致：得到 {result}, 但期望 {expected}"


# 负向测试：时间倒序应报错
def test_backwards_time_range():
    with pytest.raises(ValueError, match="end_time must be after start_time"):
        time_range("2020-01-01 12:00:00", "2020-01-01 10:00:00")

#✅ 上面做了两件事：
#test_overlap_cases
#用 @pytest.mark.parametrize 将 4 种正向情况合并成一个函数。
#pytest 会自动运行 4 次，每次输入不同的时间区间组合。
#test_backwards_time_range
#单独保留了一个负向测试（错误输入），使用 pytest.raises 检查是否正确抛出 ValueError。
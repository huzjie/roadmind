"""数据集加载示例。"""
from roadmind.data.dataset import DrivingDataset

ds = DrivingDataset("./data/images")
print("帧数:", len(ds))
if len(ds):
    print("首帧:", type(ds[0]))

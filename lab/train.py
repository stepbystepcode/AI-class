# https://docs.ultralytics.com/modes/train
from ultralytics import YOLO

# https://universe.roboflow.com/roboflow-universe-projects/safety-cones-vfrj2
# 加载预训练模型
model = YOLO('yolo11n.pt')

# 训练配置
results = model.train(
    # 基础训练设置
    data="datasets/data.yaml",
    epochs=100,

    # 硬件优化参数
    device=[0,1],  # 使用两张GPU
    batch=32,      # 每张GPU的batch size，实际总batch为64
    workers=8,     # CPU工作线程数，根据CPU核心数设置

    # 性能优化参数
    amp=True,      # 启用自动混合精度训练
    cache=True,    # 启用数据缓存以减少IO开销

    # 图像处理设置
    imgsz=640,     # 训练图像大小

    # 保存和验证设置
    save=True,
    save_period=10,  # 每10个epoch保存一次
    val=True         # 启用验证
)

## 计算机视觉 · 图像生成

这个实现用单通道的 28 × 28 图像训练 U-Net。阅读脚本时，可以沿着三个函数看清一张图如何被加噪，又如何从噪声开始逐步生成。

- `q_sample` 按时间步给输入图像加入高斯噪声。脚本使用线性 β 调度，共 200 步。
- `p_losses` 把带噪图像和时间步交给 U-Net，让它预测刚才加入的噪声。训练循环选择 Huber 损失。
- `p_sample_loop` 从随机噪声开始，按时间步倒序调用 `p_sample`。每一步的预测都是下一步的输入。

## 源码与 Notebook

<a href="/assets/source/diffusionDemo.py" download>下载完整 Python 脚本</a> · [打开 Jupyter Notebook](https://github.com/river-ya/Deep-Learning-Note/blob/039f854e2bb3ecf5bf51f75f7b42dd93539587b6/paper_reproduction/diffusionDemo/diffusonDemo.ipynb) · [查看仓库中的 Python 原件](https://github.com/river-ya/Deep-Learning-Note/blob/039f854e2bb3ecf5bf51f75f7b42dd93539587b6/paper_reproduction/diffusionDemo/diffusionDemo.py) · [依赖清单](https://github.com/river-ya/Deep-Learning-Note/blob/039f854e2bb3ecf5bf51f75f7b42dd93539587b6/paper_reproduction/diffusionDemo/requirements.txt)

源码取自 river-ya/Deep-Learning-Note，版本 `039f854`，提交日期为 2026-10-23。

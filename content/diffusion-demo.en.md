## Computer vision · Image generation

The script trains a U-Net on 28 × 28 grayscale images. Three functions trace the path from a clean training image to the reverse sampling loop.

- `q_sample` adds Gaussian noise for a given timestep. The script uses a linear beta schedule with 200 steps.
- `p_losses` asks the U-Net to predict the injected noise from the noisy image and timestep. The training loop selects Huber loss.
- `p_sample_loop` starts with random noise and calls `p_sample` in reverse timestep order, passing each prediction to the next step.

## Source and notebook

<a href="/assets/source/diffusionDemo.py" download>Download the Python script</a> · [Open the Jupyter notebook](https://github.com/river-ya/Deep-Learning-Note/blob/039f854e2bb3ecf5bf51f75f7b42dd93539587b6/paper_reproduction/diffusionDemo/diffusonDemo.ipynb) · [Python source on GitHub](https://github.com/river-ya/Deep-Learning-Note/blob/039f854e2bb3ecf5bf51f75f7b42dd93539587b6/paper_reproduction/diffusionDemo/diffusionDemo.py) · [Dependencies](https://github.com/river-ya/Deep-Learning-Note/blob/039f854e2bb3ecf5bf51f75f7b42dd93539587b6/paper_reproduction/diffusionDemo/requirements.txt)

Source revision `039f854` in river-ya/Deep-Learning-Note, committed on October 23, 2026.

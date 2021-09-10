# Sentiment-Trading-Bots
A variety of stock/cryptocurrency trading bots that use NLP and Sentiment analysis to make orders
Only the reddit and twitter bots have been uploaded so far.

<h1>Prerequisites</h1>

```
pip install python-binance praw textblob tensorflow ta ernie torch
```

I reccommend using an anaconda environment with this, but naturally, these bots work with anything.

Additionally, should you be running this on a local device, I recommend having a CUDA enabled GPU and
all the relevant CUDA and cudnn files installed. It <i>will</i> run on a CPU, but not as fast

I will not take any responsibility for any profits/losses incurred by any third party using these bots

<h1>Built Using</h1>
<ul>
  <li><a href="https://pandas.pydata.org/">Pandas</a> - a data handling package</li>
  <li><a href="https://www.tensorflow.org/">Tensorflow</a> - a deep learning framework built by Google</li>
  <li><a href="https://pytorch.org/">PyTorch</a> - a deep learning framework built by Facebook</li>
  <li><a href="https://github.com/labteral/ernie">Ernie</a> a BERT based sentence classification package built on the Keras API</li>
  <li><a href="https://praw.readthedocs.io/en/stable/#">PRAW</a> - the python reddit API wrapper</li>
  <li><a href="https://python-binance.readthedocs.io/en/latest/">python-binance</a> the python binance API wrapper</li>
  <li><a href="https://developer.nvidia.com/cuda-zone">CUDA</a> - a parallel computing platform and programming model developed by Nvidia for computing on GPUs</li>
  <li><a href="https://developer.nvidia.com/cudnn">cuDNN</a> - a GPU accelerated library for Deep Neural Networks based on CUDA</li>
</ul>

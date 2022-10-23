# File: assign_class_tags.py
# Goal: asign class tags to each figure from texts, and plot statistics

import argparse
import json
import os
import timeit
from collections import Counter
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

start = timeit.default_timer()

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')

args = parser.parse_args()

ROOT_PATH = args.path_data
PARSED_DATA_PATH = os.path.join(ROOT_PATH, 'parsed')  # Already parsed by Grobid
PROCESSED_DATA_PATH = os.path.join(ROOT_PATH, 'paper2figure')
JSON_DIR = os.path.join(PROCESSED_DATA_PATH, 'json_data')
IMAGES_DIR = os.path.join(PROCESSED_DATA_PATH, 'figures')
OUT_PATH = 'output'


def normalize_text(text):
    lower_string = text.lower()
    no_number_string = re.sub(r'\d+', '', lower_string)
    no_punc_string = re.sub(r'[^\w\s]', '', no_number_string)
    no_wspace_string = no_punc_string.strip()
    return no_wspace_string

# This tags are obtained after a word-frequency analysis on captions
architecture_types = {
    'cnn': ['cnn', 'convolutional', 'convnet', 'convolution', 'conv2d', 'resnet', 'vgg', 'mobilenet', 'efficientnet',
            'inceptionV', 'conv', 'kernels',
            'alexnet'],
    'encoder': ['encoder', 'encoding', 'encoded', 'encodes'],
    'attention': ['attention'],
    'embedding': ['embedding', 'embeddings', 'descriptor', 'embedded'],
    'sequence': ['sequence', 'sequences', 'token', 'tokens'],
    'latent': ['latent'],
    'pooling': ['pooling'],
    'temporal': ['temporal'],
    'fusion': ['fusion', 'fuse'],
    'unet': ['unet'],
    'mapping': ['mapping'],
    'rnn': ['rnn', 'recurrent neural', ' gru ', '(gru)', 'recurrent'],
    'softmax': ['softmax'],
    'lstm': ['lstm', 'long-short term'],
    'transformer': ['transformer', ' bert ', ' bart ', 't5', 'self-attention', 'cross-attention'],
    'contrastive': ['triplet', 'siamese', 'contrastive'],
    'gan': ['gan', 'discriminator', 'adversarial', 'gan', 'discriminative'],
    'reconstruction': ['reconstruction'],
    'svm': ['svm', 'support vector'],
    'mlp': [' mlp ', '(mlp)', 'dnn', 'feed forward', 'multi layer perceptron', 'linear layer'],
    'vae': ['vae', 'variational autoencoder', 'autoencoder'],
    'supervised': ['supervised'],
    'generative': ['generative'],
    'translation': ['translation'],
    'upsampling': ['upsampling'],
    'skip': ['skip'],
    'alignment': ['alignment'],
    'crossmodal': ['crossmodal'],
    'bilinear': ['bilinear'],
    'nas': ['nas'],
    'perceptron': ['perceptron'],
    'mse': ['mse'],
    'alexnet': ['alexnet'],
    'resnet': ['resnet'],
    'vgg': ['vgg'],
    'clip': ['clip'],
    'encoderdecoder': ['encoderdecoder'],
    'rcnn': ['rcnn', 'r-cnn', 'yolo'],
    'nlp': ['nlp', 'natural language', 'language model'],
    'rl': ['reinforcement', 'Q-Learning', 'rl'],
    'clustering': ['cluster', 'kmeans', 'k-means', 'k means'],
    'diffusion': ['diffusion', 'ddpm'],
    'distillation': ['teacher', 'student', 'distill'],
    'gnn': ['gnn', 'graph neural network', 'graph network'],
    'graphs': ['graphs'],
    'crossentropy': ['entropy'],
    'decoders': ['decoders'],
    'quantization': ['quantization'],
    'dilated': ['dilated'],
    'gcn': ['gcn'],
    'variational': ['variational'],
    'denoising': ['denoising'],
    'adam': ['adam'],
    'siamese': ['siamese'],
    'clouds': ['clouds'],
    'mnist': ['mnist'],
    'gru': ['gru'],
    'selfsupervised': ['selfsupervised'],
    'sigmoid': ['sigmoid'],
    'bidirectional': ['bidirectional'],
    'compression': ['compression'],
    'maxpooling': ['maxpooling'],
    'bert': ['bert'],
    'imagenet': ['imagenet'],
    'cifar': ['cifar'],
    'pyramid': ['pyramid'],
    'dnn': ['dnn'],
    'multimodal': ['multimodal']
}

import pickle
def main() -> None:
    # Loop over figures json data
    dict_class_architectures = {}
    [dict_class_architectures.setdefault(i, 0) for i in architecture_types.keys()]

    try:
        with open('data.p', 'rb') as fp:
            dict_class_architectures = pickle.load(fp)
    except:

        for paper in tqdm(os.listdir(JSON_DIR)):
            with open(os.path.join(JSON_DIR, paper)) as f:
                paper_data = json.load(f)
                if not paper_data:
                    continue
                for fig_data in paper_data:
                    for caption in fig_data['captions']:
                        types = []
                        cap = normalize_text(caption)
                        for type in architecture_types:
                            if any(name in cap for name in architecture_types[type]):
                                # types.append(type)
                                dict_class_architectures[type] += 1

    dict_class_architectures ={k: v for k, v in sorted(dict_class_architectures.items(), key=lambda item: item[1],reverse=True)}
    labels, values = zip(*dict_class_architectures.items())
    # labels = [f'20{l}' if l is not 22 else f'April\n 20{l}' for l in labels]

    sns.set_style({'font.family': 'serif'})
    sns.set(font_scale=4)
    ax = sns.barplot(x=list(labels), y=list(values), color='gray')
    plt.xlabel('Architecture tags', fontsize=13)
    plt.ylabel('Number of figures', fontsize=13)
    plt.setp(ax.get_xticklabels(), rotation=80, fontsize=11)
    plt.setp(ax.get_yticklabels(), fontsize=11)
    plt.yticks(range(0, max(values), 5000))
    plt.show()

    stop = timeit.default_timer()
    print('Time: ', stop - start)


if __name__ == "__main__":
    main()

# File: construct_dataset.py
# Created by Juan A. Rodriguez on 02/11/2022
# Goal: (Step 4) - Perform the split of the dataset and store in train and val json files
# Output: At the end of this process you will have a directory 'json_data' with text pairs 
# and metadata for each figure in json format (on json per figure) 

import argparse
import json
import os
from tqdm import tqdm
import re

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path_data', type=str, default=None, required=True,
                    help='Path where the data is stored')
args = parser.parse_args()

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

def normalize_texts_scipdf(text):
    lower_string = text.lower()
    citation_token_string = re.sub(r'\[.+\]', 'citation-tk', lower_string) # Manage citations
    number_token_string = re.sub(r'[+-]?((\d+(\.\d+)?)|(\.\d+)|(\d[-/]\d))[ .:\n,]', 'number-tk ', citation_token_string) # Manage numbers
    no_weird_dots = re.sub(r' +\.', '.', number_token_string) # Manage weird dots
    no_weird_symbols = re.sub(r'(• ?)|(@)', '', no_weird_dots) # Manage weird symbols
    no_double_spaces = re.sub(r'  ', ' ', no_weird_symbols) # Manage double spaces
    no_wspace_string = no_double_spaces.strip()
    return no_wspace_string

def normalize_texts_galai(text):
    lower_string = text.lower()
    citation_token_string = re.sub(r'\[.+\]', '[START_REF][END_REF]', lower_string) # Manage citations
    no_weird_dots = re.sub(r' +\.', '.', citation_token_string) # Manage weird dots like ' .' -> '.'
    no_weird_symbols = re.sub(r'(•)|(@)|(\?)', '', no_weird_dots) # remove stop symbols
    no_double_spaces = re.sub(r'  ', ' ', no_weird_symbols) # Manage double spaces
    no_wspace_string = no_double_spaces.strip()
    return no_wspace_string

def remove_duplicates_from_list(lst):
    result = []
    for element in lst:
        if element not in result:
            result.append(element)
    return result

def get_figure_type(texts):
    types = []
    for text in texts:
        for type in architecture_types:
            if any(name in text.lower() for name in architecture_types[type]):
                types.append(type)
        # Remove duplicates
    types = remove_duplicates_from_list(types)
    return types

def ocr_result_to_string(ocr_res):
    ocr_string_with_coords = ""
    for item in ocr_res['ocr_result']:
        ocr_string_with_coords += f'{item}'
    return ocr_string_with_coords

def main():
    ROOT_PATH = args.path_data
    OCR_OUT_DIR = os.path.join(ROOT_PATH, 'ocr_results_2') # ocr_results_2 is the more updated dir, ocr_results is the v1
    splits = ['train', 'test']
    for split in splits:
        data_split = []
        with open(os.path.join(ROOT_PATH, f'{split}_data.json')) as f:
            data = json.load(f)
        for fig in tqdm(data):    
            figure_id = fig['figure_id']
            try:
                with open(os.path.join(OCR_OUT_DIR, figure_id + '.json')) as f:
                    ocr_result = json.load(f)

                # Process ocr to string with coords
                ocr_with_coords = ocr_result_to_string(ocr_result)

                # Extract architecture tags
                types = get_figure_type(fig['captions'] + [ocr_with_coords])

                ob = {
                    "figure_id" : figure_id,
                    "captions" : fig['captions'],
                    "captions_scipdf" : [normalize_texts_scipdf(text) for text in fig['captions']],
                    "captions_galai" : [normalize_texts_galai(text) for text in fig['captions']],
                    "ocr_result": ocr_result,
                    "ocr_with_coords":ocr_with_coords,
                    "class_tag": types,
                    "aspect": round(fig['aspect'], 2)
                }
                data_split.append(ob)
            except:
                continue

        with open(os.path.join(ROOT_PATH, f"paper2fig_{split}.json"), "w") as f:
            json.dump(data_split, f)

if __name__ == '__main__':
    main()
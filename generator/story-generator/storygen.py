"""
Story generator based on textgenrnn
"""

from textgenrnn import textgenrnn


def cleantext(text):
    """
    
    """
    print("Start Cleaning")


def generate():
    textgen = textgenrnn(weights_path='colaboratory_weights.hdf5',
                        vocab_path='colaboratory_vocab.json',
                        config_path='colaboratory_config.json')

    textgen.generate_samples(max_gen_length=1000)
    textgen.generate_to_file('textgenrnn_texts.txt', max_gen_length=1000)

"""
Story generator based on textgenrnn
"""

from textgenrnn import textgenrnn


def cleantext(text):
    """
    
    """
    print("Start Cleaning")


def generate():
    root_dir = 'config/'
    textgen = textgenrnn(weights_path= root_dir + 'colaboratory_weights.hdf5',
                        vocab_path= root_dir + 'colaboratory_vocab.json',
                        config_path= root_dir + 'colaboratory_config.json')
    textgen.generate_samples(max_gen_length=1000)
    textgen.generate_to_file('textgenrnn_texts.txt', max_gen_length=1000)

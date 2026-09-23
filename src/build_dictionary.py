import os 
from tokenizer import tokenize

DATASET = "dataset"
OUTPUT_PATH = "output/dictionary.txt"


def collect_vocabulary(dataset_dir):
    vocabulary = set()
    for filename in os.listdir(dataset_dir):
        filepath = os.path.join(dataset_dir, filename) 
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f: 
                vocabulary.update(tokenize(line))
    return vocabulary


def write_vocabulary(vocabulary, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
     for word_id, word in enumerate(sorted(vocabulary)):
            f.write(f"{word}\t{word_id}\n")    


if __name__ == "__main__":
    vocabulary = collect_vocabulary(DATASET)
    write_vocabulary(vocabulary, OUTPUT_PATH)
    print(f"Vocabulary written to {OUTPUT_PATH} with {len(vocabulary)} unique words.")

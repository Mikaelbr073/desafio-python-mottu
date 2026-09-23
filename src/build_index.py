import os
import heapq
from tokenizer import tokenize

DICTIONARY_PATH = "output/dictionary.txt"
DATASET_DIR = "dataset"
OUTPUT_PATH = "output/inverted_index.txt"
TEMP_DIR = "output/blocks"
BLOCK_SIZE = 10


def load_dictionary(dictionary_path):
    dictionary = {}
    with open(dictionary_path, "r", encoding="utf-8") as f:
        for line in f:
            word, word_id = line.strip().split("\t")
            dictionary[word] = int(word_id)
    return dictionary


def chunked(items, size):
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def collect_block_pairs(filenames, dataset_dir, dictionary):
    pairs = set()
    for filename in filenames:
        doc_id = int(filename)
        filepath = os.path.join(dataset_dir, filename)
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            for line in f:
                for word in tokenize(line):
                    word_id = dictionary.get(word)
                    if word_id is not None:
                        pairs.add((word_id, doc_id))
    return pairs


def write_block(pairs, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        for word_id, doc_id in sorted(pairs):
            f.write(f"{word_id}\t{doc_id}\n")


def build_blocks(dataset_dir, dictionary, block_size, temp_dir):
    filenames = os.listdir(dataset_dir)
    block_paths = []
    for block_index, filenames_chunk in enumerate(chunked(filenames, block_size)):
        pairs = collect_block_pairs(filenames_chunk, dataset_dir, dictionary)
        block_path = os.path.join(temp_dir, f"block_{block_index}.txt")
        write_block(pairs, block_path)
        block_paths.append(block_path)
    return block_paths


def read_pairs(filepath):
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            word_id_str, doc_id_str = line.rstrip("\n").split("\t")
            yield (int(word_id_str), int(doc_id_str))


def merge_blocks(block_paths, output_path):
    streams = [read_pairs(path) for path in block_paths]
    merged = heapq.merge(*streams)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        current_word_id = None
        current_doc_ids = []
        for word_id, doc_id in merged:
            if word_id != current_word_id:
                if current_word_id is not None:
                    doc_ids_str = ",".join(str(d) for d in current_doc_ids)
                    out.write(f"{current_word_id}\t{doc_ids_str}\n")
                current_word_id = word_id
                current_doc_ids = [doc_id]
            else:
                current_doc_ids.append(doc_id)
        if current_word_id is not None:
            doc_ids_str = ",".join(str(d) for d in current_doc_ids)
            out.write(f"{current_word_id}\t{doc_ids_str}\n")


if __name__ == "__main__":
    dictionary = load_dictionary(DICTIONARY_PATH)
    block_paths = build_blocks(DATASET_DIR, dictionary, BLOCK_SIZE, TEMP_DIR)
    merge_blocks(block_paths, OUTPUT_PATH)
    print(f"Index written to {OUTPUT_PATH} from {len(block_paths)} blocks.")
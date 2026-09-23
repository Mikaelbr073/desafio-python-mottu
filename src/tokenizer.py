def tokenize(line) -> list[str]:
    words= []
    current = "" 
    for char in line.lower():
        if char.isalnum():
            current += char
        else:
            if current:
                words.append(current)
                current = ""
    if current:
        words.append(current)
    return words
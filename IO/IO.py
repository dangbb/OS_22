
def read_line(io):
    text = io.readline().split(' ')
    if not isinstance(text, list):
        text = [text]
    return [int(num) for num in text]
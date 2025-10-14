
def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.lstrip("#").strip()
        else:
            raise Exception("No H1 title found in markdown")
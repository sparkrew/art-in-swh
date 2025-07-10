f = open('../source_data/source_data_moma_artists.txt')
content = f.read()
f.close()
with open('../moma_artists_parsed.txt', 'x') as output_f:
    content = content.split('\n')
    for (i, line) in enumerate(content):
        if i == 0:
            continue # Skip the first line
        line = line.split(',')
        try:
            output_f.write(line[1] + '\n') # Write Name to file
        except IndexError:
            continue


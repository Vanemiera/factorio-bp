import zlib
import base64
import json
from pprint import pprint
from dataclasses import dataclass

INDENT = 1

def decode(infile, outfile):
    raw_data = 0

    with open(infile, 'r') as f:
        raw_data = f.read()

    version = raw_data[0]
    raw_bytes = base64.b64decode(raw_data[1:])
    decompressed_bytes = zlib.decompress(raw_bytes)
    json_string = decompressed_bytes.decode('utf-8')
    data = json.loads(json_string)

    with open(outfile, 'w') as f:
        json.dump(data, f, indent=INDENT, sort_keys=False)

def decodes(raw_data):
    version = raw_data[0]
    raw_bytes = base64.b64decode(raw_data[1:])
    decompressed_bytes = zlib.decompress(raw_bytes)
    json_string = decompressed_bytes.decode('utf-8')
    data = json.loads(json_string)
    return data

def encodes(infile):
    with open(infile, 'r') as f:
        data = json.load(f)

    json_compact = json.dumps(data)
    bytes_uncompressed = json_compact.encode('utf-8')
    bytes_compressed = zlib.compress(bytes_uncompressed, 9)
    b64_data = '0' + base64.b64encode(bytes_compressed).decode('utf-8')
    
    return b64_data

def clip(file, *args, **kwargs):
    import pandas as pd
    df = pd.DataFrame([encodes(file)])
    df.to_clipboard(index=False, header=False)

def unclip(*args, **kwargs):
    import pandas as pd
    df = pd.read_clipboard()
    data = decodes(df.columns[0])
    if 'blueprint' in data:
        label =  data['blueprint']['label']
        filename = label.replace(' ', '_').lower()
        with open(f'blueprints/{filename}.json', 'w') as f:
            json.dump(data, f, indent=INDENT, sort_keys=False)
    elif 'blueprint_book' in data:
        label =  data['blueprint_book']['label']
        filename = label.replace(' ', '_').lower()
        with open(f'books/{filename}.json', 'w') as f:
            json.dump(data, f, indent=INDENT, sort_keys=False)
    # decision = input('Overwrite existing file? (y/n):')
    # if decision == 'y':
    #     print('Writing...')
    # elif decision == 'n':
    #     print('Aborting...')
    #     return
    # else:
    #     print('Invalid input, aborting...')
    #     return

def zipcollection(*args, **kwargs):
    from glob import glob
    from zipfile import ZipFile
    with ZipFile('collection.zip', mode='w') as bundle:
        for f in glob('blueprints/*.json') + glob('books/*.json'):
            data = encodes(f).encode('utf-8')
            with bundle.open(f[:-4]+'txt', mode='w') as bp:
                bp.write(data)

def unbundle(file, *args, **kwargs):
    with open(file, mode='r') as book:
        data = json.loads(book.read())
        for blueprint in data['blueprint_book']['blueprints']:
            del blueprint['index']
            label =  blueprint['blueprint']['label']
            print(f'Unpacking "{label}"...')
            filename = label.replace(' ', '_').lower()
            with open(f'blueprints/{filename}.json', 'w') as f:
                json.dump(blueprint, f, indent=INDENT, sort_keys=False)

def bundle(pattern, label, *args, **kwargs):
    print(f'pattern:{pattern}')
    print(f'label:{label}')

    from glob import glob

    book = {'blueprint_book':{
        'blueprints': [],
        'item': 'blueprint-book',
        'label': label,
        'active_index': 0,
        'version': 0}}
    index = 0
    bookfilename = label.replace(' ', '_').lower()

    for filename in glob(pattern):
        print(f'Adding "{filename}"...')
        with open(filename, 'r') as f:
            blueprint = json.load(f)
            blueprint['index'] = index
            index += 1
            book['blueprint_book']['blueprints'].append(blueprint)

    blueprints = iter(book['blueprint_book']['blueprints'])
    print_versions = (bp['blueprint']['version'] for bp in blueprints)
    book['blueprint_book']['version'] = max(print_versions)

    with open(f'books/{bookfilename}.json', 'w') as f:
        json.dump(book, f, indent=INDENT, sort_keys=False)

def main():
    """
    Sub commands:
    * clip (convert and copy blueprint data to clipboard)
    * unclip (convert clipboard data and save to disk)
    * zipcollection (converts all json files to bp and outputs a zip)
    * bundle (merges blueprints to a book)
    * unbundle (saves blueprints in a book as separate files)
    """
    import argparse

    parser_main = argparse.ArgumentParser()
    parser_main.set_defaults(func=False)

    subparsers = parser_main.add_subparsers()

    parser_clip = subparsers.add_parser('clip')
    parser_clip.set_defaults(func=clip)
    parser_clip.add_argument('file', type=str, help='file to copy to clipboard')

    parser_unclip = subparsers.add_parser('unclip')
    parser_unclip.set_defaults(func=unclip)

    parser_zip = subparsers.add_parser('zip')
    parser_zip.set_defaults(func=zipcollection)

    parser_unbundle = subparsers.add_parser('unbundle')
    parser_unbundle.set_defaults(func=unbundle)
    parser_unbundle.add_argument('file', type=str, help='book file to unbundle')

    parser_unbundle = subparsers.add_parser('bundle')
    parser_unbundle.set_defaults(func=bundle)
    parser_unbundle.add_argument('pattern', type=str, help='Glob pattern of blueprints')
    parser_unbundle.add_argument('label', type=str, help='Book label')

    args = parser_main.parse_args()
    if args.func:
        args.func(**vars(args))
    else:
        parser_main.print_help()

if __name__ == "__main__":
    main()
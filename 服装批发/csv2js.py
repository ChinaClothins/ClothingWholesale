import csv, json, os, sys

# Use script's own directory, not CWD
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'products.csv')
js_path = os.path.join(script_dir, 'products.js')

products = []
errors = []

for encoding in ['utf-8-sig', 'utf-8', 'gbk', 'gb18030', 'latin-1']:
    try:
        with open(csv_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            # Clean up fieldnames: strip BOM char and any stray "/xef/xbb/xbf" text prefix
            raw_fields = reader.fieldnames or []
            clean_fields = []
            for fn in raw_fields:
                fn = fn.lstrip('\ufeff')  # real UTF-8 BOM char
                # Remove literal "/xef/xbb/xbf" prefix if present (corrupted BOM)
                while fn.startswith('/xef') or fn.startswith('/xbb') or fn.startswith('/xbf'):
                    fn = fn[4:]
                clean_fields.append(fn)
            reader.fieldnames = clean_fields

            for row in reader:
                name = (row.get('name') or '').strip()
                if not name:
                    continue
                products.append({
                    'name': name,
                    'image': (row.get('image') or '').strip(),
                    'category': (row.get('category') or '').strip(),
                    'tag': (row.get('tag') or '').strip(),
                    'stockBadge': (row.get('stockBadge') or '').strip(),
                    'sizes': (row.get('sizes') or '').strip(),
                    'colors': (row.get('colors') or '').strip(),
                    'season': (row.get('season') or '').strip(),
                    'desc': (row.get('desc') or '').strip(),
                    'moq': (row.get('moq') or '').strip()
                })
        if products:
            break
    except Exception as e:
        errors.append(encoding + ': ' + str(e))
        products = []

if not products:
    print('ERROR reading ' + csv_path)
    for err in errors:
        print('  ' + err)
    sys.exit(1)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write('var PRODUCTS = ' + json.dumps(products, ensure_ascii=False, indent=2) + ';\n')

print('Done: ' + str(len(products)) + ' products -> products.js')

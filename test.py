from CIANparser import Parser
import json

with open('db.json', 'w', encoding='utf-8') as file:
    print('Starting...')
    db = Parser.run(Parser, 1, 5)
    json.dump(db, file, sort_keys=True, indent=2)
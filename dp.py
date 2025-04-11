import sqlite3

def make_db(source='districts.txt'):
    con = sqlite3.connect('lenobl.db')
    cur = con.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district TEXT,
            description TEXT,
            map_link TEXT,
            name TEXT
        )
        '''
    )
    with open(source, 'r') as s:
        for line in s:
            line = line.strip()
            if not line: continue
            if not line.startswith('- '):
                curd = line.rstrip(':')
            else:
                content = line[2:]
                first_colon_index = content.find(':')
                if first_colon_index == -1: continue
                name = content[:first_colon_index].strip()
                rest_content = content[first_colon_index + 1:].strip()
                second_colon_index = rest_content.find(':')
                if second_colon_index == -1: continue
                description = rest_content[:second_colon_index].strip()
                map_link = rest_content[second_colon_index + 1:].strip()
                cur.execute(
                    '''
                    INSERT INTO districts (district, name, description, map_link)
                    VALUES (?, ?, ?, ?)
                    ''', 
                    (curd, name, description, map_link)
                )
    con.commit()
    con.close()

def get_by_district(district):
    make_db()
    con = sqlite3.connect('lenobl.db')
    cur = con.cursor()
    cur.execute('SELECT name, description, map_link FROM districts WHERE district = ?', (district,))
    results = cur.fetchall()
    con.close()
    return results

import sqlite3 as sl

class LocalDB:
    def __init__(self):
        self.con = sl.connect('covers.db')
        self.cur = self.con.cursor()
        with self.con:
            self.con.execute("""
                CREATE TABLE IF NOT EXISTS COVER (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    colors TEXT
                )
            """)
            self.con.execute("""
                CREATE TABLE IF NOT EXISTS CURRENT (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)

    def set_current(self, name):
        self.cur.execute("""
            UPDATE CURRENT
            SET name = ?
            WHERE id = 1
        """, (name,))
        self.con.commit()


    def get_current(self):
        self.cur.execute('SELECT name FROM CURRENT WHERE id = 1')
        res = self.cur.fetchone()
        if res:
            return res[0]
        else:
            return None

    def insert_cover(self, name, colors):
        cur = self.con.cursor()
        color_str = ','.join(colors)
        cur.execute('INSERT INTO COVER (name, colors) VALUES (?, ?)', (name, color_str))
        self.con.commit()

    def update_cover(self, name, colors):
        color_str = ','.join(colors)
        self.cur.execute("""
        INSERT OR REPLACE INTO COVER (id, name, colors)
        VALUES (COALESCE((SELECT id FROM COVER WHERE name = ?), ((SELECT MAX(id) FROM COVER) + 1)), ?, ?)
        """, (name, name, color_str))

        self.con.commit()

    def get_cover(self, name):
        self.cur.execute('SELECT colors FROM COVER WHERE name = ?', (name,))
        res = self.cur.fetchone()
        if res:
            colors = res[0].split(',')
            return colors
        else:
            return None

    def get_all_covers(self):
        self.cur.execute('SELECT * FROM COVER')
        return self.cur.fetchall()

    def delete_cover(self, id):
        self.cur.execute('DELETE FROM covers WHERE id = ?', (id,))
        self.con.commit()

    def get_current_cover(self):
        self.cur.execute('SELECT name FROM CURRENT WHERE id = 1')
        res = self.cur.fetchone()
        if res:
            name = res[0]
            return self.get_cover(name)
        else:
            return None

    def close(self):
        self.con.close()

# -*- coding: utf-8 -*-

import sqlite3


class ReviewsCrawlerPipeline(object):
    def __init__(self):
        self.connection = sqlite3.connect("reviews.db")
        self.cursor = self.connection.cursor()
        # self.cursor.execute("DROP TABLE IF EXISTS reviews;")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reviews (_id text PRIMARY KEY,
            artist text,
            album text,
            rating text,
            intro text,
            url text);""")

    def process_item(self, item, spider):
        self.cursor.execute("SELECT COUNT(*) FROM reviews WHERE url = '" + item['url'] + "';")
        (result, ) = self.cursor.fetchone()
        if result == 0:
            self.cursor.execute("""INSERT INTO reviews (_id, artist, album, rating, intro, url) VALUES
                (?, ?, ?, ?, ?, ?);""", (item['_id'], item['artist'], item['album'], item['rating'],
                                         item['intro'], item['url']))
            self.connection.commit()
            with open('./reviews/' + item['_id'] + ".txt", 'w', encoding='utf-8') as output:
                output.write(item['text'])
        return item

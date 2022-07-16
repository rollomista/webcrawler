'''Modulo db_mediator.
'''
import sqlite3 as sql  # pylint: disable=import-error


class DbMediator():
    '''DbMediator.

    Permette la comunicazione ed interazione con il database.'''

    def __init__(self):
        self.filename = 'words_occurrence.db'
        self.connection = None

    def connect(self):
        '''Crea la connessione con il database.
        '''
        self.connection = sql.connect(self.filename)

    def update_word_tables(self, word_count_table):
        '''Inserisce le informazioni contenute in word_count_table nel db.

        Si creano, se non presenti, le tabelle asociate alle parole.
        Si verifica se è già presente una riga corrispondente all'url,
        per ciascuna tabella. Se non presente, le informazioni vengono memorizzate
        in una nuova riga.

        Args:
            word_count_table (dict): Le keys sono le parole, a ciascuna delle quali
            corrisponde una tabella nel db. I values sono delle liste di tuple. Ciascuna
            tupla corriponde ad una riga da inserire.'''
        cursor = self.connection.cursor()
        self._create_words_tables(word_count_table)
        for word in word_count_table:
            for row in word_count_table.get(word):
                cursor.execute(f''' SELECT count(url) FROM {word}
                WHERE url='{row[0]}'
                ''')
                if cursor.fetchone()[0] == 0:
                    cursor.execute(f'''INSERT INTO {word}
                        VALUES (
                            '{row[0]}', {row[1]})
                        ''')
        self.connection.commit()

    def print_word_table(self, word):
        '''Stampa la tabella di nome word.

        Args:
            word (str): Parola corrispondente al nome della tabella.'''
        cursor = self.connection.cursor()
        for row in cursor.execute(f'''SELECT * FROM {word}'''):
            print(row)

    def _create_words_tables(self, word_count_table):
        cursor = self.connection.cursor()
        for word in word_count_table:
            cursor.execute(f''' SELECT count(name) FROM sqlite_master
                WHERE type='table' AND name='{word}'
                ''')
            if cursor.fetchone()[0] == 0:
                cursor.execute(f'''CREATE TABLE {word} (
                    url text,
                    count integer
                    )''')
        self.connection.commit()

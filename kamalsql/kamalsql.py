import mysql.connector as mysql


class KamalSQL:
    """
    A simple wrapper for MySQL (mysql-connector)
    """

    config = None
    connection = None
    cursor = None

    def __init__(self, **kwargs) -> None:
        self.config = kwargs
        self.connect()

    def connect(self) -> None:
        """
        Connect to the mysql server.
        """

        try:
            self.connection = mysql.connect(
                host=self.config['host'],
                db=self.config['database'],
                user=self.config['user'],
                passwd=self.config['password']
            )
            self.cursor = self.connection.cursor()
        except:
            print('Could not connect to the MySQL server.')
            raise

    def status(self) -> str:
        if (self.connection):
            return 'Connection Succesful'
        return 'Connection Unsucessful'

    def query(self, sqlQuery, params=None):
        """
        Runs a raw query

        Credits: github.com/knadh/simplemysql
        """

        # check if connection is alive. if not, reconnect

        try:
            self.cursor.execute(sqlQuery, params)
        except mysql.OperationalError as e:
            # If mysql timed out,
            #    reconnect and retry once
            if e[0] == 2006:
                self.connect()
                self.cursor.execute(sqlQuery, params)
            else:
                raise
        except:
            print("Query failed")
            raise

        return self.cursor

    def showTables(self) -> list:
        """
        Returns a list with the tables present in the
        database.
        """
        sqlQuery = 'SHOW TABLES;'
        fetcher = self.query(sqlQuery)

        tables = [table[0] for table in fetcher]
        return tables

    def commit(self):
        """
        Commit a transaction
        (transactional engines like InnoDB require this)
        """
        return self.connection.commit()

    def end(self):
        """
        Closes the MySQL connection.
        """
        self.cursor.close()
        self.connection.close()

    def __exit__(self, type, value, traceback):
        self.end()

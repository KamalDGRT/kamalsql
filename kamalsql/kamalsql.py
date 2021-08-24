import mysql.connector as mysql
from tabulate import tabulate


class KamalSQL:
    config = None
    connection = None
    cursor = None

    def __init__(self, **kwargs) -> None:
        self.config = kwargs
        self.config["autocommit"] = kwargs.get("autocommit", False)
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
            self.connection.autocommit = self.config["autocommit"]
        except:
            print('Could not connect to the MySQL server.')
            raise

    def status(self) -> str:
        if (self.connection):
            return 'Connection Succesful'
        return 'Connection Unsucessful'

    def query(self, sqlQuery, params=None):
        """
        Run a raw SQL query
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
        Returns a list with the tables
        present in the database.
        """
        sqlQuery = 'SHOW TABLES;'
        fetcher = self.query(sqlQuery)

        tables = [table[0] for table in fetcher]
        return tables

    def describeTable(self, table) -> list:
        """
        Returns a list of tuples witht the table description.
        """
        sqlQuery = 'DESC ' + table + ';'
        fetcher = self.query(sqlQuery)
        details = [table for table in fetcher]
        details.insert(0, ('Field', 'Type', 'Null', 'Key', 'Default', 'Extra'))
        return details

    def fancyDescribeTable(self, table) -> str:
        """
        Returns the table description in a tabular format.
        """
        return tabulate(
            self.describeTable(
                table
            ),
            headers='firstrow',
            tablefmt='fancy_grid'
        )

    def insert(self, table, info):
        """
        Inserts a record into a given table.
        """
        columns = tuple(info.keys())
        values = tuple(info[column] for column in columns)
        sqlQuery = 'INSERT INTO ' + table + ' '
        sqlQuery += str(columns).replace("'", '')
        sqlQuery += ' VALUES ' + str(values) + ';'
        print(sqlQuery)
        return self.query(sqlQuery)

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

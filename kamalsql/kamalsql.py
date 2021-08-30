import mysql.connector as mysql
from tabulate import tabulate


class KamalSQL:
    config = None
    connection = None
    cursor = None

    def __init__(self, **kwargs) -> None:
        self.config = kwargs
        self.config["autocommit"] = kwargs.get("autocommit", False)
        self.config["keep_alive"] = kwargs.get("keep_alive", False)
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
            self.connection.autocommit = self.config["autocommit"]
            self.cursor = self.connection.cursor()
        except:
            print('Could not connect to the MySQL server.')
            raise

    def status(self) -> str:
        if (self.connection):
            return 'Connection Successful'
        return 'Connection Unsuccessful'

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
            if e[0] == 2006 or e.args[0] == 2013:
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
        Returns a list of tuples with the table description.
        """
        sqlQuery = 'DESC ' + table + ';'
        fetcher = self.query(sqlQuery)
        details = [table for table in fetcher]
        details.insert(0, ('Field', 'Type', 'Null', 'Key', 'Default', 'Extra'))
        return details

    def tableFormatRows(self, data) -> str:
        """
        Returns the table generated from rows in a tabular format.
        """
        if (data is None):
            return 'The table is empty !!!'
        else:
            firstRow = dict(zip(data[0].keys(), data[0].keys()))
            data.insert(0, firstRow)
            return '\n' + tabulate(data, headers='firstrow') + '\n'

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

    def select(self, table=None, fields=None, where=None, order=None, limit=None):
        """
        Runs a select query
        """

        sqlQuery = "SELECT %s FROM `%s`" % (",".join(fields), table)

        # where conditions
        # if where condition exists, then append to query
        if where and len(where) > 0:
            sqlQuery += " WHERE %s" % where[0]

        # order
        # if order by condition exists, append to query
        if order:
            sqlQuery += " ORDER BY %s" % order[0]

            if len(order) > 1:
                sqlQuery += " %s" % order[1]

        # limit
        # if limit exists, append to query
        if limit:
            sqlQuery += " LIMIT %s" % limit[0]

            if len(limit) > 1:
                sqlQuery += ", %s" % limit[1]

        # Parameters to be passed, applies only to where
        # clause because the argument size fluctuates.
        params = None
        if where and len(where) > 1:
            params = where[1]
        return self.query(sqlQuery, params)

    def getAll(self, table=None, fields='*', where=None, order=None, limit=None) -> list:
        """
        Get all rows of a given query
            table = (str) table_name
            fields = (field1, field2 ...) list of fields to select
            where = ("parameterizedstatement", [parameters])
                    eg: ("id=%s and name=%s", [1, "test"])
            order = [field, ASC|DESC]
            limit = [from, to]
        """

        cursor = self.select(table, fields, where, order, limit)
        result = cursor.fetchall()

        rows = None
        if result:
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in result]

        return rows

    def insert(self, table, info):
        """
        Inserts a record into a given table.
        """
        columns = [key for key in info.keys()]
        values = [info[column] for column in columns]
        sqlQuery = 'INSERT INTO ' + table + ' '
        sqlQuery += str(columns).replace("'", '')
        sqlQuery += ' VALUES ' + str(values) + ';'
        sqlQuery = sqlQuery.replace('[', '(').replace(']', ')')
        return self.query(sqlQuery)

    def update(self, table, info, where=None):
        keys = "=%s, ".join(info.keys()) + "=%s"
        values = list(info.values())
        sqlQuery = 'UPDATE %s SET %s' % (table, keys)

        # where conditions
        # if where condition exists, then append to query
        if where and len(where) > 0:
            sqlQuery += " WHERE %s" % where[0]

        # Parameters to be passed, applies only to where
        # clause because the argument size fluctuates.
        # In update query, setting the values to a
        # particular column is a common one, that is
        # the reason why the params variable has the
        # contents of values assigned to it.
        # When the where clause exists, we just append
        # the values to the params variable.
        params = values
        if where and len(where) > 1:
            params += where[1]

        return self.query(sqlQuery, params)

    def delete(self, table, where=None):
        """
        Delete rows based on a WHERE condition.
        """

        sqlQuery = "DELETE FROM " + table

        # where conditions
        # if where condition exists, then append to query
        if where and len(where) > 0:
            sqlQuery += " WHERE %s" % where[0]

        # Parameters to be passed, applies only to where
        # clause because the argument size fluctuates.
        params = None
        if where and len(where) > 1:
            params = where[1]
        return self.query(sqlQuery, params)

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

    def __exit__(self):
        self.end()

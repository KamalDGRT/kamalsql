# KamalSQL

Kamal's version of a Python wrapper for MySQL database stuff.

## Installation

To install the `kamalsql` package, you can execute the below command.

```
pip install kamalsql
```

If you have already installed `kamalsql` and would like to upgrade
to the latest version you could do this:

```
python -m pip install --upgrade kamalsql
```

## Usage

Before getting into how to use this, here is the database info for the
below examples.

-   Tables present: `department`, `student`
-   Table description of `department`

    | Field | Type        | Null | Key | Default | Extra |
    | ----- | ----------- | ---- | --- | ------- | ----- |
    | sname | varchar(20) | YES  |     | NULL    |       |
    | regno | varchar(20) | YES  |     | NULL    |       |
    | m1    | int(11)     | YES  |     | NULL    |       |
    | m2    | int(11)     | YES  |     | NULL    |       |

### For the connection to the database

```py
from kamalsql import KamalSQL

db = KamalSQL(
    host='localhost',
    user='username',
    password='mypassword',
    database='mydatabase'
)
```

When you establish a connection in the above way, the auto-commit
feature is disabled by default. If you would like to auto-commit
the transactions, you can establish the connection is the following
way:

```py
from kamalsql import KamalSQL

db = KamalSQL(
    host='localhost',
    user='username',
    password='mypassword',
    database='mydatabase',
    autocommit=True
)
```

You could also check the connection status using the `status()` function:

```py
print(db.status())
```

If the connection is established, you will get this:

```
Connection Successful
```

If not, this:

```
Connection Unsuccessful
```

### List out the tables present in the database

You can get the tables present in the database using the
`showTables()` function.

```py
tables = db.showTables()
print(tables)
```

##### Output

```
['department', 'student']
```

### Describing the Table

There are a couple of ways you could do this:

-   using `describeTable()`
-   using `fancyDescribeTable()`

#### using `describeTable()`

The `describeTable()` returns a list with the description in the form of
tuples. So, to make it more readable, one has to use a loop.

```py
description = db.describeTable('department')
for info in description:
    print(info)
```

##### Output

```
('Field', 'Type', 'Null', 'Key', 'Default', 'Extra')
('sname', 'varchar(20)', 'YES', '', None, '')
('regno', 'varchar(20)', 'YES', '', None, '')
('m1', 'int(11)', 'YES', '', None, '')
('m2', 'int(11)', 'YES', '', None, '')
```

#### using `fancyDescibeTable()`

Here we are using the `tabulate` module to pretty-print the
table description.

```py
description = db.fancyDescribeTable('department')
print(description)
```

##### Output

```
╒═════════╤═════════════╤════════╤═══════╤═══════════╤═════════╕
│ Field   │ Type        │ Null   │ Key   │ Default   │ Extra   │
╞═════════╪═════════════╪════════╪═══════╪═══════════╪═════════╡
│ sname   │ varchar(20) │ YES    │       │           │         │
├─────────┼─────────────┼────────┼───────┼───────────┼─────────┤
│ regno   │ varchar(20) │ YES    │       │           │         │
├─────────┼─────────────┼────────┼───────┼───────────┼─────────┤
│ m1      │ int(11)     │ YES    │       │           │         │
├─────────┼─────────────┼────────┼───────┼───────────┼─────────┤
│ m2      │ int(11)     │ YES    │       │           │         │
╘═════════╧═════════════╧════════╧═══════╧═══════════╧═════════╛
```

### Inserting values to a table

Now that we know how to establish connection, lets see how to insert
values into a table.

```py
db.insert(
    'department',
    {
        'sname': 'Akash',
        'regno': '391201',
        'm1': 95,
        'm2': 96
    }
)

db.insert(
    'department',
    {
        'sname': 'Anish',
        'regno': '391202',
        'm1': 92,
        'm2': 91
    }
)

db.insert(
    'department',
    {
        'sname': 'Bala',
        'regno': '391203',
        'm1': 91,
        'm2': 90
    }
)

db.insert(
    'department',
    {
        'sname': 'Dinesh',
        'regno': '391204',
        'm1': 65,
        'm2': 86
    }
)
```

If you have not enabled the auto-commit feature, then make sure to use
`db.commit()` to complete the transaction.

### Viewing the table contents

-   We saw how to insert values.
-   Now lets check if they have been inserted into the table.
-   This can be done by invoking the `getAll()` function.
-   `getAll()` returns a list with dictionary objects.

```py
records = db.getAll('department')
for record in records:
    print(record)
```

##### Output

```
{'sname': 'Akash', 'regno': '391201', 'm1': 95, 'm2': 96}
{'sname': 'Anish', 'regno': '391202', 'm1': 92, 'm2': 91}
{'sname': 'Bala', 'regno': '391203', 'm1': 91, 'm2': 90}
{'sname': 'Dinesh', 'regno': '391204', 'm1': 65, 'm2': 86}
```

-   By default, if you pass just the table name, it will select all the
    columns.
-   If you wish to view the above output in a tabular format, then you
    could use `tableFormatRows()` to do the same.

```py
rows = db.getAll('department')
table = db.tableFormatRows(rows)
print(table)
```

##### Output

```
sname      regno    m1    m2
-------  -------  ----  ----
Akash     391201    95    96
Anish     391202    92    91
Bala      391203    91    90
Dinesh    391204    65    86
```

-   See, I know that the above statements can be combined to form a one-liner
    like this: `print(db.tableFormatRows(db.getAll('department')))` but,
    for the sake of simplicity and to make things more clearer, I am doing it
    in that way.

-   If you would like to add a few more conditions, then you could invoke
    the `getAll()` function in this way:

```py
rows = db.getAll(
    'department',                    # Table to be selected
    ['regno', 'sname'],              # Columns to display
    ("regno >= %s and regno <= %s",  # WHERE clause
        ['391201', '391204']         # values for the arguments used in WHERE
    ),
    ["regno", "asc"],                # ORDER BY regno asc
    [0, 2]                           # LIMIT 0, 2
)

for row in rows:
    print(row)

print('\nTabular Format: \n')
print(db.tableFormatRows(rows))
```

##### Output

```
{'regno': '391201', 'sname': 'Akash'}
{'regno': '391202', 'sname': 'Anish'}

Tabular Format:


  regno  sname
-------  -------
 391201  Akash
 391202  Anish
```

### Updating the values

-   We saw how to insert and the various ways to see the table's content.
-   Now, lets see how to update existing values.
-   Note: Don't forget to give the `WHERE` condition. If you don't provide
    that, the update condition will get applied to the entire table.

```py
db.update(
    'department',                 # The table
    {                             # The new values
        "sname": "Frank",
        "regno": "391205"
    },
    ("regno = %s", ['391204'])    # the WHERE condition.
)

rows = db.getAll('department')
print(db.tableFormatRows(rows))
```

##### Output

```
sname      regno    m1    m2
-------  -------  ----  ----
Akash     391201    95    96
Anish     391202    92    91
Bala      391203    91    90
Frank     391205    65    86
```

### Deleting record(s)

-   We saw how to insert, view and the various ways to see the table's content.
-   Now, lets see how to remove record(s).
-   Note: Don't forget to give the `WHERE` condition. If you don't provide
    that, the `DELETE` condition will get applied to the entire table.

```py
db.delete(
    'department',               # Table involved
    ("regno = %s", ['391205'])  # the WHERE clause
)

rows = db.getAll('department')
print(db.tableFormatRows(rows))
```

```
sname      regno    m1    m2
-------  -------  ----  ----
Akash     391201    95    96
Anish     391202    92    91
Bala      391203    91    90
```

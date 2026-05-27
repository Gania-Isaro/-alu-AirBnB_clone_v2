# AirBnB Clone - The Console (v2)

## Team

| Name | GitHub |
|------|--------|
| Gania Kayumba | [Gania-Isaro](https://github.com/Gania-Isaro) |
| Jessica Bizima | [Jessica-Bizima](https://github.com/Jessica-Bizima) |

## Description

This project is the second step toward building a full web application that clones AirBnB.
It builds on v1 by adding:
- MySQL database storage using SQLAlchemy ORM
- Dual storage engine support (FileStorage and DBStorage)
- Environment-variable-driven configuration
- Extended console supporting parameterised object creation

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HBNB_ENV` | Running environment: `dev` or `test` |
| `HBNB_MYSQL_USER` | MySQL username |
| `HBNB_MYSQL_PWD` | MySQL password |
| `HBNB_MYSQL_HOST` | MySQL host (default: localhost) |
| `HBNB_MYSQL_DB` | MySQL database name |
| `HBNB_TYPE_STORAGE` | Storage type: `file` or `db` |

## The Command Interpreter

### How to Start

**Interactive mode:**

```
$ ./console.py
(hbnb)
```

**Non-interactive mode:**

```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb)
```

### How to Use

Type commands at the `(hbnb)` prompt.

**Commands:**

- `create <class> [key=value ...]` - Creates a new instance with optional params and prints the id
- `show <class> <id>` - Prints the string representation of an instance
- `destroy <class> <id>` - Deletes an instance
- `all [class]` - Prints all instances, or all of a given class
- `update <class> <id> <attribute> <value>` - Updates an attribute of an instance
- `quit` - Exit the program
- `EOF` - Exit the program (Ctrl+D)
- `help` - Show available commands

**Supported classes:** BaseModel, User, State, City, Amenity, Place, Review

### Examples

```
$ ./console.py
(hbnb) create State name="California"
49faff9a-6318-451f-87b6-910505c55907
(hbnb) all State
["[State] (49faff9a-6318-451f-87b6-910505c55907) {'name': 'California', ...}"]
(hbnb) quit
$
```

**With DBStorage:**

```
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
  HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
  HBNB_TYPE_STORAGE=db ./console.py
(hbnb) create State name="California"
```

## Storage

### FileStorage (default)
Serializes/deserializes objects to/from `file.json`.

### DBStorage
Uses MySQL via SQLAlchemy. Configure with environment variables above.

**Setup development DB:**
```bash
cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
```

**Setup test DB:**
```bash
cat setup_mysql_test.sql | mysql -hlocalhost -uroot -p
```

## Running Tests

**FileStorage:**
```bash
python3 -m unittest discover tests
```

**DBStorage:**
```bash
HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
HBNB_TYPE_STORAGE=db python3 -m unittest discover tests
```

## Authors

See the [AUTHORS](./AUTHORS) file.

### Original Authors (v1)
- Gania Isaro

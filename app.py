from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy import engine, text, Table, MetaData
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
import cx_Oracle
import DBconnectiondata

sid = cx_Oracle.makedsn(DBconnectiondata.host, DBconnectiondata.port, sid=DBconnectiondata.sidn)
cstr = 'oracle://{user}:{password}@{sid}'.format(
    user=DBconnectiondata.user,
    password=DBconnectiondata.password,
    sid=sid
)
engine =  engine.create_engine(
    cstr,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50
)

# Flask stuff
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

meta = MetaData()
insp = inspect(engine)
conn = engine.connect()

table_names = engine.table_names()
tables = []
allrows = []
allcollumns = []
primaryKeys = []
foreignKeys = []
for table in table_names:
    result = conn.execute(text("select * FROM " + table))
    total = result.fetchall()
    allrows.append(len(total))
    try:
        allcollumns.append(len(total[0]))
    except:
        pass
    table = Table(table, meta, autoload=True, autoload_with=engine)
    tables.append(table)
    foreignKeyColNames = [str(relations.column) for relations in table.foreign_keys]
    primaryKeyColNames = [pk_column.name for pk_column in table.primary_key.columns.values()]
    for i in range(len(primaryKeyColNames)-1):
        primaryKeyColNames[i] += ','
    for i in range(len(foreignKeyColNames)-1):
        foreignKeyColNames[i] += ','
    foreignKeyColNames = [foreign.split(".") for foreign in foreignKeyColNames]
    primaryKeys.append(primaryKeyColNames)
    foreignKeys.append(foreignKeyColNames)
conn.close()

current_table = ['tactu']

@app.route('/')
def index():
    return render_template("index.html", table_names = table_names, rows=allrows, columns=allcollumns, primaryKeys = primaryKeys, foreignKeys = foreignKeys)

@app.route('/table', methods = ["POST"])
def table():
    table_name = request.form.get("table_name")
    table_name = table_name.lower()
    return redirect(url_for('showtable', table_name = table_name))

@app.route('/table/<table_name>')
def showtable(table_name):
    table_name = table_name.lower()
    current_table[0] = table_name
    conn = engine.connect()
    if engine.dialect.has_table(conn, table_name):
        result = conn.execute(text("select * FROM " + table_name))
    else:
        return render_template("message.html", message="Can't find table named " + table_name)
    total = result.keys()
    column_names = total._keys
    total = result.fetchall()
    columns = len(total[0])
    # To avoid VScode from flagging jinja2 syntax as "problem"
    jsfunctions = []
    for i in range(columns):
        jsfunctions.append("onclick = sortTable(" + str(i) + ")")
    conn.close()
    return render_template("table.html", table_name = table_name, column_names = column_names, total = total, jsfunctions = jsfunctions)

@app.route('/table/<table_name>/submit', methods = ["POST"])
def submit(table_name):
    current_table = table_name
    pos = table_names.index(current_table)
    rows = allrows[pos]
    cols = allcollumns[pos]
    table = tables[pos]
    primaryKeyColNames = [pk_column.name for pk_column in table.primary_key.columns.values()]
    conn = engine.connect()
    result = conn.execute(text("select " + primaryKeyColNames[0] + " FROM " + current_table))
    total = result.fetchall()
    primaryKeyColName = primaryKeyColNames[0]
    primaryKeyValues = [pk[0] for pk in total]
    columnNames = table.columns.keys()
    columns_table = insp.get_columns(current_table)
    columnIsChar = []
    for c in columns_table:
        if('CHAR' in str(c['type']) or 'DATE' in str(c['type'])):
            columnIsChar.append(True)
        else:
            columnIsChar.append(False)
    for i in range(rows):
        stmt = "UPDATE " + current_table + " SET "
        for j in range(cols):
            new = request.form.get(str(i) + ',' + str(j))
            if(not columnIsChar[j]):
                stmt += columnNames[j] + ' = ' + new
            else:
                stmt += columnNames[j] + " = '" + new + "'"
            if(j+1 != cols):
                stmt += ', '
        stmt+=" WHERE " + primaryKeyColName + " = " + str(primaryKeyValues[i])
        print(stmt)
        engine.execute(stmt)
    conn.close()
    return render_template("message.html", message="Changes have been applied to the table successfully")
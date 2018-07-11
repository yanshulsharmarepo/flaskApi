import mysql.connector
import json

dataPoints = ['id', 'first_name', 'last_name', 'company_name', 'city', 'state', 'zip', 'email', 'web', 'age']


def getConnection():
    db = mysql.connector.connect(host='localhost', database='Records', user='root', password='admin123')
    return db


# Use all the SQL you like

def getUsers(request):
    db = getConnection()
    page = '0'
    limit = '10'
    name = None
    sort = 'order by id'
    try:
        page = request.args.get('page')
        if (page == None):
            page = '0'
        else:
            page = int(page) - 1
            if(page <= 0):
                page = 0
            page = str(page)

    except:
        page = '0'
    try:
        limit = request.args.get('limit')
        if (limit == None):
            limit = '10'
    except:
        limit = '10'

    try:
        name = request.args.get('name')
    except:
        name = None
    try:
        sort = request.args.get('sort')
        if (sort == None):
            sort = 'order by id'
        else:
            firstCh = sort[0]
            if (firstCh == '-'):
                field = sort[1:]
                sort = 'order by ' + field + " ASC"
            else:
                field = sort
                sort = 'order by ' + field + " DESC"
    except:
        sort = 'order by id'

    query = 'SELECT id,first_name ,last_name,company_name,city,state,zip,email,web,age FROM users'

    if name == None:
        name = None
    else:
        query = query + " where first_name like '%" + name + "%'" + " or last_name like '%" + name + "%' "

    page = int(page) * int(limit)
    page = str(page)
    if page is '':
        page = '0'

    query = query + " " + sort
    query = query + " limit " + page + "," + limit
    cur = db.cursor()
    result = {}
    count = 0
    print(query)
    cur.execute(query)

    for row in cur.fetchall():
        result[count] = {dataPoints[0]: row[0], dataPoints[1]: row[1], dataPoints[2]: row[2], dataPoints[3]: row[3],
                         dataPoints[4]: row[4], dataPoints[5]: row[5], dataPoints[6]: row[6], dataPoints[7]: row[7],
                         dataPoints[8]: row[8], dataPoints[9]: row[9]}
        count = count + 1
    db.close()
    result['status'] = 200
    result = json.dumps(result)
    return result


def createUsers(request):
    jsonV = request.get_json()
    dictonary = {}
    response = {}
    for field in dataPoints:
        try:
            dictonary[field] = jsonV[field]
        except:
            dictonary[field] = None
    mustPresent = ['first_name', 'last_name']
    for field in mustPresent:
        if (dictonary[field] == None):
            response['errorMessage'] = field + "Should Be Present"
            response['errorCode'] = 500
            return json.dumps(response)

    fields = '('
    values = '('
    for field in dataPoints:
        if field == 'id':
            continue
        fields = fields + "" + field + ","
        if dictonary[field] == None:
            values = values + " NULL ,"
        else:
            values = values + "'" + str(dictonary[field]) + "',"

    values = values[:-1]
    fields = fields[:-1]
    values = values + ')'
    fields = fields + ')'

    try:
        db = getConnection()
        query = 'INSERT IGNORE INTO users ' + fields + ' VALUES ' + values
        print(query)
        cur = db.cursor()
        result = cur.execute(query)
        db.commit()
        db.close()
        response["code"] = 200
        return json.dumps(response)
    except:
        response['errorMessage'] = "Internal Server Error"
        response['errorCode'] = 500

        return json.dumps(response)


def getUser(id):
    db = getConnection()
    cur = db.cursor()
    result = {}
    query = 'SELECT id,first_name ,last_name,company_name,city,state,zip,email,web,age FROM users WHERE id =' + id
    count = 0
    cur.execute(query)

    for row in cur.fetchall():
        result[count] = {dataPoints[0]: row[0], dataPoints[1]: row[1], dataPoints[2]: row[2], dataPoints[3]: row[3],
                         dataPoints[4]: row[4], dataPoints[5]: row[5], dataPoints[6]: row[6], dataPoints[7]: row[7],
                         dataPoints[8]: row[8], dataPoints[9]: row[9]}
        count = count + 1
    db.close()
    result['status'] = 201
    result = json.dumps(result)
    return result


def alterUser(id, request):
    jsonV = request.get_json()
    dictonary = {}
    response = {}
    for field in dataPoints:
        try:
            dictonary[field] = jsonV[field]
        except:
            dictonary[field] = None

    values = ''
    for field in dataPoints:
        if (dictonary[field] == None):
            continue
        values = values + ' ' + field + ' = "' + str(dictonary[field]) + '",'
    values = values[:-1]
    values = values + ''

    response = {}
    try:
        db = getConnection()
        query = 'UPDATE `users` SET  ' + values + ' WHERE id = ' + id
        print(query)
        cur = db.cursor()
        result = cur.execute(query)
        db.commit()
        db.close()
        response["code"] = 200
        return json.dumps(response)
    except:
        response['errorMessage'] = "Internal Server Error"
        response['errorCode'] = 500

        return json.dumps(response)


def deleteUser(id):
    response = {}
    try:
        db = getConnection()
        query = 'DELETE FROM `users` WHERE id = ' + id
        cur = db.cursor()
        result = cur.execute(query)
        db.commit()
        db.close()
        response["code"] = 200
        return json.dumps(response)
    except:
        response['errorMessage'] = "Internal Server Error"
        response['errorCode'] = 500

        return json.dumps(response)

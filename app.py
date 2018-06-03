import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def index():

    return render_template('home.html')

@app.route('/findyourmla' , methods=['GET', 'POST'])
def findyourmla():
    districts = district_list()
    if request.method == 'GET':
        return render_template('findyourmla.html', districts=districts, chosen='', info = '')
    else:
        chosen = request.form['chose']
        info = get_info(chosen)
        return render_template('findyourmla.html', districts=districts, chosen=chosen, info=info)

def get_info(district):
    conn = sqlite3.connect("ministers.db")
    c = conn.cursor()

    c.execute('''SELECT * FROM ministers WHERE riding='%s' ''' % district)
    rows = c.fetchall()

    member = rows[0][0]
    district = rows[0][1]
    party = rows[0][2]
    email = rows[0][3]
    phone = rows[0][4]
    image_url = rows[0][5]

    info = {
        'name' : member,
        'district' : district,
        'party' : party,
        'email' : email,
        'phone' : phone.replace('.', '-'),
        'image_url' : image_url
    }

    conn.close()
    return info

def district_list():
    conn = sqlite3.connect("ministers.db")
    c = conn.cursor()

    c.execute('''SELECT riding FROM ministers ''')
    rows = c.fetchall()
    districts = []
    for row in rows:
        districts.append(row[0])
    districts.sort()

    conn.close()

    return districts


if __name__=='__main__':
    app.run(port=8080)
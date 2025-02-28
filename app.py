from flask import Flask, request, render_template, jsonify, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configurar las credenciales de Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Ruta para manejar la solicitud del formulario
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        document = request.form['document']
        sheet = client.open('nombre_de_tu_hoja').sheet1
        records = sheet.get_all_records()
        result = [record for record in records if record['document'] == document]
        return render_template('survey.html', result=result)
    return render_template('index.html', result=None)

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/statement_account')
def statement_account():
    return render_template('statement_account.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/impact')
def impact():
    return render_template('impact.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    document = request.form['document']
    #print(f'Received document: {document} (type: {type(document)})')  # Debug log
    sheet = client.open('Gestión de Préstamos').worksheet('Préstamos')
    records = sheet.get_all_records()
    #print(f'All records: {records}')  # Debug log
    result = [record for record in records if str(record['Cedula']) == document]
    #print(f'Response data: {result}')  # Debug log
    return jsonify(result)

@app.route('/update_data', methods=['POST'])
def update_data():
    # Handle the data update logic here
    data = request.form
    # Process the data
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, url_for, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import os
import json

google_creds_json = os.getenv("GOOGLE_CREDENTIALS")

if google_creds_json:
    creds_dict = json.loads(google_creds_json)  # Convertir el string JSON en diccionario
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
else:
    raise ValueError("No se encontraron las credenciales de Google Sheets en las variables de entorno")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])    
def survey():
    if request.method == 'POST':
        document = request.form['document']
        sheet = client.open('nombre_de_tu_hoja').sheet1
        records = sheet.get_all_records()
        result = [record for record in records if record['ID'] == document]
        return render_template('survey.html', result=result)
    return render_template('survey.html', result=None)

@app.route('/statementAccount')
def statement_account():
    return render_template('statement_account.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user = request.form['user']
        contrasena = request.form['pass']
        # Procesar los datos del formulario según sea necesario
        return render_template('impact.html', user=user, contrasena=contrasena)
    return render_template('impact.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    document = request.form['document']
    #print(f'Received document: {document}')  # Debug log
    
    sheet = client.open('Gestión de Préstamos').worksheet(document)
    records = sheet.get_all_records()
    #print(f'All records: {records}')  # Debug log
    
    # Convert document to integer for comparison
    try:
        document = int(document)
    except ValueError:
        print(f'Invalid document ID: {document}')  # Debug log
        return jsonify([])

    result = [record for record in records if int(record['ID']) == document]
    #print(f'Response data: {result}')  # Debug log
    return jsonify(result)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080, threads=8)


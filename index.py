from flask import Flask, render_template, url_for, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import numpy as np
import pandas as pd
import mysql.connector
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

mydb= mysql.connector.connect(host="localhost",user="root",passwd="Admin", database="sfpc",port="3306")
cursor= mydb.cursor()   

df = px.data.tips()
days = df.day.unique()

app = Flask(__name__)

# Configurar las credenciales de Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])    
def survey():
    if request.method == 'POST':
        document = request.form['document']
        sheet = client.open('nombre_de_tu_hoja').sheet1
        records = sheet.get_all_records()
        result = [record for record in records if record['Cedula'] == document]
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
    sheet = client.open('Gestión de Préstamos').worksheet('Préstamos')
    records = sheet.get_all_records()
    #print(f'All records: {records}')  # Debug log
    
    # Convert document to integer for comparison
    try:
        document = int(document)
    except ValueError:
        print(f'Invalid document ID: {document}')  # Debug log
        return jsonify([])

    result = [record for record in records if int(record['Cedula']) == document]
    #print(f'Response data: {result}')  # Debug log
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


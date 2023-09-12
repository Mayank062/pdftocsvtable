from flask import Flask, request, render_template, send_file


app = Flask(__name__)


# Define a route to display the upload form
@app.route('/')
def upload_form():
  return render_template('upload_form.html')


# Define a route to handle form submission and PDF to CSV conversion
@app.route('/convert', methods=['POST'])
def convert_pdf_to_csv():
  pdf_file = request.files['pdfFile']
  csv_file_name = request.form['csvFile']

  # Save the uploaded PDF file
  pdf_file_path = os.path.join('uploads', pdf_file.filename)
  pdf_file.save(pdf_file_path)

  try:
    # Convert the PDF to CSV
    tabula.convert_into(pdf_file_path,
                        'output.csv',
                        output_format='csv',
                        pages='all',
                        lattice=True)

    # Read the CSV file
    data = pd.read_csv('output.csv')

    # Drop the first row
    data.drop(0, inplace=True)

    # Save the resulting CSV file with the provided name
    data.to_csv(csv_file_name, index=False)

    return send_file(csv_file_name, as_attachment=True)
  except Exception as e:
    return f"Error: {e}"


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

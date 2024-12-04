
from flask import Flask, render_template, request, send_file
import pandas as pd
from ydata_profiling import ProfileReport
import os

app = Flask(__name__)

# Route to upload a file and generate the profile
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve uploaded file
        file = request.files['file']
        
        if file:
            # Save the uploaded file
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Read the file
            df = pd.read_excel(file_path)

            # Generate profile report
            profile = ProfileReport(df, title="Dataset Profiling Report", explorative=True)

            # Save the report to an HTML file
            output_file = os.path.join('reports', 'dataset_profile_report.html')
            profile.to_file(output_file)

            # Send the file for download
            return send_file(output_file, as_attachment=True)

    return '''
    <!doctype html>
    <title>Upload an Excel file for Profiling</title>
    <h1>Upload an Excel file for Profiling</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload and Generate Report">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)

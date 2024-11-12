import streamlit as st
import pandas as pd
import os

# Define a folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to save uploaded files
def save_uploaded_file(uploaded_file):
    with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())

# Function to get list of uploaded files
def get_uploaded_files():
    files = os.listdir(UPLOAD_FOLDER)
    return files

# Report Section
def report():
    st.markdown("""
    <style>
        .report-section {
            background-color: #e3f2fd; /* Light blue background */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .report-title {
            font-size: 36px;
            color: #1976d2; /* Blue */
            text-align: center;
            margin-bottom: 15px;
        }
        .report-description {
            font-size: 18px;
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        .upload-card, .files-card {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .upload-card h3, .files-card h3 {
            font-size: 24px;
            color: #1976d2;
        }
        .files-table {
            margin-top: 10px;
            width: 100%;
            border-collapse: collapse;
        }
        .files-table th, .files-table td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }
        .files-table th {
            background-color: #f1f1f1;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="report-title">Upload and View Reports</h1>', unsafe_allow_html=True)
    st.markdown('<p class="report-description">Upload new reports and view previously uploaded ones. Ensure your reports are in PDF or CSV format.</p>', unsafe_allow_html=True)
    
    # File upload
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<h3>Upload New Report</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file (PDF/CSV)", type=['pdf', 'csv'])
    
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)
        st.success("File uploaded successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display previously uploaded files
    st.markdown('<div class="files-card">', unsafe_allow_html=True)
    st.markdown('<h3>Previous Reports</h3>', unsafe_allow_html=True)
    
    files = get_uploaded_files()
    
    if files:
        st.markdown('<table class="files-table">', unsafe_allow_html=True)
        st.markdown('<tr><th>Filename</th><th>Download</th></tr>', unsafe_allow_html=True)
        for file in files:
            st.markdown(f'<tr><td>{file}</td><td><a href="/{UPLOAD_FOLDER}/{file}" download="{file}">Download</a></td></tr>', unsafe_allow_html=True)
        st.markdown('</table>', unsafe_allow_html=True)
    else:
        st.write("No reports available.")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Main function to render the Report section
def main():
    report()

if __name__ == "__main__":
    main()

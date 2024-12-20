import streamlit as st
import os
import zipfile
import requests
import json

# Function to analyze code using Blackbox.ai API
def analyze_code(file_path):
    api_url = "https://api.blackbox.ai/analyze"  # Replace with the actual API endpoint
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
    
    with open(file_path, 'r') as file:
        code = file.read()
    
    response = requests.post(api_url, headers=headers, json={"code": code})
    
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a JSON response
    else:
        st.error(f"Error analyzing code: {response.text}")
        return None

# Function to save modified files
def save_modified_files(modified_files, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name, content in modified_files.items():
        with open(os.path.join(output_dir, file_name), 'w') as file:
            file.write(content)

# Streamlit UI
st.title("Code Analyzer with Blackbox.ai")

uploaded_file = st.file_uploader("Upload a project folder (zip)", type=["zip"])

if uploaded_file is not None:
    # Unzip the uploaded file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("uploaded_project")

    # Analyze each file in the project folder
    modified_files = {}
    for root, dirs, files in os.walk("uploaded_project"):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.py', '.js', '.java')):  # Add other file types as needed
                st.write(f"Analyzing {file_path}...")
                analysis_result = analyze_code(file_path)
                if analysis_result:
                    # Here you can modify the analysis result based on your requirements
                    # For demonstration, let's just append a comment
                    modified_files[file_path] = analysis_result.get("modified_code", "") + "\n# Changes made based on analysis"

    # Save modified files
    output_dir = "modified_project"
    save_modified_files(modified_files, output_dir)

    st.success("Code analysis and modifications completed!")
    st.write(f"Modified files saved in: {output_dir}")

    # Optionally, provide a download link for the modified project
    with zipfile.ZipFile('modified_project.zip', 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))

    st.download_button("Download Modified Project", "modified_project.zip")
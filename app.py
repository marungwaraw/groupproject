# app.py
import streamlit as st
import subprocess
import threading
import os
import pandas as pd

def run_people_counter():
    command = "python people_counter.py --prototxt detector/MobileNetSSD_deploy.prototxt --model detector/MobileNetSSD_deploy.caffemodel"
    
    # Run the command using subprocess and store the process object
    process = subprocess.Popen(command, shell=True)
    
    # Store the process ID in a file for later termination
    with open("process_id.txt", "w") as f:
        f.write(str(process.pid))

def stop_people_counter():
    # Read the process ID from the file and terminate the process
    try:
        with open("process_id.txt", "r") as f:
            process_id = int(f.read())
            os.system(f"taskkill /F /PID {process_id}")
    except FileNotFoundError:
        st.warning("Process ID file not found. The process may have already stopped.")

def generate_line_chart():
    # Read the counting data CSV file
    try:
        df = pd.read_csv("utils/data/logs/counting_data.csv")
        
        # Check if the necessary columns are present
        if 'Enter' in df.columns and 'Exit' in df.columns and 'Total' in df.columns:
            # Display line charts for Enter, Exit, and Total
            st.line_chart(df.set_index("In Time")["Enter"], use_container_width=True, key='enter', height=300)
            st.line_chart(df.set_index("In Time")["Exit"], use_container_width=True, key='exit', height=300)
            st.line_chart(df.set_index("In Time")["Total"], use_container_width=True, key='total', height=300)
        else:
            st.warning("Required columns ('Enter', 'Exit', 'Total') not found in the CSV file.")
    except FileNotFoundError:
        st.warning("Counting data file not found. Start counting to generate data.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("People Counter")

    if st.button("Display the Screen "):
        # Run the people_counter.py script in a separate thread
        thread = threading.Thread(target=run_people_counter)
        thread.start()

    if st.button("Hide the Screen"):
        # Stop the people_counter.py script
        stop_people_counter()

    # Display real-time counting information
    try:
        with open("utils/data/logs/counting_data.csv", "r") as csvfile:
            data = csvfile.read()
            st.text(data)
    except FileNotFoundError:
        st.warning("Counting data file not found. The counting may not have started yet.")

    # Button to display line charts
    if st.button("Display Line Charts"):
        generate_line_chart()

    # Add any additional reporting or visualization components here

if __name__ == "__main__":
    main()

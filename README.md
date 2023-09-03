# face-detection-opencv
The Facial Recognition Attendance Tracker is a Python-based system designed to automate attendance tracking in educational institutions or any organization that requires monitoring attendance. It uses facial recognition to identify and mark the attendance of registered individuals in real-time.

# Features
Facial Recognition: Utilizes the face_recognition library to identify individuals based on their facial features.
Real-time Monitoring: Tracks attendance as individuals pass in front of a webcam in real-time.
Firebase Integration: Stores student information in a Firebase Realtime Database and student images in Firebase Cloud Storage.
Dynamic Interface: Provides a dynamic graphical interface with student details, including name, major, ID, and attendance status.
Attendance Recording: Records attendance based on configurable time intervals.
Easy Setup: Simple setup with minimal dependencies.
Customizable: Easily extendable for different use cases and custom UI designs.
# Usage
Clone the Repository

git clone https://github.com/K-SAHASRA/face-detection-opencv.git

# Install Dependencies

pip install -r requirements.txt


# Configuration

Add your Firebase service account key (serviceAccountKey.json) and ensure Firebase Realtime Database and Cloud Storage are set up correctly.
Run the Tracker

# Usage Instructions

When the script is running, it will capture webcam input and recognize registered individuals.
Detected individuals' attendance will be updated in real-time based on the configured time interval.

# Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix: git checkout -b feature-name.
Make your changes and commit them: git commit -m 'Add feature'.
Push to the branch: git push origin feature-name.
Create a pull request on GitHub.
License
This project is licensed under the MIT License.

# Acknowledgments
OpenCV
face_recognition
cvzone
Firebase


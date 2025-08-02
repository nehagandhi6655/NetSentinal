NETSENTINAL - ** Network Intrusion Detection System 🔐**
NetSentinal is a Machine Learning-powered Network Intrusion Detection System (NIDS) built using Flask, Scikit-learn, and NSL-KDD dataset. It helps analyze network traffic data and classify threats such as DoS, Probe, R2L, U2R, or Normal, providing real-time insights and suggestions.


🚀 Features
Upload CSV files containing network traffic logs

Predicts attack type using trained Random Forest model

Displays row-wise classification

Generates summary pie chart

Provides security suggestions

Responsive UI with animated elements

Developer profile cards with hover effect

🛠️ Tech Stack
Python, Flask (Backend)

Scikit-learn, Pandas, NumPy (ML and Data Handling)

HTML, CSS, JavaScript (Frontend)

Matplotlib (Charts & Graphs)

📂 Project Structure
csharp
Copy
Edit
NETSENTINAL-NIDS/
│
├── app.py                      # Flask application
├── model/
│   └── trained_model.pkl       # Pre-trained ML model
├── static/
│   ├── css/                    # Custom styles
│   ├── js/                     # JavaScript for interactivity
│   └── images/                 # Charts & assets
├── templates/
│   ├── index.html              # Upload interface
│   └── result.html             # Output display
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1.Clone the repository:
git clone https://github.com/dev-26-17/NETSENTINAL-NIDS.git
cd NETSENTINAL-NIDS
2.Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate  # On Windows
3.Install dependencies:
pip install -r requirements.txt
4.Run the app:
python app.py
5.Open your browser and go to:
http://127.0.0.1:5000



🧠 About the Model
Trained using the NSL-KDD dataset

Uses LabelEncoding and StandardScaler for preprocessing

Random Forest Classifier (optimized with GridSearchCV)

Accuracy: ~89%

📊 Sample Output
Row-wise attack classification (Normal / DoS / R2L / Probe / U2R)

Pie chart summarizing attack distribution

Suggestions for detected threats

🧪 Test Your Own Dataset
Make sure your CSV has 41 feature columns (similar to NSL-KDD format)

Upload via the interface

Get immediate results and visual summary

👩‍💻 Developers
Devaki Vasundhara Kadupu

LinkedIn Profile

📜 License
This project is licensed under the MIT License.


from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
from collections import Counter


app = Flask(__name__, template_folder='templates', static_folder='static')

# Load model, encoders, and scaler
with open("model/trained_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Expected columns (same order used during training)
columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
    "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]

# Safe transformation function for label encoding
def safe_transform(le, val):
    if val in le.classes_:
        return le.transform([val])[0]
    else:
        # Handle unknown categories by returning a default value
        return -1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"})

        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()  # remove any leading/trailing spaces
        
# Remove header row if it's present (check first row)
        if df.columns[0].lower() == "duration":
            df = df[1:]

        df.columns = columns  # assign correct column names


        for col in ['protocol_type', 'service', 'flag']:
            le = label_encoders[col]
            df[col] = df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

        df_scaled = scaler.transform(df)
        predictions = model.predict(df_scaled)
        label_le = label_encoders['output']
        predicted_labels = label_le.inverse_transform(predictions)

        # Count each attack type
        count_dict = dict(Counter(predicted_labels))

        # Define colors for specific attack types
        attack_colors = {
        'normal': '#00cc66',      # green
        'neptune': '#ff4d4d',     # red
        'smurf': '#3399ff',       # blue
        'portsweep': '#ffcc00',   # yellow
        'satan': '#9966ff',       # purple
        'back': '#ff9933',        # orange
        'warezclient': '#cc00cc', # pink
        'guess_passwd': '#6600cc' # violet
    # Add more labels if needed
    }

# Match the colors to the labels dynamically
        labels = list(count_dict.keys())
        sizes = list(count_dict.values())
        colors = [attack_colors.get(label, '#999999') for label in labels]  # default gray if label not mapped

# Generate pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title("Attack Type Distribution")
        chart_path = os.path.join("static", "images", "prediction_chart.png")
        plt.savefig(chart_path)
        plt.close()


        # Generate suggestions
        suggestions = []
        for attack_type in count_dict.keys():
            if attack_type.lower() == "neptune":
                suggestions.append("Possible DoS activity detected. Check for unusual traffic volume.")
            elif attack_type.lower() == "portsweep":
                suggestions.append("Port scanning detected. Restrict unused ports and enable scan detection.")
            elif attack_type.lower() == "normal":
                suggestions.append("Traffic seems normal.")
            else:
                suggestions.append(f"Review activity for possible {attack_type} behavior.")
        return render_template("result.html", predictions=predicted_labels.tolist(), suggestion=suggestions, chart_path=chart_path)
        

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

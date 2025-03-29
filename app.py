from flask import Flask, request, jsonify, render_template
import os
from model import predict_data
import pandas as pd
from eda_images import generate_eda_images, get_image  # Importing image APIs

app = Flask(__name__, static_folder="static")

# ✅ Home Route → Load Frontend
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prediction')
def prediction():
    return render_template('predict.html')

@app.route('/insights')
def insights():
    return render_template('data-insights.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy-policy.html')

@app.route('/terms-of-service')
def tos():
    return render_template('terms-of-service.html')

@app.route('/get-predictions')
def get_predictions():
    return render_template('index.html')

# ✅ Prediction Route → POST request from frontend
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # ✅ Ensure all inputs are lists
        def ensure_list(value):
            return value if isinstance(value, list) else [value] if value else []

        categories = ensure_list(data.get("categories"))
        genders = ensure_list(data.get("genders"))
        age_groups = ensure_list(data.get("age_groups"))
        locations = ensure_list(data.get("locations"))
        payment_methods = ensure_list(data.get("payment_methods"))

        # Validate months_to_predict
        months_to_predict = int(data.get("months"))
        if months_to_predict is None or not str(months_to_predict).isdigit():
            return jsonify({"status": "error", "message": "Invalid 'months_to_predict' value"}), 400
        months_to_predict = int(months_to_predict)

        # ✅ Call prediction function with correctly formatted lists
        monthly_revenue, total_revenue = predict_data(
            categories, genders, age_groups, locations, payment_methods, months_to_predict
        )

        total_revenue /= 5
        if monthly_revenue is None:
            return jsonify({
                'status': 'error',
                'message': 'No data available for the selected filters.'
            }), 400

        return jsonify({
            'status': 'success',
            'monthly_revenue': monthly_revenue.to_dict(orient='records'),
            'total_revenue': f"₹{total_revenue:,.0f}"
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

file_path = "data/clothing_shop_preprocessed_data.csv"
df = pd.read_csv(file_path)

@app.route("/api/dataset_overview", methods=["GET"])
def dataset_overview():
    """API to return dataset summary."""
    summary = {
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Dataset Size (MB)": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "Columns": list(df.columns),
        "Head": df.head(12).to_dict(orient="records"),  # Convert first 5 rows to JSON format
    }
    return jsonify(summary)

# ✅ EDA Image Generation APIs (Imported)
@app.route("/api/generate_eda_images")
def eda_images():
    return generate_eda_images()

@app.route("/static/images/<filename>")
def serve_image(filename):
    return get_image(filename)

if __name__ == '__main__':
    app.run(debug=True)

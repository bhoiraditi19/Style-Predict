from flask import Flask, request, jsonify, render_template, send_file
import os
from model import predict_data
import pandas as pd
from eda_images import generate_eda_images, get_image  # Importing image APIs
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import io

# Load environment variables from .env file
load_dotenv()


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

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    try:
        data = request.json
        report_name = data.get('report_name', '')
        monthly_revenue = data.get('monthly_revenue', [])
        total_revenue = data.get('total_revenue', '')

        # Create PDF
        pdf_output = io.BytesIO()
        from reportlab.lib.pagesizes import landscape
        if report_name == "Dataset Summary":
            doc = SimpleDocTemplate(pdf_output, pagesize=landscape(letter))
        else:
            doc = SimpleDocTemplate(pdf_output, pagesize=letter)
        styles = getSampleStyleSheet()

        elements = []

        # Map report names to image files
        image_map = {
            "Monthly Revenue": "monthly_revenue.png",
            "Top-Selling Categories": "top_categories.png",
            "Worst-Selling Categories": "worst_categories.png",
            "Top 5 Locations": "top_locations.png",
            "Bottom 5 Locations": "bottom_locations.png",
            "Age Group vs Revenue": "age_revenue.png",
            "Gender-wise Revenue": "gender_revenue.png",
            "Payment Method Distribution": "payment_method_distribution.png",
            "Revenue by Payment Method": "revenue_by_payment_method.png",
            "Seasonal Revenue": "seasonal_revenue.png",
            "Discount Impact on Sales": "discount_impact.png",
            "Diwali & New Year Sales": "diwali_newyear_sales.png",
            "Peak & Lowest Sales Month": "peak_lowest_sales.png",
            "Month-over-Month Growth": "mom_growth.png",
        }

        from reportlab.platypus import Paragraph

        if report_name == "Dataset Summary":
            # Fetch actual dataset summary
            summary = {
                "Total Rows": len(df),
                "Total Columns": len(df.columns),
                "Dataset Size (MB)": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
                "Columns": list(df.columns),
                "Head": df.head(12).to_dict(orient="records"),
            }

            # Title
            title = Paragraph("Dataset Summary Report", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))

            # Summary details
            elements.append(Paragraph(f"Total Rows: {summary['Total Rows']}", styles['Normal']))
            elements.append(Paragraph(f"Total Columns: {summary['Total Columns']}", styles['Normal']))
            elements.append(Paragraph(f"Dataset Size: {summary['Dataset Size (MB)']} MB", styles['Normal']))
            elements.append(Spacer(1, 12))

            # Create table with all columns in landscape with dynamic column widths
            from reportlab.lib.styles import ParagraphStyle

            # Define a small paragraph style for wrapping
            small_style = ParagraphStyle(
                name='small',
                fontSize=5,
                leading=6,
                alignment=1,  # center alignment
                spaceAfter=2,
                spaceBefore=2,
            )

            # Wrap headers and data in Paragraphs for wrapping
            table_data = [ [Paragraph(col, small_style) for col in summary['Columns']] ]
            for row in summary['Head']:
                table_data.append([Paragraph(str(row[col]), small_style) for col in summary['Columns']])

            from reportlab.lib.pagesizes import landscape
            from reportlab.lib.units import inch

            # Set landscape letter with smaller margins
            page_width, page_height = landscape(letter)
            left_margin = right_margin = 36  # 0.5 inch margins
            usable_width = page_width - left_margin - right_margin

            num_cols = len(summary['Columns'])
            col_width = usable_width / num_cols
            col_widths = [col_width] * num_cols

            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            elements.append(table)


        elif report_name in image_map:
            # Add image to PDF
            try:
                image_path = os.path.join(os.path.dirname(__file__), 'static', 'images', image_map[report_name])
                if os.path.exists(image_path):
                    img = Image(image_path, width=400, height=300)
                    elements.append(Paragraph(f"{report_name} Report", styles['Title']))
                    elements.append(Spacer(1, 12))
                    elements.append(img)
                else:
                    elements.append(Paragraph(f"{report_name} Report - Image not found", styles['Title']))
            except Exception as e:
                elements.append(Paragraph(f"{report_name} Report - Error loading image: {str(e)}", styles['Title']))

        else:
            # For other reports, use dummy data or prediction-like data
            if report_name:
                total_revenue = f"Report: {report_name} - Total Revenue Rs. 12345"
                monthly_revenue = [
                    {'Year': 2023, 'Month': 'Jan', 'Predicted_Revenue': 10000},
                    {'Year': 2023, 'Month': 'Feb', 'Predicted_Revenue': 12000},
                    {'Year': 2023, 'Month': 'Mar', 'Predicted_Revenue': 15000},
                ]

            # Title
            title = Paragraph("Sales Prediction Report", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))

            # Total Revenue
            if isinstance(total_revenue, str):
                total_revenue = total_revenue.replace('₹', 'Rs.')

            total_para = Paragraph(f"Total Predicted Revenue: {total_revenue}", styles['Normal'])
            elements.append(total_para)
            elements.append(Spacer(1, 12))

            # Table data
            table_data = [['Year', 'Month', 'Predicted Revenue (Rs.)']]
            for row in monthly_revenue:
                year = str(row.get('Year', ''))
                month = str(row.get('Month', ''))
                revenue = str(row.get('Predicted_Revenue', '')).replace('₹', 'Rs.')
                table_data.append([year, month, revenue])

            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

        import sys
        print("Starting PDF build...", file=sys.stderr)
        doc.build(elements)
        print("PDF build completed.", file=sys.stderr)
        pdf_output.seek(0)

        # Save PDF to temp file for manual inspection
        temp_pdf_path = os.path.join(os.path.dirname(__file__), 'temp_report.pdf')
        with open(temp_pdf_path, 'wb') as f:
            f.write(pdf_output.getbuffer())
        print(f"PDF saved to {temp_pdf_path}")

        # Print PDF size
        pdf_size = len(pdf_output.getvalue())
        print(f"Generated PDF size: {pdf_size} bytes")

        from flask import send_file
        pdf_output.seek(0)
        return send_file(
            pdf_output,
            as_attachment=True,
            download_name='report.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        print("Error generating PDF:", traceback.format_exc())
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

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    email_body = f"""
    You received a new contact form submission:

    Name: {name}
    Email: {email}
    Message:
    {message}
    """

    try:
        # Email sending logic
        send_email("shaileshhawale64@gmail.com", "New Contact Form Submission", email_body)
        return jsonify({'message': 'Message sent successfully!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to send message.'}), 500

def send_email(to_email, subject, body):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    # Using Gmail SMTP (you can change this if needed)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)

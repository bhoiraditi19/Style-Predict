# StylePredict
Clothing Store Sales Prediction Model


## 🔗 Live Demo  
https://fashionforecast-h008.onrender.com/

---

## 💻 Tech Stack Used

- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Backend**: Python (Flask)
- **Machine Learning**: XGBoost, Scikit-learn, Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Deployment**: WSGI + Gunicorn

---

## 📌 Project Description

This project is a machine learning-powered dashboard built to **analyze and forecast e-commerce clothing store sales**.  
It includes detailed visualizations of trends, payment methods, and predicted sales based on historical transaction data.  

✅ **Why I built it:**  
To combine my knowledge of machine learning and web development into a full-stack project that solves a real-world business problem — helping businesses forecast future sales with clarity and interactivity.

---

## 🖼️ Screenshots

| Dataset Summary | Feature Importance |
|------------------|----------------------|
| ![Dataset](screenshots/dataset_summary.png) | ![Feature](screenshots/feature_importance.png) |

| Monthly Trends | Payment Distribution |
|------------------|----------------------|
| ![Trend](screenshots/monthly_revenue.png) | ![Payment](screenshots/payment_methods.png) |

| Prediction Page | Home Page |
|------------------|------------------|
| ![Predict](screenshots/prediction_page.png) | ![Home](screenshots/homepage.png) |

| About Us | |
|------------------|------------------|
| ![About](screenshots/about_us.png) | |

---

## ⭐ Features

- 📂 **Preloaded Dataset Analysis**  
  App uses a built-in historical transaction dataset — no upload required.

- 📊 **Insights Page for EDA (Exploratory Data Analysis)**  
  A dedicated “Insights” page shows visualizations such as category-wise sales, payment distributions, and trends — all rendered from backend-generated images.

- 🤖 **XGBoost Model-Based Prediction**  
  Sales forecasting is powered by a pre-trained XGBoost model built using realistic, real-world purchase behavior.

- 🎯 **Filter-Based Custom Predictions**  
  Users can dynamically adjust inputs like:
  - Product category  
  - Age group  
  - Gender  
  - Location  
  - Payment method  
  - Future time horizon (in months)

- 📈 **Forecast Future Sales**  
  App predicts total future sales (1 to 12 months ahead) based on filtered criteria and displays results with clear visual styling.

- 🌐 **Multiple Web Pages**  
  Fully structured frontend with the following routes/pages:
  - Home  
  - Prediction  
  - Insights (EDA)  
  - About Us  
  - Contact Us  
  - Privacy Policy  

- 📱 **Responsive UI**  
  The app is mobile-friendly on most pages (except Insights, currently desktop-optimized).

---

## 🛠 Installation / Usage Instructions


```bash
# Clone the repository
git clone https://github.com/HawaleShailesh004/Style-Predict.git
cd Style-Predict

# (Optional) Create and activate a virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

Then open http://localhost:5000 in your browser.

🚧 Future Improvements / What I Learned
🔧 Future Plans:
Improve responsiveness of the Insights page

Add export options (CSV/PDF) for predictions

Add interactive graphs using Plotly for live updates

Deploy live version on Render or another cloud platform


📚 What I Learned:
End-to-end ML pipeline integration in a web app

XGBoost model training and deployment

Backend image rendering for EDA

Frontend/backend interaction using Flask templates

Practical use of filters for dynamic prediction

Building clean, scalable folder structures for web apps

🙋‍♂️ Author
Shailesh Hawale
Email: shaileshhawale004@gmail.com



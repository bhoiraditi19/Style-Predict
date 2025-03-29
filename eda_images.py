from flask import Blueprint, jsonify, send_from_directory
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import os

# Use non-GUI backend for Matplotlib
matplotlib.use('Agg')

# Create a blueprint for EDA image APIs
eda_blueprint = Blueprint('eda', __name__)

# Load dataset
FILE_PATH = "data/clothing_shop_preprocessed_data.csv"
df = pd.read_csv(FILE_PATH)

print(df.columns)

# Convert 'Year' and 'Month' into a single datetime column
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01")
df.drop(columns=["Year", "Month"], inplace=True)

df["Total_Revenue"] = df["Total_Revenue"] / 10 

# Create a directory for saving images
IMAGE_DIR = "static/images/"
os.makedirs(IMAGE_DIR, exist_ok=True)

# ✅ Function to format Y-axis values in INR (Crores & Thousands)
def format_inr(value, _):


    if value >= 1e7:  # 10 million = 1 Crore
        return f"₹{value/1e7:.1f}C"
    elif value >= 1e3:  # Thousands
        return f"₹{value/1e3:.0f}T"
    return f"₹{value:.0f}"



# ✅ Function to save charts
def save_chart(fig, filename):
    filepath = os.path.join(IMAGE_DIR, filename)
    fig.savefig(filepath, bbox_inches="tight")
    plt.close(fig)

# ✅ Generate all EDA charts with formatted Y-values
def generate_eda_images():
    """Generate and save all EDA-related images with uniform size & proper formatting."""

  ## 📈 Monthly Revenue Trend
    monthly_revenue = df.groupby("Date")["Total_Revenue"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(data=monthly_revenue, x="Date", y="Total_Revenue", ax=ax)
    ax.set_title("Monthly Revenue Trend", fontsize=16)
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("Revenue (₹)", fontsize=14)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b-%Y"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    ax.tick_params(axis='x', rotation=45)
    save_chart(fig, "monthly_revenue.png")

    ## 🏆 Top-Selling Categories
    top_categories = df.groupby("Category")["Total_Revenue"].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=top_categories.index, y=top_categories.values, ax=ax, palette="Blues")
    ax.set_title("Top-Selling Categories", fontsize=16)
    ax.set_xlabel("Category", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    save_chart(fig, "top_categories.png")

    ## 📉 Worst-Selling Categories
    worst_categories = df.groupby("Category")["Total_Revenue"].sum().sort_values().head(5)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=worst_categories.index, y=worst_categories.values, ax=ax, palette="Reds")
    ax.set_title("Worst-Selling Categories", fontsize=16)
    ax.set_xlabel("Category", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    ax.tick_params(axis='x', rotation=30)
    save_chart(fig, "worst_categories.png")

    ## 📍 Top 5 Locations by Revenue
    top_locations = df.groupby("Location")["Total_Revenue"].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=top_locations.index, y=top_locations.values, ax=ax, palette="Greens")
    ax.set_title("Top 5 Locations by Revenue", fontsize=16)
    ax.set_xlabel("Location", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    save_chart(fig, "top_locations.png")

    ## 📍 Bottom 5 Locations by Revenue
    top_locations = df.groupby("Location")["Total_Revenue"].sum().sort_values(ascending=True).head(5)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=top_locations.index, y=top_locations.values, ax=ax, palette="Oranges")
    ax.set_title("Bottom 5 Locations by Revenue", fontsize=16)
    ax.set_xlabel("Location", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    save_chart(fig, "bottom_locations.png")

    ## 👥 Age Group vs Revenue
    age_revenue = df.groupby("Age_Group")["Total_Revenue"].sum()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=age_revenue.index, y=age_revenue.values, ax=ax, palette="Purples")
    ax.set_title("Revenue by Age Group", fontsize=16)
    ax.set_xlabel("Age Group", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    # ✅ Ensure formatter is applied
    formatter = plt.FuncFormatter(format_inr)
    ax.yaxis.set_major_formatter(formatter)
    save_chart(fig, "age_revenue.png")




    ## 💳 Payment Method Distribution (Fixed)
    payment_counts = df["Payment_Method"].value_counts(normalize=True) * 100  # Convert to percentage
    fig, ax = plt.subplots(figsize=(12, 8))
    payment_counts.plot(
        kind="pie", 
        autopct=lambda p: f"{p:.1f}%" if p > 0 else "",  # Only show non-zero percentages
        ax=ax, 
        colors=sns.color_palette("pastel"),
        startangle=140,  # Rotate for better visibility
        wedgeprops={'edgecolor': 'black'}  # Add black edges for better separation
    )
    ax.set_title("Payment Method Distribution", fontsize=16)
    ax.set_ylabel("")
    save_chart(fig, "payment_method_distribution.png")

    ## 💳 Revenue by Payment Method Distribution
    payment_revenue = df.groupby("Payment_Method")["Total_Revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=payment_revenue.index, y=payment_revenue.values, ax=ax, palette="coolwarm")
    ax.set_title("Revenue by Payment Method", fontsize=16)
    ax.set_xlabel("Payment Method", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    # ✅ Format y-axis values (e.g., 800,000 → 800K)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))  # Convert to Lakhs
    save_chart(fig, "revenue_by_payment_method.png")



    # 🎇 Diwali & New Year Sales Impact
    seasonality_revenue = df.groupby(["Is_Diwali_Season", "Is_New_Year_Season"])["Total_Revenue"].sum()

    # ✅ Compute Non-Festival revenue separately
    non_festival_revenue = df[
        (df["Is_Diwali_Season"] == 0) & (df["Is_New_Year_Season"] == 0)
    ]["Total_Revenue"].sum()

    # ✅ Convert to DataFrame and append Non-Festival revenue correctly
    seasonality_revenue = seasonality_revenue.reset_index()
    seasonality_revenue = pd.concat([
        seasonality_revenue,
        pd.DataFrame({"Is_Diwali_Season": [0], "Is_New_Year_Season": [0], "Total_Revenue": [non_festival_revenue]})
    ]).drop_duplicates().set_index(["Is_Diwali_Season", "Is_New_Year_Season"])["Total_Revenue"]

    # ✅ Define labels for X-axis
    seasonality_labels = {
        (0, 0): "Non-Festival",
        (1, 0): "Diwali",
        (0, 1): "New Year",
        (1, 1): "Diwali & New Year"
    }

    # ✅ Create Bar Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    seasonality_revenue.plot(kind="bar", color=["green", "gold", "blue", "purple"], ax=ax)

    ax.set_title("Diwali & New Year Sales Impact", fontsize=16)
    ax.set_xlabel("Season", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)

    # ✅ Set X-axis labels dynamically
    ax.set_xticklabels([seasonality_labels[idx] for idx in seasonality_revenue.index], rotation=30)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    save_chart(fig, "diwali_newyear_sales.png")




    # 🎇 Revenue by Season
    season_columns = ["Is_Diwali_Season", "Is_New_Year_Season", "Is_Summer_Season", "Is_Winter_Season"]
    season_labels = ["Diwali", "New Year", "Summer", "Winter"]

    # ✅ Calculate total revenue for each season
    seasonal_revenue = {label: df[df[season] == 1]["Total_Revenue"].sum() for season, label in zip(season_columns, season_labels)}

    # ✅ Convert to DataFrame for plotting
    seasonal_revenue_df = pd.DataFrame(list(seasonal_revenue.items()), columns=["Season", "Total_Revenue"])

    # ✅ Create Bar Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=seasonal_revenue_df, x="Season", y="Total_Revenue", ax=ax, palette="coolwarm")

    ax.set_title("Revenue by Season", fontsize=16)
    ax.set_xlabel("Season", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))

    save_chart(fig, "seasonal_revenue.png")






    ## 🏷️ Discount Impact on Sales
    discount_months = df[df["Total_Revenue"].diff() > 0]
    no_discount_months = df[df["Total_Revenue"].diff() <= 0]
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=["Discount Months", "No Discount Months"], 
                y=[discount_months["Total_Revenue"].sum(), no_discount_months["Total_Revenue"].sum()], ax=ax)
    ax.set_title("Impact of Discounts on Sales", fontsize=16)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    save_chart(fig, "discount_impact.png")

    ## 📈 Month-over-Month Revenue Growth
    df["MoM_Growth"] = df["Total_Revenue"].pct_change() * 100
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(data=df, x="Date", y="MoM_Growth", ax=ax, marker="o")
    ax.axhline(0, color="red", linestyle="dashed")
    ax.set_title("Month-over-Month Revenue Growth (%)", fontsize=16)
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("Growth (%)", fontsize=14)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b-%Y"))
    ax.tick_params(axis='x', rotation=45)
    save_chart(fig, "mom_growth.png")

    # 📅 Peak & Lowest Revenue Months
    monthly_revenue = df.groupby("Date")["Total_Revenue"].sum()
    top_5_months = monthly_revenue.nlargest(5)
    bottom_5_months = monthly_revenue.nsmallest(5)
    peak_lowest_months = pd.concat([top_5_months, bottom_5_months]).sort_values()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=peak_lowest_months.index.strftime("%b-%Y"), y=peak_lowest_months.values, ax=ax, palette="coolwarm")
    ax.set_title("Peak & Lowest Revenue Months", fontsize=16)
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("Total Revenue (₹)", fontsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_inr))
    ax.tick_params(axis="x", rotation=45)
    save_chart(fig, "peak_lowest_sales.png")


    return {"message": "EDA images generated successfully!"}

# ✅ API Endpoint to trigger image generation
@eda_blueprint.route('/api/generate_eda_images', methods=['GET'])
def api_generate_eda_images():
    return generate_eda_images()

# ✅ API to serve images
@eda_blueprint.route('/api/images/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

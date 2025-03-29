// // Function to fetch dataset overview (Total Rows & File Size)
// async function fetchDatasetInfo() {
//     try {
//         const response = await fetch("/api/dataset_overview");
//         const data = await response.json();
        
//         document.getElementById("total-rows").innerText = data.total_rows;
//         document.getElementById("file-size").innerText = `${data.file_size} MB`;
//     } catch (error) {
//         console.error("Error fetching dataset overview:", error);
//     }
// }

// // Function to create a chart dynamically
// async function createChart(apiURL, canvasId, labelKey, valueKey, title, chartType = "bar", xLabel = "", yLabel = "") {
//     try {
//         const response = await fetch(apiURL);
//         const data = await response.json();

//         const labels = data.map(item => item[labelKey]);
//         const values = data.map(item => item[valueKey]);

//         const ctx = document.getElementById(canvasId).getContext("2d");

//         new Chart(ctx, {
//             type: chartType,
//             data: {
//                 labels: labels,
//                 datasets: [{
//                     label: title,
//                     data: values,
//                     backgroundColor: [
//                         "#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#BA68C8"
//                     ],
//                     borderColor: "#ffffff",
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false,
//                 plugins: {
//                     legend: {
//                         display: true,
//                         labels: { color: "#ffffff" }
//                     }
//                 },
//                 scales: {
//                     x: { 
//                         title: { display: true, text: xLabel, color: "#ffffff" },
//                         ticks: { color: "#ffffff" }
//                     },
//                     y: { 
//                         title: { display: true, text: yLabel, color: "#ffffff" },
//                         ticks: { color: "#ffffff" }
//                     }
//                 }
//             }
//         });
//     } catch (error) {
//         console.error(`Error fetching data for ${canvasId}:`, error);
//     }
// }

// // Smooth Appear Animation on Scroll
// const sections = document.querySelectorAll(".insight-section");

// function checkVisibility() {
//     sections.forEach(section => {
//         const rect = section.getBoundingClientRect();
//         if (rect.top < window.innerHeight - 50) {
//             section.classList.add("visible");
//         }
//     });
// }

// window.addEventListener("scroll", checkVisibility);

// // Fetch all data & render charts
// fetchDatasetInfo();
// createChart("/api/monthly_sales", "monthlyRevenueChart", "Date", "Total_Revenue", "Monthly Sales", "line", "Months", "Revenue (₹)");
// createChart("/api/top_categories", "categorySalesChart", "Category", "Total_Revenue", "Category Sales", "bar", "Product Category", "Revenue (₹)");
// createChart("/api/payment_method_usage", "paymentChart", "Payment_Method", "Total_Revenue", "Payment Methods", "doughnut", "", "");
// createChart("/api/seasonal_sales", "seasonalChart", "Season", "Total_Revenue", "Seasonal Sales Impact", "pie", "", "");

// // Trigger animation check on load
// document.addEventListener("DOMContentLoaded", checkVisibility);

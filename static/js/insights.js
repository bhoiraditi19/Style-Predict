// Sample Chart.js implementation for interactivity
document.addEventListener("DOMContentLoaded", function() {
    const pieCtx = document.getElementById("pieChart").getContext("2d");
    new Chart(pieCtx, {
        type: "pie",
        data: {
            labels: ["Category A", "Category B", "Category C"],
            datasets: [{
                data: [40, 30, 30],
                backgroundColor: ["#3498db", "#e74c3c", "#2ecc71"]
            }]
        }
    });

    const lineCtx = document.getElementById("lineChart").getContext("2d");
    new Chart(lineCtx, {
        type: "line",
        data: {
            labels: ["2022", "2023", "2024"],
            datasets: [{
                label: "Revenue Growth",
                data: [100, 150, 200],
                borderColor: "#e67e22",
                fill: false
            }]
        }
    });

  
});

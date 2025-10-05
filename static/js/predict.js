document.addEventListener("DOMContentLoaded", function () {
  function setupDropdown(dropdownId, listId, selectedContainerId) {
    const dropdown = document.getElementById(dropdownId);
    const list = document.getElementById(listId);
    const selectedContainer = document.getElementById(selectedContainerId);
    const checkboxes = list.querySelectorAll("input[type='checkbox']");

    // Add "Select All" option
    const selectAllLi = document.createElement("li");
    selectAllLi.innerHTML = `<input type="checkbox" id="${listId}-select-all"> Select All`;
    list.prepend(selectAllLi);
    const selectAllCheckbox = document.getElementById(`${listId}-select-all`);

    // Toggle dropdown visibility on click
    dropdown.addEventListener("click", function () {
      list.classList.toggle("show");
    });

    // Handle selection for individual checkboxes
    list.addEventListener("click", function (event) {
      if (
        event.target.tagName === "INPUT" &&
        event.target !== selectAllCheckbox
      ) {
        const value = event.target.value;
        if (event.target.checked) {
          addSelectedItem(value, event.target);
        } else {
          removeSelectedItem(value);
        }
        updateSelectAllState();
      }
    });

    // Handle "Select All" click
    selectAllCheckbox.addEventListener("change", function () {
      checkboxes.forEach((checkbox) => {
        checkbox.checked = selectAllCheckbox.checked;
        if (selectAllCheckbox.checked) {
          addSelectedItem(checkbox.value, checkbox);
        } else {
          removeSelectedItem(checkbox.value);
        }
      });
    });

    // Function to add selected item
    function addSelectedItem(value, checkboxElement) {
      // Prevent duplicate entries
      if (selectedContainer.querySelector(`[data-value='${value}']`)) return;

      const item = document.createElement("div");
      item.className = "selected-item";
      item.innerHTML = `${value} <span class="remove-item">&times;</span>`;
      item.dataset.value = value;
      selectedContainer.appendChild(item);

      // Remove item when clicking ❌
      item.querySelector(".remove-item").addEventListener("click", function () {
        checkboxElement.checked = false;
        item.remove();
        updateSelectAllState();
      });
    }

    // Function to remove selected item
    function removeSelectedItem(value) {
      [...selectedContainer.children].forEach((child) => {
        if (child.dataset.value === value) child.remove();
      });
    }

    // Update "Select All" checkbox state based on individual selections
    function updateSelectAllState() {
      const allChecked = [...checkboxes].every((cb) => cb.checked);
      const someChecked = [...checkboxes].some((cb) => cb.checked);
      selectAllCheckbox.checked = allChecked;
      selectAllCheckbox.indeterminate = someChecked && !allChecked;
    }

    list.addEventListener("click", function (event) {
      event.stopPropagation();
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", function (e) {
      if (!dropdown.contains(e.target) && !list.contains(e.target)) {
        list.classList.remove("show");
      }
    });
  }

  // Initialize dropdowns
  setupDropdown(
    "categories-dropdown",
    "categories-list",
    "selected-categories"
  );
  setupDropdown(
    "age-groups-dropdown",
    "age-groups-list",
    "selected-age-groups"
  );
  setupDropdown("locations-dropdown", "locations-list", "selected-locations");
  setupDropdown(
    "payment-methods-dropdown",
    "payment-methods-list",
    "selected-payment-methods"
  );
  setupDropdown("genders-dropdown", "genders-list", "selected-genders");

  // ✅ Form Submission
  document
    .getElementById("prediction-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      // Collect selected values
      const categories = [
        ...document.querySelectorAll("#categories-list input:checked"),
      ]
        .filter((el) => el.id !== "categories-list-select-all")
        .map((el) => el.value);

      const age_groups = [
        ...document.querySelectorAll("#age-groups-list input:checked"),
      ]
        .filter((el) => el.id !== "age-groups-list-select-all")
        .map((el) => el.value);

      const locations = [
        ...document.querySelectorAll("#locations-list input:checked"),
      ]
        .filter((el) => el.id !== "locations-list-select-all")
        .map((el) => el.value);

      const payment_methods = [
        ...document.querySelectorAll("#payment-methods-list input:checked"),
      ]
        .filter((el) => el.id !== "payment-methods-list-select-all")
        .map((el) => el.value);

      const genders = [
        ...document.querySelectorAll("#genders-list input:checked"),
      ]
        .filter((el) => el.id !== "genders-list-select-all")
        .map((el) => el.value);

      const months = document.getElementById("months_to_predict").value;

      // alert(
      //   JSON.stringify({
      //     categories,
      //     age_groups,
      //     genders,
      //     locations,
      //     payment_methods,
      //     months,
      //   })
      // );

      // Send data to backend
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          categories,
          age_groups,
          genders,
          locations,
          payment_methods,
          months,

          // categories: ["Shirts"],
          // age_groups: ["18-25"],
          // genders: ["Male"],
          // locations: ["Mumbai"],
          // payment_methods: ["UPI"],
          // months: "10",
        }),
      });

      const result = await response.json();

      // ✅ Display results
      if (result.status === "success") {
        document.getElementById("results").style.display = "grid";
        document.getElementById(
          "total-revenue"
        ).innerText = `Total Revenue: ${result.total_revenue}`;

        const tableBody = document.querySelector("#monthly-results tbody");
        tableBody.innerHTML = "";
        result.monthly_revenue.forEach((row) => {
          tableBody.innerHTML += `<tr>
                    <td>${row.Year}</td>
                    <td>${row.Month}</td>
                    <td>₹${row.Predicted_Revenue}</td>
                </tr>`;
        });

        const monthsLabels = result.monthly_revenue.map(
          (row) => `${row.Month} / ${String(row.Year).slice(-2)}`
        );
        const revenueData = result.monthly_revenue.map(
          (row) => row.Predicted_Revenue
        );

        // ✅ Create or update the line chart

        const ctx = document.getElementById("predictionChart").getContext("2d");

        if (window.predictionChart) {
          try {
            window.predictionChart.destroy();
          } catch (e) {
            console.log("Error destroying chart:", e);
          }
        }

        window.predictionChart = new Chart(ctx, {
          type: "line",
          data: {
            labels: monthsLabels,
            datasets: [
              {
                label: "Predicted Revenue (₹)",
                data: revenueData,
                borderColor: "#fff", // 🔹 Custom Line Color (Orange-Red)
                backgroundColor: "rgba(55, 43, 95, 0.5)", // 🔹 Fill Area Color (Light Orange-Red)
                borderWidth: 5, // 🔹 Line Thickness
                pointRadius: 8, // 🔹 Size of Data Points
                pointBackgroundColor: "#000", // 🔹 Data Point Color (Black)
                // pointBorderColor: "#ff5733", // 🔹 Data Point Border Color
                pointHoverRadius: 10, // 🔹 Larger Points on Hover
                pointHoverBackgroundColor: "#fff", // 🔹 Change Point Color on Hover
                fill: true, // 🔹 Fill Area Under Line
                tension: 0.3, // 🔹 Smooth Curved Line
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                title: {
                  display: true,
                  text: "Months",
                  color: "#fff", // 🔹 X-Axis Label Color
                  font: { size: 26, weight: "700" },
                },
                ticks: { color: "#fff", font: { size: 18, weight: "bold" } }, // 🔹 X-Axis Ticks Color
                grid: { color: "rgba(0, 0, 0, 0.5)" }, // 🔹 X-Axis Grid Color
              },
              y: {
                title: {
                  display: true,
                  text: "Revenue (₹)",
                  color: "#fff", // 🔹 Y-Axis Label Color
                  font: { size: 26, weight: "700" },
                },
                ticks: { color: "#fff", font: { size: 18, weight: "bold" } }, // 🔹 Y-Axis Ticks Color
                grid: { color: "rgba(0, 0, 0,0.5)" }, // 🔹 Y-Axis Grid Color
              },
            },
            plugins: {
              legend: {
                labels: {
                  color: "#fff", // 🔹 Legend Text Color
                  font: { size: 25, weight: "500" },
                },
              },
              tooltip: {
                backgroundColor: "#444", // 🔹 Tooltip Background Color
                titleColor: "#fff", // 🔹 Tooltip Title Color
                bodyColor: "#fff", // 🔹 Tooltip Text Color
                borderColor: "#ff5733", // 🔹 Tooltip Border Color
                borderWidth: 2,
              },
            },
          },
        });

        console.log("Chart created successfully");

        // Add download PDF handler
        document.getElementById("download-pdf").addEventListener("click", function() {
            fetch("/download_pdf", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    monthly_revenue: result.monthly_revenue,
                    total_revenue: result.total_revenue
                })
            }).then(response => response.blob()).then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'prediction_report.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
            }).catch(error => {
                console.error('Error downloading PDF:', error);
                alert('Error downloading PDF');
            });
        });

      } else {
        alert(result.message);
      }
      // ✅ Extract data for the line chart
    });
});

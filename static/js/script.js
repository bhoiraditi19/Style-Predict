document.getElementById("prediction-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        categories: Array.from(document.getElementById("categories").selectedOptions).map(option => option.value),
        genders: Array.from(document.getElementById("genders").selectedOptions).map(option => option.value),
        age_groups: Array.from(document.getElementById("age_groups").selectedOptions).map(option => option.value),
        locations: Array.from(document.getElementById("locations").selectedOptions).map(option => option.value),
        payment_methods: Array.from(document.getElementById("payment_methods").selectedOptions).map(option => option.value),
        months_to_predict: document.getElementById("months_to_predict").value
    };

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.status === 'success') {
        document.getElementById('results').style.display = 'block';
        document.getElementById('total-revenue').innerText = `Total Revenue: ${result.total_revenue}`;

        const tableBody = document.querySelector('#monthly-results tbody');
        tableBody.innerHTML = '';
        result.monthly_revenue.forEach(row => {
            tableBody.innerHTML += `<tr>
                <td>${row.Year}</td>
                <td>${row.Month}</td>
                <td>${row.Predicted_Revenue}</td>
            </tr>`;
        });
    } else {
        alert(result.message);
    }
});

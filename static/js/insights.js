document.addEventListener("DOMContentLoaded", function () {
  function setupDownloadButtons() {
    const buttons = document.querySelectorAll(".download-sub-pdf");
    buttons.forEach((button) => {
      button.removeEventListener("click", handleDownloadClick);
      button.addEventListener("click", handleDownloadClick);
    });
  }

  function handleDownloadClick(event) {
    const button = event.currentTarget;
    const reportName = button.getAttribute("data-report");

    fetch("/download_pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        report_name: reportName,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${reportName.replace(/\s+/g, "_").toLowerCase()}_report.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error("Error downloading PDF:", error);
        alert("Failed to download PDF: " + error.message);
      });
  }

  setupDownloadButtons();
});

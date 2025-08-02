// Toggle profile popup on hover (with persistent hover)
const names = document.querySelectorAll(".name");
const popups = document.querySelectorAll(".profile-popup");

names.forEach((name) => {
    const popupId = name.getAttribute("data-profile");
    const popup = document.getElementById(popupId);
    // Function to show the popup
    function showProfilePopup() {
    document.querySelector('.profile-popup').style.display = 'block';
    }



    name.addEventListener("mouseenter", () => {
        // Hide all other popups
        popups.forEach((p) => (p.style.display = "none"));
        popup.style.display = "block";
    });

    name.addEventListener("mouseleave", () => {
        setTimeout(() => {
            popup.style.display = "none";
        }, 3000); // Delay to allow hover on popup
    });

    popup.addEventListener("mouseenter", () => {
        popup.style.display = "block";
    });

    popup.addEventListener("mouseleave", () => {
        popup.style.display = "none";
    });
});

// Upload handler
document.getElementById("uploadForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("csvFile");
    const resultDiv = document.getElementById("result");

    const file = fileInput.files[0];

    

if (!file) {
    resultDiv.innerHTML = '<span style="color:red;">Please select a CSV file to upload.</span>';
    return;
}

const formData = new FormData();
formData.append("file", file);

resultDiv.innerHTML = "⏳ Predicting... Please wait.";

fetch("/predict", {
    method: "POST",
    body: formData,
})
.then((response) => {
    if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
    }
    return response.text(); // Changed from response.json()
})
.then((html) => {
    document.open();
    document.write(html);
    document.close();
})



    .catch((error) => {
        console.error("Fetch error:", error);
        resultDiv.innerHTML = `<span style="color:red;">Error: ${error.message}</span>`;
    });
});
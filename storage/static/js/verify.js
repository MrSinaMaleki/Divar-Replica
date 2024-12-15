document.addEventListener("DOMContentLoaded", function () {
  const submitButton = document.getElementById("submit-verification-form");

  submitButton.addEventListener("click", async function (event) {
    event.preventDefault(); // Prevent default button behavior

    // Get form inputs
    const nationality = document.getElementById("nationality").value;
    const idNumber = document.getElementById("national-code").value;

    // Validate inputs (optional)
    if (idNumber.length !== 11 || isNaN(idNumber)) {
      alert("کد ملی باید ۱۱ رقم باشد.");
      return;
    }

    // User email - You might need to fetch this dynamically
    const email = "user@example.com"; // Replace with the actual email of the logged-in user

    // Prepare FormData
    const formData = new FormData();
    formData.append("email", email);
    formData.append("nationality", nationality === "ایرانی" ? "persian" : "other"); // Map to backend values
    formData.append("id_number", idNumber);

    try {
      // Send data to API
      const response = await fetchWithAuth("http://localhost:8000/account/api/profile/verifycheck/", {
        method: "POST",
        body: formData,
      });

      const data = await response

        alert("تأیید هویت با موفقیت انجام شد.");
        console.log("Success:", data);

    } catch (error) {
      alert("مشکلی در ارتباط با سرور پیش آمده است.");
      console.error("Error:", error);
    }
  });
});


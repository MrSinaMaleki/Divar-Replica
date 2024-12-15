document.addEventListener("DOMContentLoaded", function () {
  const verify_box = document.getElementById('verify-box')


  async function verify_status(){
      const response = await fetchWithAuth(`http://localhost:8000/account/api/profile/verifycheck/`);
      const data = await response;
      // console.log('veerified: ',data.is_verified)
      if (data.is_verified){
        const verificationDate = new Date(data.is_verified_date).toLocaleDateString("fa-IR");
          verify_box.innerHTML = `
            <div class="max-w-lg mx-auto mt-12 p-6 bg-gray-800 rounded-lg shadow-lg">
              <p class="text-lg text-green-400 font-semibold mb-4">حساب کاربری شما تأیید شده است.</p>
              <p class="text-sm text-gray-400">تاریخ تأیید: ${verificationDate}</p>
            </div>
          `;
      }
  }







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

    verify_status()
});


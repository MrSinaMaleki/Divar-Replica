document.addEventListener("DOMContentLoaded", async function () {
      const apiUrl = `http://localhost:8000/account/api/profile/${user_id}`;
      const loadingElement = document.getElementById("loading");
      const profileDetails = document.getElementById("profile-details");
      const profileCard = document.getElementById('profile-card')
      const profileEdit = document.getElementById('profile-edit')

      const edit_profile = document.getElementById('edit_profile')
        edit_profile.addEventListener('click',e => {
            profileCard.style.display = 'none'
            profileEdit.classList.remove("hidden");
            profileEdit.classList.add("shadow");
            profileEdit.style.display = 'flex';
            profileEdit.classList.add("shadow-white");
            console.log(profileEdit)


        })

      try {
        // Fetch the user data from the API
        const response = await fetchWithAuth(apiUrl, {
          method: "GET",
        });

        const data = await response

        // Populate the profile data
        document.getElementById("first_name").textContent = data.first_name || "N/A";
        document.getElementById("last_name").textContent = data.last_name || "N/A";
        document.getElementById("email").textContent = data.email || "N/A";

        // Show the profile details and hide the loading state
        loadingElement.classList.add("hidden");
        profileDetails.classList.remove("hidden");
      } catch (error) {
        console.error("Error loading profile:", error);
        loadingElement.innerHTML = `<p class="text-red-500">Failed to load profile information.</p>`;
      }
    });
const profileForm = document.getElementById("profile-form");
profileForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent form from refreshing the page

        const formData = {
          first_name: document.getElementById("first_name_inp").value,
          last_name: document.getElementById("last_name_inp").value,
          email: user_email,
        };
    // console.log(formData.first_name)
    // console.log(formData.last_name)
    // console.log(formData.email)

        try {
          const response = await fetchWithAuth(`http://localhost:8000/account/api/profile/${user_id}`, {
            method: "PUT", // Use PUT for full update or PATCH for partial update
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
          });


          const updatedData = await response
          alert("Profile updated successfully!");
          console.log("Updated Data:", updatedData);
        } catch (error) {
          console.error("Error updating profile:", error);
          alert("Failed to update profile. Please try again.");
        }
      });

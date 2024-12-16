async function getLikedPosts() {
  try {
    const res = await fetchWithAuth("http://localhost:8000/account/api/profile/my_posts", { method: "GET" });
    const data = await res;

    // Select the container where cards will be rendered
    const container = document.getElementById("cards-container");

    // Clear the container before rendering
    container.innerHTML = "";

    // Loop through the fetched data and create cards
    data.forEach((item) => {
      console.log(item)
      // Use the first image if available; otherwise, fallback to a placeholder
      const coverImage = item.images.length > 0 ? item.images[0].image : "https://via.placeholder.com/120";

      // Create the card HTML
    const cardHTML = `
          <div class="bg-gray-800 border border-gray-700 rounded-lg shadow-lg p-6 flex flex-col space-y-4 hover:bg-gray-700 transition cursor-pointer">
            <!-- Image -->
            <img src="${coverImage}" alt="${item.title}" class="w-full h-48 rounded-lg object-cover" />
        
            <!-- Content -->
            <div class="flex-1">
              <!-- Title -->
              <h3 class="text-lg font-bold mb-2">${item.title}</h3>
        
              <!-- Description -->
              <p class="text-sm text-gray-300 mb-4">${item.description}</p>
        
              <!-- Status -->
              <p class="text-xs font-medium text-gray-400">وضعیت: <span class="text-blue-400">${item.status}</span></p>
            </div>
        
            <!-- Buttons -->
            <div class="flex justify-between items-center">
              <!-- Edit Button -->
              <button 
                class="flex items-center text-gray-300 hover:text-gray-100 text-sm"
                onclick="editPost(${item.id})"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 ml-1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 3.487l3.651 3.65-9.193 9.193H7.67v-3.65l9.192-9.193z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.855 6.44l-3.652-3.652M7.67 15.192v3.651h3.651" />
                </svg>
                ویرایش
              </button>
        
              <!-- Ladder Button -->
              <button 
                class="flex items-center text-gray-300 hover:text-gray-100 text-sm"
                onclick="ladderPost(${item.id})"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 ml-1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 12h18M9 6h6M9 18h6" />
                </svg>
                نردبان
              </button>
        
              <!-- Delete Button -->
              <button 
                class="flex items-center text-red-500 hover:text-red-700 text-sm"
                onclick="deletePost(${item.id})"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 ml-1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 13h6M12 10v6M4 7h16M10 7v1.5M14 7v1.5M4 7l1 12a2 2 0 002 2h10a2 2 0 002-2l1-12" />
                </svg>
                حذف آگهی
              </button>
            </div>
          </div>
        `;



      // Append the card to the container
      container.insertAdjacentHTML("beforeend", cardHTML);
    });
  } catch (error) {
    console.error("Error fetching liked posts:", error);
  }
}

// Call the function to fetch and render posts
getLikedPosts();

function showpostinfo(postId) {
  location.replace(`http://localhost:8000/post/post_detail/${postId}`);
}

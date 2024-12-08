document.addEventListener("DOMContentLoaded", () => {
  fetchMainCategories(); // Fetch main categories on page load
    fetchProvinces();
});

// Fetch Main Categories
function fetchMainCategories() {
  fetch("http://localhost:8000/category/main_categories/")
    .then(response => response.json())
    .then(data => {
      const mainCategorySelect = document.getElementById("main-category");
      data.forEach(category => {
        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.title;
        mainCategorySelect.appendChild(option);
      });
    })
    .catch(error => console.error("Error fetching main categories:", error));
}

// Fetch Subcategories based on selected Main Category
function fetchSubCategories(mainCategoryId) {
  const subCategorySelect = document.getElementById("sub-category");
  const subSubCategorySelect = document.getElementById("sub-subcategory");
  const selectCategoryBtn = document.getElementById("select-category-btn");

  subCategorySelect.innerHTML = '<option value="">انتخاب زیرمجموعه...</option>'; // Reset subcategory options
  subCategorySelect.disabled = true;
  subSubCategorySelect.disabled = true;
  selectCategoryBtn.disabled = true;

  if (!mainCategoryId) return;

  fetch(`http://localhost:8000/category/${mainCategoryId}/children/`)
    .then(response => response.json())
    .then(data => {
      data.forEach(subcategory => {
        const option = document.createElement("option");
        option.value = subcategory.id;
        option.textContent = subcategory.title;
        subCategorySelect.appendChild(option);
      });

      subCategorySelect.disabled = data.length === 0;
    })
    .catch(error => console.error("Error fetching subcategories:", error));
}

// Fetch Sub-Subcategories based on selected Subcategory
function fetchSubSubCategories(subCategoryId) {
  const subSubCategorySelect = document.getElementById("sub-subcategory");
  const selectCategoryBtn = document.getElementById("select-category-btn");

  subSubCategorySelect.innerHTML = '<option value="">انتخاب زیر-زیرمجموعه...</option>'; // Reset sub-subcategory options
  subSubCategorySelect.disabled = true;
  selectCategoryBtn.disabled = true;

  if (!subCategoryId) return;

  fetch(`http://localhost:8000/category/${subCategoryId}/children/`)
    .then(response => response.json())
    .then(data => {
      data.forEach(subSubcategory => {
        const option = document.createElement("option");
        option.value = subSubcategory.id;
        option.textContent = subSubcategory.title;
        subSubCategorySelect.appendChild(option);
      });

      subSubCategorySelect.disabled = data.length === 0;
    })
    .catch(error => console.error("Error fetching sub-subcategories:", error));
}

// Log category selection and enable button if all categories are selected
function logCategorySelection(subSubCategoryId) {
  const mainCategoryId = document.getElementById("main-category").value;
  const subCategoryId = document.getElementById("sub-category").value;
  const subSubCategorySelect = document.getElementById("sub-subcategory");
  const selectCategoryBtn = document.getElementById("select-category-btn");

  // If all category selections have been made, enable the button
  if (mainCategoryId && subCategoryId && subSubCategoryId) {
    selectCategoryBtn.disabled = false;
  } else {
    selectCategoryBtn.disabled = true;
  }

  console.log("Selected categories:", { mainCategoryId, subCategoryId, subSubCategoryId });
}

// Show the next form
function showLocationSelection() {
  const categorySelection = document.getElementById("category-container");
  const locationSelection = document.getElementById("location-selection");

  categorySelection.classList.add("hidden");
  locationSelection.classList.remove("hidden");
}

function fetchProvinces() {
  fetch("http://localhost:8000/location/")
    .then(response => response.json())
    .then(data => {
      const provinces = data.filter(location => location.type === 1);
      const provinceSelect = document.getElementById("province");

      provinces.forEach(province => {
        const option = document.createElement("option");
        option.value = province.id;
        option.textContent = province.title;
        provinceSelect.appendChild(option);
      });
    })
    .catch(error => console.error("Error fetching provinces:", error));
}

// Fetch Cities based on the selected Province
function fetchCities(provinceId) {
  const areaSelect = document.getElementById("area");
  const continueBtn = document.getElementById("continue-btn");

  areaSelect.innerHTML = '<option value="">انتخاب محله...</option>'; // Reset options
  areaSelect.disabled = true;
  continueBtn.disabled = true;

  if (!provinceId) return;

  fetch("http://localhost:8000/location/")
    .then(response => response.json())
    .then(data => {
      const areas = data.filter(location => location.type === 2 && location.parent === parseInt(provinceId));

      areas.forEach(area => {
        const option = document.createElement("option");
        option.value = area.id;
        option.textContent = area.title;
        areaSelect.appendChild(option);
      });

      areaSelect.disabled = areas.length === 0;
      continueBtn.disabled = areas.length === 0;
    })
    .catch(error => console.error("Error fetching areas:", error));
}

// Proceed to post form after selecting location
function proceedToPostForm() {
  const provinceId = document.getElementById("province").value;
  const areaId = document.getElementById("area").value;

  if (provinceId && areaId) {
    console.log("Proceeding with the following selection:");
    console.log("Province ID:", provinceId);
    console.log("Area ID:", areaId);

  } else {
    console.log("Please select both province and area.");
  }
}


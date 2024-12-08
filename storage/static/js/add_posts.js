document.addEventListener("DOMContentLoaded", () => {
  fetchMainCategories(); // Fetch main categories on page load
  fetchProvinces();
});


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
      const provinces = data.filter(location => location.type === 1);  // Assuming type 1 is for provinces
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

  // Check if the area select element exists
  if (!areaSelect) {
    console.error('Area select element not found');
    return;
  }

  // Reset the area options and disable the select
  areaSelect.innerHTML = '<option value="">انتخاب محله...</option>'; // Reset options
  areaSelect.disabled = true;
  continueBtn.disabled = true;

  if (!provinceId) return;

  fetch("http://localhost:8000/location/")
    .then(response => response.json())
    .then(data => {
      const areas = data.filter(location => location.type === 2 && location.parent === parseInt(provinceId));

      // Ensure that areas are found before adding options
      if (areas.length === 0) {
        areaSelect.disabled = true;
        continueBtn.disabled = true;
        return;
      }

      // Add the area options
      areas.forEach(area => {
        const option = document.createElement("option");
        option.value = area.id;
        option.textContent = area.title;
        areaSelect.appendChild(option);
      });

      // Re-enable the select dropdown after populating
      areaSelect.disabled = false;
      continueBtn.disabled = false;
    })
    .catch(error => console.error("Error fetching areas:", error));
}

// Proceed to post form after selecting location
function proceedToPostForm() {
  const provinceId = document.getElementById("province").value;
  const areaId = document.getElementById("area").value;
  const subSubCategoryId = document.getElementById("sub-subcategory").value; // Get selected sub-sub-category ID

  if (provinceId && areaId && subSubCategoryId) {
    console.log("Proceeding to additional fields...");

    // Fetch additional fields for the selected sub-sub-category
    fetch(`http://localhost:8000/post/post-fields/${subSubCategoryId}/`)
      .then(response => response.json())
      .then(data => {
        renderPostFieldsBelowLocation(data.category_fields);
        renderPostFields(data.post_fields);
      })
      .catch(error => console.error("Error fetching post fields:", error));
  } else {
    console.log("Please select province, area, and category.");
  }
}

// Render dynamically generated form fields below the location form
function renderPostFieldsBelowLocation(fields) {
  const province = document.getElementById("province");
  const area = document.getElementById("area");
  const continue_btn = document.getElementById("continue-btn");
  province.disabled = true;
  area.disabled = true;
  continue_btn.style.display = 'none'

  const locationSelection = document.getElementById("location-selection");

  // Check if the dynamic fields section already exists; if so, remove it first
  let dynamicFieldsContainer = document.getElementById("dynamic-fields-container");
  if (dynamicFieldsContainer) {
    dynamicFieldsContainer.remove();
  }

  // Create a container for dynamic fields
  dynamicFieldsContainer = document.createElement("div");
  dynamicFieldsContainer.id = "dynamic-fields-container";
  dynamicFieldsContainer.classList.add("w-full", "bg-gray-900", "text-white", "p-6", "rounded-lg", "mt-6");

  const fieldsTitle = document.createElement("h2");
  fieldsTitle.textContent = "اطلاعات اضافی";
  fieldsTitle.classList.add("text-xl", "font-semibold", "mb-4");
  dynamicFieldsContainer.appendChild(fieldsTitle);

  // Generate the fields based on API response
  fields.forEach(field => {
    const fieldWrapper = document.createElement("div");
    fieldWrapper.classList.add("mb-4", "w-full");

    const label = document.createElement("label");
    label.textContent = field.name + (field.is_optional ? " (اختیاری)" : "");
    label.classList.add("block", "text-lg", "mb-2");

    let input;

    // Handle field types
    if (field.f_type === "drop-down") {
      input = document.createElement("select");
      input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");

      // Add dropdown options
      const options = field.drop_down_menu_options.split(" - ");
      options.forEach(optionText => {
        const option = document.createElement("option");
        option.value = optionText;
        option.textContent = optionText;
        input.appendChild(option);
      });
    } else {
      input = document.createElement("input");
      input.type = field.f_type === "int" ? "number" : "text";
      input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");
    }

    if (!field.is_optional) {
      input.required = true;
    }

    fieldWrapper.appendChild(label);
    fieldWrapper.appendChild(input);
    dynamicFieldsContainer.appendChild(fieldWrapper);
  });

  // Add the dynamic form container to the location form
  locationSelection.appendChild(dynamicFieldsContainer);
}

function renderPostFields(fields) {
  const locationSelection = document.getElementById("location-selection");

  // Create a container for dynamic fields (we will append this instead of replacing it)
  let dynamicFieldsContainer = document.createElement("div");
  dynamicFieldsContainer.id = "dynamic-fields-container";
  dynamicFieldsContainer.classList.add("w-full", "bg-gray-900", "text-white", "p-6", "rounded-lg", "mt-6");

  const fieldsTitle = document.createElement("h2");
  fieldsTitle.textContent = "اطلاعات پست";
  fieldsTitle.classList.add("text-xl", "font-semibold", "mb-4");
  dynamicFieldsContainer.appendChild(fieldsTitle);

  // Generate the fields based on API response for "title", "description", "laddered", and "images"
  fields.forEach(field => {
    if (field === "title" || field === "description" || field === "laddered" || field === "images") {
      const fieldWrapper = document.createElement("div");
      fieldWrapper.classList.add("mb-4", "w-full");

      const label = document.createElement("label");
      label.textContent = field === "title" ? "عنوان" :
                         field === "description" ? "توضیحات" :
                         field === "laddered" ? "آیا نردبانی است؟" :
                         "تصاویر";
      label.classList.add("block", "text-lg", "mb-2");

      let input;

      // Create the appropriate input based on the field
      if (field === "title") {
        input = document.createElement("input");
        input.type = "text";
        input.placeholder = "عنوان پست";
        input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");
      } else if (field === "description") {
        input = document.createElement("textarea");
        input.placeholder = "توضیحات پست";
        input.rows = 4;
        input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");
      } else if (field === "laddered") {
        input = document.createElement("input");
        input.type = "checkbox";
        input.classList.add("form-checkbox", "w-5", "h-5");
      } else if (field === "images") {
        input = document.createElement("input");
        input.type = "file";
        input.multiple = true;  // Allow multiple files
        input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");
        input.accept = "image/*";  // Accept only images
      }

      fieldWrapper.appendChild(label);
      fieldWrapper.appendChild(input);
      dynamicFieldsContainer.appendChild(fieldWrapper);
    }
  });

  // Append the dynamic form container to the location form, instead of replacing the content
  locationSelection.appendChild(dynamicFieldsContainer);
}




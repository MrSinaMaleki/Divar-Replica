document.addEventListener("DOMContentLoaded", () => {
  fetchMainCategories(); // Fetch main categories on page load
  fetchProvinces();
});

// Get the image input and preview elements
const imageInput = document.getElementById("ad-images");
const imagePreview = document.getElementById("image-preview");

let uploadedImages = []; // This will store the uploaded files

// Function to handle image input change
function handleImageUpload(event) {
  // Clear previous previews
  imagePreview.innerHTML = "";

  // Get the files selected by the user
  const files = Array.from(event.target.files);

  // Limit to a maximum of 10 images
  if (files.length + uploadedImages.length > 10) {
    alert("تعداد عکس‌های انتخاب شده نباید بیشتر از ۱۰ باشد.");
    return;
  }

  // Add new files to the uploaded images array
  uploadedImages = [...uploadedImages, ...files];

  // Display image previews
  files.forEach(file => {
    const reader = new FileReader();

    reader.onload = (e) => {
      const imgWrapper = document.createElement("div");
      imgWrapper.classList.add("relative", "w-full", "h-28", "overflow-hidden", "rounded", "bg-gray-700");

      const img = document.createElement("img");
      img.src = e.target.result;
      img.classList.add("w-full", "h-full", "object-cover");

      const removeButton = document.createElement("button");
      removeButton.textContent = "×";
      removeButton.classList.add(
        "absolute", "top-1", "right-1", "bg-red-500", "text-white",
        "text-xs", "p-1", "rounded-full", "hover:bg-red-700", "transition"
      );

      removeButton.addEventListener("click", () => removeImage(file, imgWrapper));

      imgWrapper.appendChild(img);
      imgWrapper.appendChild(removeButton);
      imagePreview.appendChild(imgWrapper);
    };

    reader.readAsDataURL(file);
  });
}

// Function to remove an image from the uploaded list
function removeImage(file, imgWrapper) {
  // Remove the file from the uploaded images array
  uploadedImages = uploadedImages.filter(uploadedFile => uploadedFile !== file);

  // Remove the image wrapper from the DOM
  imgWrapper.remove();
}

// Attach the event listener to the image input
imageInput.addEventListener("change", handleImageUpload);

// Optional: If you're using drag-and-drop functionality, you can add this listener too
imagePreview.addEventListener("dragover", (e) => e.preventDefault());
imagePreview.addEventListener("drop", (e) => {
  e.preventDefault();
  const files = Array.from(e.dataTransfer.files);
  imageInput.files = e.dataTransfer.files; // Update the input field files (required for handling)
  handleImageUpload({ target: { files } }); // Simulate the input change event
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
      const provinceSelect = document.getElementById("provinces");
        console.log("province inp: ", provinceSelect)

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
async function proceedToPostForm() {
  const provinceId = document.getElementById("provinces").value;
  const areaId = document.getElementById("area").value;
  const subSubCategoryId = document.getElementById("sub-subcategory").value; // Get selected sub-sub-category ID

  if (provinceId && areaId && subSubCategoryId) {
    console.log("Proceeding to additional fields...");

    try {
      // Fetch additional fields for the selected sub-sub-category
      const data = await fetchWithAuth(`http://localhost:8000/post/post-fields/${subSubCategoryId}/`);

      // Check if category_fields and post_fields are defined and arrays
      if (Array.isArray(data.category_fields)) {
        renderPostFieldsBelowLocation(data.category_fields);
      } else {
        console.error("category_fields is not an array:", data.category_fields);
      }

      if (Array.isArray(data.post_fields)) {
        renderPostFields(data.post_fields);
      } else {
        console.error("post_fields is not an array:", data.post_fields);
      }
    } catch (error) {
      console.error("Error fetching post fields:", error);
    }
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
  continue_btn.style.display = 'none';

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

  fields_list = fields

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
    input.id = field.id

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
        input.name = 'title'
      } else if (field === "description") {
        input = document.createElement("textarea");
        input.placeholder = "توضیحات پست";
        input.rows = 4;
        input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");
        input.name = 'description'
      } else if (field === "laddered") {
        input = document.createElement("input");
        input.type = "checkbox";
        input.classList.add("form-checkbox", "w-5", "h-5");
        input.name = 'laddered'
      } else if (field === "images") {
        input = document.createElement("span");
        // input.type = "file";
        // input.multiple = true;  // Allow multiple files
        // input.classList.add("w-full", "p-2", "bg-gray-800", "border", "border-gray-700", "rounded", "focus:outline-none", "focus:ring", "focus:ring-indigo-500");
        // input.accept = "image/*";  // Accept only images
        const images_selector = document.getElementById('image-upload-section')
        images_selector.style.display = 'flex'



      }

      fieldWrapper.appendChild(label);
      fieldWrapper.appendChild(input);
      dynamicFieldsContainer.appendChild(fieldWrapper);
    }
  });

          // Add Submit Button
      const submitButton = document.createElement("button");
      submitButton.textContent = "ارسال آگهی";
      submitButton.id = "submit-post-btn";
      submitButton.classList.add(
        "w-full",
        "bg-green-600",
        "hover:bg-green-700",
        "text-white",
        "py-2",
        "px-4",
        "rounded",
        "mt-4"
      );
      submitButton.onclick = submitPost; // Attach the submit function

  // Append the dynamic form container to the location form, instead of replacing the content
  locationSelection.appendChild(dynamicFieldsContainer);
  dynamicFieldsContainer.appendChild(submitButton);
}

// console.log(user_id)

async function sendPostData(payload) {
    const url = "http://localhost:8000/post/api/create_post/"; // Replace with your API endpoint
    const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    try {
        const response = await fetchWithAuth(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(payload),
        });

        Swal.fire({
          title: 'ثبت آگهی موفقیت امیز بود',
          text: 'آگهی مورد نظر اضافه شد',
          icon: 'success',
          confirmButtonText: 'اوکی',
        })
        // Handle the successful response
        console.log("Post created successfully:", response);


       // location.replace('http://localhost:8000/account/login/')
        uploadedImagesStep()
        const uploadImagesForm = document.getElementById("uploadImagesForm");
        const submitImagebtn = document.getElementById("submitImagebtn");

        uploadImagesForm.addEventListener("submit", (event) => {submitImages(event, response.post_id);
        });

    } catch (error) {
        console.error("Error creating post:", error);

        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: `Failed to create post: ${error.message}`,
        });
    }
}


async function submitPost(event) {
  const areaSelect = document.getElementById("area");
  const sub_subcategory = document.getElementById("sub-subcategory");
  const titleInput = document.querySelector('input[name="title"]');
  const description = document.querySelector('textarea[name="description"]');
  const laddered = document.querySelector('input[name="laddered"]');
  const all_fields = []
  const all_images = []

  fields_list.forEach(inp =>{
    all_fields.push({"field_id": inp.id, "value":document.getElementById(inp.id).value})
  })

  let index = 0;
  uploadedImages.forEach(imgg =>{
    if (index > 0){
      var is_cover = false
    }else{
      is_cover = true
    }

   all_images.push(
       {
      "image": imageInput.files[index],
      "caption": "",
      "is_cover": is_cover,
      },)
      index += 1
  })
  console.log("all_images: ",all_images)

  payload ={
    "title": titleInput.value,
    "description": description.value,
    "laddered": laddered.checked,
    "category_id": sub_subcategory.value,
    "user_id": user_id,
    "location_id": areaSelect.value,
    "video": null,
    "fields": all_fields
  }
  sendPostData(payload)

}


function uploadedImagesStep() {
  const postInfoForm = document.getElementById("location-selection");
  postInfoForm.classList.add("hidden");


  const uploadImagesForm = document.getElementById("uploadImagesForm")
  uploadImagesForm.classList.remove("hidden")

}

async function submitImages(event ,post_id){
    event.preventDefault()
  const formData = new FormData();
      const files = document.getElementById("ad-images").files;

      if (files.length === 0) {
          alert("Please select at least one image.");
          return;
      }

      // Append each file to the FormData
        Array.from(files).forEach((file, index) => {
            formData.append('images', file);  // Image field
            formData.append('caption', "");  // Empty caption or a specific one
            formData.append('is_cover', index === 0 ? 'true' : 'false');  // First image is cover
        });


      // Add the post ID to the form data
      formData.append('post_id', post_id);
        console.log("post_id", post_id)

      try {
          // Make the POST request to upload images
          const response = await fetchWithAuth("http://localhost:8000/post/api/add_image/", {
              method: "POST",
              body: formData,
          });

          if (response.message === "Images were added successfully.") {
            Swal.fire({
              title: 'ثبت عکس های آگهی موفقیت امیز بود',
              text: '',
              icon: 'success',
              confirmButtonText: 'ادامه',
            })
              setTimeout(() => location.replace('http://localhost:8000/'), 3000)

          } else {
              console.error("Error uploading images:", response);
              alert("Failed to upload images. Please try again.");
          }
      } catch (error) {
          console.error("Failed to upload images:", error);
          alert("An error occurred while uploading images.");
      }

}
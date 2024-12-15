      let locationCard = document.querySelector("#location-card");
      let provinceList = document.querySelector("#province");
      let provinceContainer = document.querySelector("#province-container");
      let openLocationCardBtn = document.querySelector("#open-location-card");
      let cancelBtn = document.querySelector("#cancel");
      let removeAllCitiesBtn = document.querySelector("#remove-all-cities");
      let removeCityBtn = document.querySelector("#remove-city");
      let choosingLocationSentence = document.querySelector(
        "#choosing-location-sentence"
      );
      //
      //
      //
      //
      // search box state
      let searchBox = document.querySelector("#search-box");
      //
      //Uncaught SyntaxError: Identifier 'set' has already been declared (at headerlogic.js:1:1)
      //
      //
      //
      //
      //
      // my divar state
      let myDivarBtn = document.querySelector("#my-divar-state");
      //
      //
      //
      //
      // support state
      let supportBtn = document.querySelector("#support-state");
      let set;
      let flag = true;
      addEventListener("DOMContentLoaded", () => {
        let result = provinces();
        result.catch((error) => console.log(error));
      });
       addEventListener("load", () => adjustCards(provinceContainer, 360));
      addEventListener("resize", () => adjustCards(provinceContainer, 360));
    cancelBtn.addEventListener("click", () => {
        locationCard.parentNode.style.display = "none";
        provinces();
      });
  openLocationCardBtn.addEventListener("click", () => {
        locationCard.parentNode.style.display = "flex";
      });
      removeCityBtn.addEventListener("click", () => {
        removeCityBtn.parentNode.parentNode.style.display = "none";
        choosingLocationSentence.style.display = "block";
      });
  // searchBox.addEventListener("click", () => {
      //   searchBox.style.display = "none";
      //   searchBox.firstElementChild.nextElementSibling.nextElementSibling.classList.remove(
      //     "hidden"
      //   );
      // });
      // document.body.addEventListener("click", (e) => {
      //   console.log(searchBox.firstElementChild);
      //   console.log(e.target);

      //   if (e.target != searchBox.firstElementChild) {
      //     searchBox.style.display = "flex";
      //     searchBox.firstElementChild.nextElementSibling.nextElementSibling.classList.remove(
      //       "hidden"
      //     );
      //   }
      // });
      supportBtn.addEventListener("click", () => {
        supportBtn.lastElementChild.classList.toggle("hidden");
      });
      myDivarBtn.addEventListener("click", () => {
          // console.log(is_loggedIn)
        if (is_loggedIn === "True") {
          myDivarBtn.firstElementChild.nextElementSibling.classList.toggle(
            "hidden"
          );
        } else {

          myDivarBtn.lastElementChild.classList.toggle("hidden");
        }
      });
 function adjustCards(frm, maxValue) {
        let vh = innerHeight;
        frm.style.maxHeight = vh - maxValue + "px";
      }
 async function provinces() {
        let response = await fetch("http://127.0.0.1:8000/location/");
        let provinces = await response.json();

        // نمایش لیست استان‌ها
        function renderProvinces() {
          provinceList.innerHTML = ""; // پاک‌کردن محتوا

          provinces
            .filter((item) => item.type === 1)
            .forEach((province) => {
              const li = document.createElement("li");
              li.innerHTML =
                province.title +
                `  <svg class="w-4 h-4 cursor-pointer text-zinc-500 rotate-90">
        <use href="#chevron-down"></use>
       </svg>`;
              li.classList.add("order");
              li.addEventListener("click", () =>
                renderCities(province.id, province.title)
              );
              provinceList.appendChild(li);
            });
        }

        // نمایش شهرهای استان
        function renderCities(provinceId, provinceName) {
          provinceList.innerHTML = ""; // پاک‌کردن محتوا

          // افزودن دکمه "همه شهرها" و "شهرهای استان"
          const allCitiesButton = document.createElement("li");
          allCitiesButton.innerHTML =
            `<svg class="w-4 h-4 cursor-pointer text-zinc-500">
        <use href="#arrow-right"></use>
        </svg>` + "همه‌ی شهرها";
          allCitiesButton.classList.add("city-order");
          allCitiesButton.addEventListener("click", renderProvinces);
          provinceList.appendChild(allCitiesButton);

          const provinceCitiesHeader = document.createElement("li");
          provinceCitiesHeader.innerHTML =
            `شهرهای استان ${provinceName}` +
            `  <span
        class="flex justify-center items-center w-8 h-8 rounded-full transition-all"
       >
          <input
            class="w-4 h-4 cursor-pointer accent-light_redwall"
            type="checkbox"
          />
       </span>`;
          provinceCitiesHeader.classList.add("order");
          provinceList.appendChild(provinceCitiesHeader);
          // افزودن لیست شهرها
          const ul = document.createElement("ul");
          provinces
            .filter((item) => item.type === 2 && item.parent === provinceId)
            .forEach((city) => {
              const li = document.createElement("li");
              li.innerHTML =
                city.title +
                `<span
        class="flex justify-center items-center w-8 h-8 rounded-full transition-all"
       >
          <input
            class="w-4 h-4 cursor-pointer accent-light_redwall"
            type="checkbox"
          />
       </span>`;
              li.classList.add("order");
              provinceList.appendChild(li);
            });
        }

        // شروع با لیست استان‌ها
        renderProvinces();
      }


const logOutBtn = document.getElementById('logOutBtn')
      logOutBtn.addEventListener('click', event=> {

        location.reload()


      })













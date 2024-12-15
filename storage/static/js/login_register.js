let loginclosebtn = document.querySelector(".close");
let verifyclosebtn = document.querySelector(".close-verify");
let emailInput = document.querySelector(".mail");
let acceptbtn = document.querySelector(".accept");
let responseMailValidate = document.querySelector(".responseMail");
let frmContainerLogin = document.querySelector(".formcontainer-login ");
let frmContainerverify = document.querySelector(".formcontainer-verify ");
let loginSection = document.querySelector(".login-section");
let verifySection = document.querySelector(".verify-section");
let timer = document.querySelector(".timer");
let requestBtn = document.querySelector(".request-btn");
let changeAddr = document.querySelector(".change-addr");
let codeInp = document.querySelector("#codeInp");
let enterbtn = document.querySelector("#enterbtn")
const fullForm = document.getElementById('fullform')
if (is_loggedIn === 'True'){
  console.log(is_loggedIn)
  // fullForm.style.display = 'none'
}


loginclosebtn.addEventListener("click", logincloseFrm);
verifyclosebtn.addEventListener("click", verifycloseFrm);

acceptbtn.addEventListener("click", () => {
  let email = emailInput.value;
  if (emailValidation(email)) {
    loginSection.style.display = "none";
    verifySection.style.display = "flex";
    timerCounter();
    sendLoginCode(email);
  } else {
    responseMailValidate.innerHTML = "لطفا ایمیل خود را به درستی وارد کنید";
    emailInput.style.borderColor = "red";
    console.log(email)
  }
});
addEventListener("load", adjustfrm);
addEventListener("resize", adjustfrm);

requestBtn.addEventListener("click", () => {
  timer.parentElement.style.display = "flex";
  requestBtn.style.display = "none";
  timerCounter();
});

changeAddr.addEventListener("click", () => {
  loginSection.style.display = "flex";
  verifySection.style.display = "none";
});

enterbtn.addEventListener("click", ()=>{
  verifyCode(emailInput.value, codeInp.value)
  verifycloseFrm()
  // location.reload()

})

function logincloseFrm() {
  loginSection.style.background = "none";
  loginSection.style.display = "none";
}
function verifycloseFrm() {
  verifySection.style.background = "none";
  verifySection.style.display = "none";
}
function emailValidation(email) {
  const ke =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return ke.test(String(email));
}
function adjustfrm() {
  let vh = innerHeight;
  frmContainerLogin.style.maxHeight = innerHeight - 144 + "px";
  frmContainerverify.style.maxHeight = innerHeight - 144 + "px";
}
function timerCounter() {
  timer.innerHTML = "30";
  let time = Number(timer.innerHTML);
  if (set) clearInterval(set);
  set = setInterval(() => {
    if (time != 0) {
      time = time - 1;
      timer.innerHTML = time;
    } else {
      clearInterval(set);
      timer.parentElement.style.display = "none";
      requestBtn.style.display = "inline-flex";
    }
  }, 1000);
}

async function sendLoginCode(email) {
  const apiUrl = "http://localhost:8000/account/loginAPI/"; // Replace with your actual API endpoint
  const payload = { email };

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return { success: false, message: errorData.Message || "Request failed" };
    }

    const responseData = await response.json();
    console.log("Success:", responseData);
    return { success: true, data: responseData };
  } catch (error) {
    console.error("Error while sending request:", error);
    return { success: false, message: "An error occurred while sending the request" };
  }
}

async function verifyCode(email, code) {
  const apiUrl = "http://localhost:8000/account/verifyAPI/"; // Replace with your actual API endpoint
  const payload = { email, code };

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      credentials: "include", // Ensures cookies (for tokens) are handled
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData);
      return { success: false, message: errorData.Message || "Request failed" };
    }

    const responseData = await response.json();
    console.log("Verification success:", responseData);

    // Assuming the response contains the tokens in the following format
    const { access_token, refresh_token } = responseData; // Adjust this to match your actual response structure

    // Save tokens in localStorage (or in cookies, if preferred)
    if (access_token) {
      localStorage.setItem("access_token", access_token);  // Save access token in localStorage
    }
    if (refresh_token) {
      localStorage.setItem("refresh_token", refresh_token);  // Save refresh token in localStorage
    }

    return { success: true, data: responseData };

  } catch (error) {
    console.error("Error while verifying code:", error);
    return { success: false, message: "An error occurred while verifying the code" };
  }
}
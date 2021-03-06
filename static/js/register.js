import {getFormData} from "./util/util.js";
import {sendRequest} from "./request/request_handler.js";
import {REGISTER_ENDPOINT} from "./endpoints.js";
import {setCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', onRegister)

function onRegister(e) {
    e.preventDefault();

    const currentTarget = e.currentTarget;

    const payload = getFormData(currentTarget);
    const errorTextElement = document.getElementById('error-text');
    errorTextElement.innerHTML = '';

    if (payload.password !== payload.passconfirmation) {
        errorTextElement.innerHTML = "Passwords dont match";
        return;
    }

    const request = sendRequest(REGISTER_ENDPOINT, "POST", payload);

    request.onreadystatechange = (e) => {
        if (request.readyState === XMLHttpRequest.DONE) {
            const status = request.status;
            const response = JSON.parse(request.response);

            if (status === 200) {
                setCookie(USER_AUTH_COOKIE, JSON.parse(request.responseText).token);
                window.location = "/topics"
            } else {
                errorTextElement.innerHTML = response.message;
            }
        }
    }
}

const previewImage = document.getElementById("preview-image");
const previewImageInput = document.getElementById("image-url-field");

const previewButton = document.getElementById("preview-button");
previewButton.addEventListener("click", function (e) {
    e.preventDefault();

    let imageUrl = previewImageInput.value;

    if (imageUrl === '') {
        imageUrl = 'https://i.postimg.cc/RF11Kn7j/default.png';
    }

    previewImage.innerHTML = '<img src="' + imageUrl + '" alt="Image" id="user-picture">';
});
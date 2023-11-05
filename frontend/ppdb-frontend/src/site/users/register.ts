import { UserCreateFromJSON } from "@api/index.js";
import { users_api } from "@this/api.js";
import { get_form_data } from "@this/form.js";

function handler(event: Event) {
    event.preventDefault();
    event.stopPropagation();

    const form = event.target as HTMLFormElement;

    const form_data = get_form_data(form);

    const password_valid =
        form_data["password"] === form_data["repeat-password"];

    form.classList.add("was-validated");

    if (!password_valid) {
        const repeat_password_input = document.getElementById(
            "repeat-password"
        ) as HTMLInputElement;

        repeat_password_input.classList.add("invalid");
        repeat_password_input.setCustomValidity("x");
        return;
    }

    users_api
        .createApiUsersPost({
            userCreate: UserCreateFromJSON(form_data),
        })
        .catch((error) => {
            alert(error.response.statusText);
        })
        .then(() => {
            form.classList.remove("was-validated");
            form.reset();
        });
}

document.getElementById("form").addEventListener("submit", handler);

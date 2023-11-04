import { PersonCreateFromJSON } from "@api/index.js";
import { persons_api } from "@this/api.js";
import { get_form_data } from "@this/form.js";

function handler(event: Event) {
    event.preventDefault();

    const form = event.target as HTMLFormElement;

    const person_create_json = get_form_data(form);

    const person_create = PersonCreateFromJSON(person_create_json);

    persons_api
        .createApiPersonsPost({ personCreate: person_create })
        .then((person) => {
            form.reset();
        });
}

document.getElementById("form").addEventListener("submit", handler);

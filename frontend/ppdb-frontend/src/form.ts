export function get_form_data(form: HTMLFormElement): object {
    let json = {};

    for (const element of form.elements) {
        if (element instanceof HTMLInputElement && element.value !== "") {
            json[element.id] = element.value;
        }
    }

    return json;
}

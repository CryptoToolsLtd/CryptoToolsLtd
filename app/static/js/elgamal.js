function changeInputType() {
    const inputField = document.getElementById("message");
    const selectedType = document.getElementById("input-type-selector").value;

    if (selectedType === "number") {
        inputField.value = "";
        inputField.placeholder = "Enter number";
    } else if (selectedType === "text") {
        inputField.placeholder = "Enter text";
        inputField.value = "";
    }
}
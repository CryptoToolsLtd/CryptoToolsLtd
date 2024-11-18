function changeInputType() {
    const inputField = document.getElementById("m");
    const selectedType = document.getElementById("input-type-selector").value;

    inputField.type = selectedType;

    if (selectedType === "number") {
        inputField.placeholder = "Enter number";
    } else if (selectedType === "text") {
        inputField.placeholder = "Enter text";
    }
}
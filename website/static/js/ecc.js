function showOption(OptionNumber) {
    // Hide both pages
    document.getElementById("option1").classList.add("hidden");
    document.getElementById("option2").classList.add("hidden");

    // Show the selected page
    if (OptionNumber === 1) {
        document.getElementById("option1").classList.remove("hidden");
    } else if (OptionNumber === 2) {
        document.getElementById("option2").classList.remove("hidden");
    }
}
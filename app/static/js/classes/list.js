const termsSelect = document.getElementById("class-list-terms-select");
termsSelect.addEventListener("change", function(event) {
    termId = event.currentTarget.value;
    const url = new URL(window.location);
    url.searchParams.set("term_id", termId);
    window.location = url.href;
});
document.getElementById("class-add-session-btn").addEventListener("click", function(event) {
    const form = document.getElementById("class-add-session-form");
    const createConfigObj = {
        formData: new FormData(form),
        category: "session"
    };

    AppApi.createRequest(event, createConfigObj);
});
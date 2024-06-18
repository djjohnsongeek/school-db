document.getElementById("class-add-session-btn").addEventListener("click", function(event) {
    const form = document.getElementById("class-add-session-form");
    const createConfigObj = {
        formData: new FormData(form),
        category: "session"
    };

    AppApi.createRequest(event, createConfigObj);
});

var classEdit = {
    addCreatedSession: function(response)
    {
        // create dom
            // escape values
        // add event listeners
    },
    templates: {
        session: `
        <div class="block">
            <div class="card">
                <header class="card-header is-clickable toggle" data-target="session-attendance-1,session-footer-1">
                    <p class="card-header-title">
                        Session 1: 2024-08-01
                    </p>
                    <button class="card-header-icon" aria-label="more options">
                        <span class="icon">
                            <i class="fa fa-angle-down" aria-hidden="true"></i>
                        </span>
                    </button>
                </header>
                <div class="card-content is-hidden" id="session-attendance-1">
                    <div class="columns">
                        <div class="column is-4">
                            ອາລານາ ພົນນາສາ (Alana Phonasa)
                        </div>
                        <div class="column">
                            <label class="radio">
                                <input type="radio" name="attendance1">
                                Present
                            </label>
                        </div>
                        <div class="column">
                            <label class="radio">
                                <input type="radio" name="attendance1">
                                Absent
                            </label>
                        </div>
                        <div class="column">
                            <label class="radio">
                                <input type="radio" name="attendance1">
                                Tardy
                            </label>
                        </div>
                    </div>
                    <div class="columns">
                        <div class="column is-4">
                            ເກສອນ ໄຊຍະວົງ (Kesone Sayavong)
                        </div>
                        <div class="column">
                            <label class="radio">
                                <input type="radio" name="attendance1">
                                Present
                            </label>
                        </div>
                        <div class="column">
                            <label class="radio">
                                <input type="radio" name="attendance1">
                                Absent
                            </label>
                        </div>
                        <div class="column">
                            <label class="radio">
                                <input type="radio" name="attendance1">
                                Tardy
                            </label>
                        </div>
                    </div>
                </div>
                <footer class="card-footer is-hidden" id="session-footer-1">
                    <a href="#" class="card-footer-item has-background-danger has-text-white">
                        <span class="icon-text">
                            <span class="icon">
                                <i class="fa fa-ban" aria-hidden="true"></i>
                            </span>
                            <span>Cancel</span>
                        </span>
                    </a>
                </footer>
            </div>
        </div>`
    }
}
document.getElementById("class-add-session-btn").addEventListener("click", function(event) {
    const form = document.getElementById("class-add-session-form");
    const createConfigObj = {
        formData: new FormData(form),
        category: "session",
        successCallback: classEdit.addCreatedSession
    };

    AppApi.createRequest(event, createConfigObj);
});

var classEdit = {
    addCreatedSession: function(response)
    {
        const block = Util.toHtml("<div class='block'></div")
        const card = Util.toHtml("<div class='card'></div");
        const cardHeader = Util.toHtml(`
            <header class="card-header is-clickable toggle" data-target="session-attendance-${response.session_id},session-footer-${response.session_id}">
                <p class="card-header-title">
                    ${response.session_name}: ${response.session_time}
                </p>
                <button class="card-header-icon" aria-label="more options">
                    <span class="icon">
                        <i class="fa fa-angle-down" aria-hidden="true"></i>
                    </span>
                </button>
            </header>
        `);
        const cardContentContainer = Util.toHtml(`
            <div class="card-content is-hidden" id="session-attendance-${response.session_id}">
        `);
        const cardFooter = Util.toHtml(`
            <footer class="card-footer is-hidden" id="session-footer-${response.session_id}">
                <a href="#" class="card-footer-item has-background-danger has-text-white">
                    <span class="icon-text">
                        <span class="icon">
                            <i class="fa fa-ban" aria-hidden="true"></i>
                        </span>
                        <span>Cancel</span>
                    </span>
                </a>
            </footer>
        `);

        // generate attendance html string
        attendanceForms = this.generateAttendanceForms(response.students);
        for (let element of attendanceForms)
        {
            cardContentContainer.append(element);
        }
        
        block.append(card);
        card.append(cardHeader);
        card.append(cardContentContainer);
        card.append(cardFooter);
        // TODO add event listeners

        // add to DOM
        document.getElementById(`session-attendance-${response.sessoin_id}`).append(block);
    },
    generateAttendanceForms: function(students)
    {
        let html = "";
        for (const student of students)
        {
            html += `
            <div class='columns'>
                <div class='column is-4'>
                    ${student.name}
                </div>
                <div class-'column'>
                    <label class="radio">
                        <input type="radio" name="attendance${student.id}">
                        Present
                    </label>
                </div>
                <div class='column'>
                    <label class="radio">
                        <input type="radio" name="attendance${student.id}">
                        Absent
                    </label>
                </div>
                <div class='column'>
                    <label class="radio">
                        <input type="radio" name="attendance${student.id}">
                        Tardy
                    </label>
                </div>
            </div>
            `;
        }

        const result = Util.toHtml(html);

        if (students.length > 0)
        {
            return result;
        }
        else {
            return [result];
        }
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
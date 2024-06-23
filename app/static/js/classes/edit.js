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
        // Generate HTML elements for the new session
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
                <a href="#" class="card-footer-item has-background-warning has-text-black">
                    <span class="icon-text">
                        <span class="icon">
                            <i class="fa fa-ban" aria-hidden="true"></i>
                        </span>
                        <span>Cancel</span>
                    </span>
                </a>
                <a href="#" class="card-footer-item has-background-danger has-text-white">
                    <span class="icon-text">
                        <span class="icon">
                            <i class="fa fa-trash" aria-hidden="true"></i>
                        </span>
                        <span>Delete</span>
                    </span>
                </a>
            </footer>
        `);

        attendanceForms = classEdit.generateAttendanceForms(response.students);
        for (let element of attendanceForms)
        {
            cardContentContainer.append(element);
        }
        
        // Link elements together
        block.append(card);
        card.append(cardHeader);
        card.append(cardContentContainer);
        card.append(cardFooter);

        // Add elements to the DOM
        document.getElementById("sessions-container").append(block);

        // Add event listeners
        cardHeader.addEventListener("click", (event) => App.toggleVisible(event));
        // TODO: add session specific event listeners (cancel and delete buttons)
    },
    generateAttendanceForms: function(students)
    {
        let html = "";
        if (students.length === 0)
        {
            html = `<div class="notification is-warning is-light">No Students Found</div>`;
        }
        else
        {
            for (const student of students)
            {
                html += `
                <div class='columns'>
                    <div class='column is-4'>
                        ${student.name}
                    </div>
                    <div class='column'>
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
                </div>`;
            }
        }

        // this is either an HTML element, or and HTMLCollection
        let result = Util.toHtml(html);
        if (result instanceof HTMLCollection)
        {
            result = Array.from(result);
        }

        if (Array.isArray(result))
        {
            return result;
        }
        else {
            console.log("Is not iterable");
            return [result];
        }
    },
}
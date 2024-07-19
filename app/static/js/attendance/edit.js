const attendancePage = {
    calendar: null,
    calendarElement: null,
    formData: new FormData(),
    init: function() {
        // Handle changes to the currently selected class
        document.getElementById("attendance-class-select").addEventListener("change", function() {
            attendancePage.loadAttendanceEvents();
            attendancePage.loadRosterAttendance();
        });

        attendancePage.calendarElement = document.getElementById('calendar');
        attendancePage.calendar = new FullCalendar.Calendar(attendancePage.calendarElement, {
            initialView: 'dayGridMonth',
            dateClick: attendancePage.onDateClicked,
            datesSet: attendancePage.onDatesSet
        });
        attendancePage.selectDate(attendancePage.currentDateStr());
        attendancePage.loadRosterAttendance();
        // render() calls the datesSet callback
        attendancePage.calendar.render();
    },
    onDatesSet: function(info) {
        attendancePage.loadAttendanceEvents();
    },
    onDateClicked: function(info) {
        attendancePage.selectDate(info.dateStr);
    },
    selectDate: function(dateStr) {
        attendancePage.calendar.select(dateStr);
        const dateInput = document.getElementById("selected-date-input");
        dateInput.value = dateStr;

        attendancePage.loadRosterAttendance();
    },
    currentDateStr: function() {
        const date = new Date();
        let day = date.getDate();
        let month = date.getMonth() + 1;
        let year = date.getFullYear();
        return `${year}-${Util.padNumber(month, 2)}-${Util.padNumber(day, 2)}`;
    },
    removeAllCalendarEvents: function() {
        const events = attendancePage.calendar.getEvents();
        for (const e of events)
        {
            e.remove();
        }
    },
    loadAttendanceEvents: function()
    {
        console.log("Fetching attendance evnets");
        const classId = parseInt(document.getElementById("attendance-class-select").value);
        const date = document.getElementById("selected-date-input").value;
        requestObj = {
            category: "attendanceEvents",
            action: "load",
            data: {
                class_id: classId,
                date: date
            },
            successCallback: function(responseData) {
                // console.log("Success");
                // console.log(responseData);

                attendancePage.removeAllCalendarEvents();
                for (let event of responseData.data.calendarEvents)
                {
                    attendancePage.calendar.addEvent(event);
                }
            },
            errorCallback: function() {
                console.log("ERROR!");
            }
        }
        AsyncApi.getRequest(requestObj);
    },
    loadRosterAttendance: function()
    {
        console.log("Fetching roster attendance");
        const classId = parseInt(document.getElementById("attendance-class-select").value);
        const date = document.getElementById("selected-date-input").value;
        requestObj = {
            category: "attendanceRoster",
            action: "load",
            data: {
                class_id: classId,
                date: date
            },
            successCallback: function(responseData) {
                console.log(responseData.data);

                // Show or hide no students message
                const msgContainer = document.getElementById("student-attendance-messages-container");
                const saveBtn = document.getElementById("student-attendance-saveBtn");
                msgContainer.replaceChildren();
                if (responseData.data.rosterAttendance.length === 0)
                {
                    msgContainer.append(document.createTextNode("No students found in the roster."));
                    msgContainer.classList.remove("is-hidden");
                    saveBtn.classList.add("is-hidden");
                }
                else {
                    msgContainer.classList.add("is-hidden");
                    saveBtn.classList.remove("is-hidden");
                }

                // Render student names
                const studentInfoContainer = document.getElementById("student-info-container");
                studentInfoContainer.replaceChildren();
                for (const item of responseData.data.rosterAttendance)
                {
                    const studentSpan = Util.toHtml(`<div class='mb-1'><span class="button is-static">${item.student.name}</span></div>`);
                    studentInfoContainer.appendChild(studentSpan);
                }
                
                // Render student attedance
                const studentAttendanceContainer = document.getElementById("student-attendance-container");
                studentAttendanceContainer.replaceChildren();
                for (const item of responseData.data.rosterAttendance)
                {
                    console.log(item);
                    // is-selected is-success|is-danger|is-warning
                    const presentSelectedClasses = item.attendance_value == "P" ? " is-selected is-success" : "";
                    const tardySelectedClasses = item.attendance_value == "T" ? " is-selected is-warning" : "";
                    const absentSelectedClasses = item.attendance_value == "A" ? " is-selected is-danger" : "";

                    const presentBtn = Util.toHtml(`<button class="button${presentSelectedClasses}" data-student-id="${item.student.id}" data-attendance-id="${item.attendance_id}" data-payload="P">Present</button>`);
                    const tardyBtn = Util.toHtml(`<button class="button${tardySelectedClasses}" data-student-id="${item.student.id}" data-attendance-id="${item.attendance_id}" data-payload="T">Tardy</button>`);
                    const absentBtn = Util.toHtml(`<button class="button${absentSelectedClasses}" data-student-id="${item.student.id}" data-attendance-id="${item.attendance_id}" data-payload="A">Absent</button>`);

                    const buttonsContainer = Util.toHtml(`<div class="buttons has-addons mb-1"></div>`);
                    buttonsContainer.appendChild(presentBtn);
                    buttonsContainer.appendChild(tardyBtn);
                    buttonsContainer.appendChild(absentBtn);

                    studentAttendanceContainer.appendChild(buttonsContainer);
                }
            },
            errorCallback: function() {
                console.log("ERROR!");
            }
        }
        AsyncApi.getRequest(requestObj);
    }
}

attendancePage.init();


// testing events
// calendar.addEvent({
//     title: "Event",
//     start: "2024-07-12",
//     end: "2024-07-12",
//     backgroundColor: "green",
// });

// calendar.addEvent({
//     title: "Event",
//     start: "2024-07-12",
//     end: "2024-07-12",
//     backgroundColor: "red",
// });
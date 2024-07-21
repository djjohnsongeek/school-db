const attendancePage = {
    calendar: null,
    calendarElement: null,
    payload: {},
    selectedDateElement: null,
    init: function() {
        // Handle changes to the currently selected class
        document.getElementById("attendance-class-select").addEventListener("change", function() {
            attendancePage.loadAttendanceEvents();
            attendancePage.loadRosterAttendance();
        });

        document.getElementById("student-attendance-saveBtn").addEventListener("click", attendancePage.saveAttendance);

        attendancePage.calendarElement = document.getElementById('calendar');
        attendancePage.calendar = new FullCalendar.Calendar(attendancePage.calendarElement, {
            initialView: 'dayGridMonth',
            dateClick: attendancePage.onDateClicked,
            datesSet: attendancePage.onDatesSet
        });
        attendancePage.loadRosterAttendance();

        // render() calls the datesSet callback
        attendancePage.calendar.render();
    },
    // This is called everytime the month is changed
    onDatesSet: function(info) {
        document.getElementById("selected-date-input").value = "";
        attendancePage.loadAttendanceEvents();
        attendancePage.loadRosterAttendance();

    },
    onDateClicked: function(info) {
        attendancePage.selectDate(info.dateStr);
        attendancePage.markCellSelected(info.dayEl);
        attendancePage.loadRosterAttendance();
    },
    markCellSelected: function(cellElement)
    {
        if (attendancePage.selectedDateElement !== null)
        {
            attendancePage.selectedDateElement.classList.remove("selected-cell");
        }
        attendancePage.selectedDateElement = cellElement;
        attendancePage.selectedDateElement.classList.add("selected-cell");
    },
    selectDate: function(dateStr) {
        attendancePage.calendar.select(dateStr);
        const dateInput = document.getElementById("selected-date-input");
        dateInput.value = dateStr;
    },
    currentDateStr: function() {
        const date = new Date();
        return Util.formatDate(date);
    },
    removeAllCalendarEvents: function() {
        const events = attendancePage.calendar.getEvents();
        for (const e of events)
        {
            e.remove();
        }
    },
    onAttendanceBtnClick: function(event) {
        const attendanceBtn = event.currentTarget;
        const attendanceBtns = attendanceBtn.parentElement.children;

        // Clear all btn styles
        for (let btn of attendanceBtns)
        {
            btn.classList.remove("is-selected", "is-success", "is-danger", "is-warning");
        }

        // Define btn's color class
        let colorClass = "";
        switch(attendanceBtn.dataset.payload)
        {
            case "P":
                colorClass = "is-success";
                break;
            case "T":
                colorClass = "is-warning";
                break;
            case "A":
                colorClass = "is-danger";
                break;
            default:
                throw new RangeError(`Invalid Attendance Payload Value: ${attendanceBtn.dataset.payload}`);
        }

        // Set clicked btn's style
        attendanceBtn.classList.add("is-selected", colorClass);

        // Set attendance data
        const attendanceValue = attendanceBtn.dataset.payload;
        const attendanceId = parseInt(attendanceBtn.dataset.attendanceId);
        const studentId = parseInt(attendanceBtn.dataset.studentId);
        attendancePage.payload[studentId] = { studentId, attendanceId, attendanceValue};
    },
    clearAttendancePayload: function() {
        attendancePage.payload = {};
    },
    loadAttendanceEvents: function() {
        console.log("Fetching attendance events");
        const classId = parseInt(document.getElementById("attendance-class-select").value);
        const date = Util.formatDate(attendancePage.calendar.getDate());
        requestObj = {
            category: "attendanceEvents",
            action: "load",
            data: {
                class_id: classId,
                date: date
            },
            successCallback: function(responseData) {
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
    loadRosterAttendance: function() {
        console.log("Fetching roster attendance");
        const classId = parseInt(document.getElementById("attendance-class-select").value);
        const date = document.getElementById("selected-date-input").value;
        const msgContainer = document.getElementById("student-attendance-messages-container");
        const saveBtn = document.getElementById("student-attendance-saveBtn");

        // with no date we cannot lookup or set attendance records
        if (date === "")
        {
            msgContainer.replaceChildren();
            msgContainer.append(document.createTextNode("No date has been selected."));
            msgContainer.classList.remove("is-hidden");
            saveBtn.classList.add("is-hidden");

            let attendanceContainer = document.getElementById("student-attendance-container");
            let infoContainer = document.getElementById("student-info-container");

            attendanceContainer.replaceChildren();
            infoContainer.replaceChildren();

            return;
        }

        requestObj = {
            category: "attendanceRoster",
            action: "load",
            data: {
                class_id: classId,
                date: date
            },
            successCallback: function(responseData) {
                // Show or hide no students message
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

                // Render student roster attendance elements
                const studentAttendanceContainer = document.getElementById("student-attendance-container");
                const studentInfoContainer = document.getElementById("student-info-container");
                studentInfoContainer.replaceChildren();
                studentAttendanceContainer.replaceChildren();
                for (const item of responseData.data.rosterAttendance)
                {
                    // render student names
                    const studentSpan = Util.toHtml(`<div class='mb-1'><span class="button is-static">${item.student.name}</span></div>`);
                    studentInfoContainer.appendChild(studentSpan);

                    // render student buttons
                    const presentSelectedClasses = item.attendance_value == "P" ? " is-selected is-success" : "";
                    const tardySelectedClasses = item.attendance_value == "T" ? " is-selected is-warning" : "";
                    const absentSelectedClasses = item.attendance_value == "A" ? " is-selected is-danger" : "";

                    const presentBtn = Util.toHtml(`<button class="button${presentSelectedClasses}" data-student-id="${item.student.id}" data-attendance-id="${item.attendance_id}" data-payload="P">Present</button>`);
                    const tardyBtn = Util.toHtml(`<button class="button${tardySelectedClasses}" data-student-id="${item.student.id}" data-attendance-id="${item.attendance_id}" data-payload="T">Tardy</button>`);
                    const absentBtn = Util.toHtml(`<button class="button${absentSelectedClasses}" data-student-id="${item.student.id}" data-attendance-id="${item.attendance_id}" data-payload="A">Absent</button>`);
                    
                    for (let btn of [presentBtn, tardyBtn, absentBtn])
                    {
                        btn.addEventListener("click", attendancePage.onAttendanceBtnClick);
                    }
                    
                    const buttonsContainer = Util.toHtml(`<div class="buttons has-addons mb-1"></div>`);
                    buttonsContainer.appendChild(presentBtn);
                    buttonsContainer.appendChild(tardyBtn);
                    buttonsContainer.appendChild(absentBtn);

                    studentAttendanceContainer.appendChild(buttonsContainer);
                }
                attendancePage.clearAttendancePayload();
            },
            errorCallback: function() {
                console.log("ERROR!");
            }
        }
        AsyncApi.getRequest(requestObj);
    },
    saveAttendance: function() {
        const classId = parseInt(document.getElementById("attendance-class-select").value);
        const date = document.getElementById("selected-date-input").value;
        const attendance = [];
        for (const value of Object.values(attendancePage.payload))
        {
            attendance.push(value);
        }

        requestObj = {
            category: "attendance",
            action: "create",
            data: {
                classId,
                date,
                attendance
            },
            successCallback: function(response)
            {
                console.log("Success!");
            },
            errorCallback: function(response)
            {
                console.log("ERROR!");
            }
        }

        AsyncApi.postRequest(requestObj);
    }
}

attendancePage.init();
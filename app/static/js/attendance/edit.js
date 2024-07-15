const attendancePage = {
    calendar: null,
    calendarElement: null,
    init: function() {
        attendancePage.calendarElement = document.getElementById('calendar');
        attendancePage.calendar = new FullCalendar.Calendar(attendancePage.calendarElement, {
            initialView: 'dayGridMonth',
            dateClick: attendancePage.onDateClicked
        });
        
        attendancePage.calendar.render();
        attendancePage.selectDate(attendancePage.currentDateStr());

        attendancePage.loadClassAttendance();
    },
    onDateClicked: function(info) {
        attendancePage.selectDate(info.dateStr);

        const classSelect = document.getElementById("attendance-class-select");
        console.log(classSelect.value);
        attendancePage.loadClassAttendance();
    },
    selectDate: function(dateStr) {
        attendancePage.calendar.select(dateStr);
        const dateInput = document.getElementById("selected-date-input");
        dateInput.value = dateStr;
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
    loadClassAttendance: function()
    {
        // TODO LOADING ANIMATION
        const classId = parseInt(document.getElementById("attendance-class-select").value);
        const date = document.getElementById("selected-date-input").value;
        requestObj = {
            category: "attendance",
            action: "load",
            data: {
                class_id: classId,
                date: date
            },
            successCallback: function(responseData) {
                console.log("Success");
                console.log(responseData);

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
var classEdit = {
    selectedStudentIds: new Set(),
    selectedStudents: [],
    init: function() {
        document.getElementById("add-student-select").addEventListener("change", classEdit.addStudent);
        document.getElementById("add-student-save-btn").addEventListener("click", classEdit.addStudentsToRoster);

        const options = {
            category: "class",
            rowToRemoveIdPrefix: "roster-item-row-",
            successMsg: "The student was successfully removed from the class roster.",
            itemName: null,
        };
        document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, options));
        classEdit.drawAttendanceChart();
    },
    drawSelectedStudents: function()
    {
        const selectedStudentsContainer = document.getElementById("add-student-selected-students");
        const tags = []
        for (const student of classEdit.selectedStudents)
        {
            tags.push(classEdit.createStudentTag(student));
        }

        selectedStudentsContainer.replaceChildren(...tags);
    },
    drawAttendanceChart: function()
    {
        const chartEL = document.getElementById("class-attendance-chart");
        const chartContainer = document.getElementById("class-attendance-chart-container");
        const noAttendanceMsgContainer = document.getElementById("class-attendance-message-container");
        const p = parseInt(document.getElementById("attendance-count-p").value);
        const t = parseInt(document.getElementById("attendance-count-t").value);
        const a = parseInt(document.getElementById("attendance-count-a").value);

        const data = {
            labels: [
              'Present',
              'Tardy',
              'Absent'
            ],
            datasets: [{
              label: '',
              data: [p, t, a],
              backgroundColor: [
                '#3ABB81',
                'rgb(255, 205, 86)',
                'rgb(255, 99, 132)',
              ],
              hoverOffset: 4
            }]
          };

        if (p === 0 & t === 0 & a === 0)
        {
            chartContainer.style.display = "none";
            noAttendanceMsgContainer.style.display = "block";

        }
        else {
            new Chart(chartEL, {
                type: 'pie',
                data: data
            });
        }
    },
    createStudentTag: function(student)
    {
        const htmlStr = `
            <span class="tag is-light" data-student-id="${student.id}">
                ${student.name}
                <button class="delete is-small" type="button" value="${student.id}"></button>
            </span>`;

        const span = Util.toHtml(htmlStr);
        span.firstElementChild.addEventListener("click", classEdit.removeStudent);

        return span;
    },
    addStudent: function(event)
    {
        const studentId = parseInt(event.currentTarget.value);
        if (!isNaN(studentId))
        {
            const selectedOption = document.getElementById(`student-option-${studentId}`);
            const studentName = selectedOption.innerText.trim();
            if (!classEdit.selectedStudentIds.has(studentId))
            {
                classEdit.selectedStudentIds.add(studentId);
                classEdit.selectedStudents.push({ name: studentName, id: studentId});
            }
            else {
                event.currentTarget.value = "";
            }

            classEdit.drawSelectedStudents();
        }
    },
    removeStudent: function(event) {
        const studentId = parseInt(event.currentTarget.value);
        if (!isNaN(studentId))
        {
            classEdit.selectedStudentIds.delete(studentId);
            const i = classEdit.selectedStudents.findIndex((item) => item.id === studentId);
            classEdit.selectedStudents.splice(i, 1);
        }

        classEdit.drawSelectedStudents();

        if (classEdit.selectedStudents.length === 0)
        {
            const noSelection = Util.toHtml(`<span class="has-text-grey-light">No Students Selected</span>`);
            document.getElementById("add-student-selected-students").replaceChildren(...[noSelection])
        }
    },
    addStudentsToRoster: function()
    {
        const classId = parseInt(document.getElementById("add-student-class-id-input").value);
        const options = {
            category: "class",
            action: "create",
            data: {
                student_ids: Array.from(classEdit.selectedStudentIds),
                itemId: classId
            },
            successCallback: function(responseData) {
                if (responseData.errors.length == 0)
                {
                    const modalElement = document.getElementById("add-student-modal");
                    Modal.close(modalElement);
                    classEdit.addNewRosterEntries(responseData.data.roster);
                    Messages.addMessage("Student(s) successfully added!", "success");
                }
                else {
                    Messages.addMessages(responseData.errors, "danger");
                }

            },
            errorCallback: function() {
                Messages.addMessage("A server error occured.");
            }
        }

        AsyncApi.postRequest(options);
    },
    addNewRosterEntries: function(roster) {
        let rosterTableBody = document.getElementById("class-roster-table-body");
        if (rosterTableBody === null)
        {
            rosterTableBody = classEdit.createRosterTableBody();
        }
        
        for (let item of roster)
        {
            data = {
                studentEditUrl: `/students/edit/${item.student.id}`,
                rosterItemId: item.id,
                studentFullName: item.student.name,
            }

            const rowElement = classEdit.createStudentRow(data);
            rosterTableBody.appendChild(rowElement);
        }
    },
    createRosterTableBody: function()
    {
        const rosterContainer = document.getElementById("class-roster-container");
        const tableHtmlString = `
            <table class="table is-fullwidth">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Attendance</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="class-roster-table-body">
                </tbody>
            </table>`;

        const table = Util.toHtml(tableHtmlString);
        rosterContainer.replaceChildren(...[table]);
        return document.getElementById("class-roster-table-body");
    },
    clearSelectedStudents: function()
    {
        classEdit.selectedStudents.length = 0;
        classEdit.selectedStudentIds.clear();
        classEdit.drawSelectedStudents();
    },
    createStudentRow: function(data)
    {
        const htmlStr = `
        <tr id="roster-item-row-${data.rosterItemId}">
            <td>
                <a href="${data.studentEditUrl}">
                    ${data.studentFullName}
                </a>
            </td>
            <td>
                <span class="tag is-success">
                    P: ?
                </span>
                <span class="tag is-danger">
                    A: ?
                </span>
                <span class="tag is-warning">
                    T: ?
                </span>
            </td>
        </tr>`;

        const removeBtnHtmlStr = `
        <button class="button is-danger modal-trigger" data-item-id="${data.rosterItemId}" data-target="confirm-delete-modal">
            <span class="icon-text">
                <span class="icon">
                    <i class="fa fa-ban" aria-hidden="true"></i>
                </span>
                <span>Remove</span>
            </span>
        </button>`


        const htmlRow = Util.toHtml(htmlStr);
        const lastCell = document.createElement("td");
        const removeBtn = Util.toHtml(removeBtnHtmlStr);
        lastCell.append(removeBtn);
        htmlRow.append(lastCell);

        removeBtn.addEventListener("click", Modal._openAndSetItemId);


        return htmlRow;
    }


}


classEdit.init();
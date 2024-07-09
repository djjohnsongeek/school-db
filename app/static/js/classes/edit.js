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
                if (!responseData.errors)
                {
                    const modalElement = document.getElementById("add-student-modal");
                    Modal.close(modalElement);
                    Messages.addMessage("Student(s) successfully added!", "success");
                    // we need to add the students
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
    clearSelectedStudents: function()
    {
        classEdit.selectedStudents.length = 0;
        classEdit.selectedStudentIds.clear();
        classEdit.drawSelectedStudents();
    },
    createStudentRow: function()
    {
        data = {
            rosterItemId: 1,
            studentEditUrl: "",
            studentFullName: "",
        }
        const htmlStr = `
        <tr id="roster-item-row-${rosterItemId}">
            <td>
                <a href="${studentEditUrl}">
                    ${studentFullName}
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
            <td>
                <button class="button is-danger modal-trigger" data-item-id="${rosterItemId}" data-target="confirm-delete-modal">
                    <span class="icon-text">
                        <span class="icon">
                            <i class="fa fa-ban" aria-hidden="true"></i>
                        </span>
                        <span>Remove</span>
                    </span>
                </button>
            </td>
        </tr>`;

        const html = Util.toHtml(htmlStr);

        return ;
    }


}


classEdit.init();
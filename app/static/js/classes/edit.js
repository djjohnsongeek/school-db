var classEdit = {
    selectedStudentIds: new Set(),
    selectedStudents: [],
    init: function() {
        document.getElementById("add-student-select").addEventListener("change", classEdit.addStudent);
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


}


classEdit.init();
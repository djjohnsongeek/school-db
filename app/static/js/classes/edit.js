var classEdit = {
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
        const tag = document.createElement("span");
        tag.dataset.studentId = student.id;
        tag.classList.add("tag", "is-light");
        const text = document.createTextNode(student.name);
        tag.appendChild(text);

        return tag;
    },
    addStudent: function(event)
    {
        const selectValue = event.currentTarget.value;
        if (selectValue !== "")
        {
            const selectedOption = document.getElementById(`student-option-${selectValue}`);
            const studentName = selectedOption.innerText.trim();
            classEdit.selectedStudents.push({ name: studentName, id: selectValue});
            classEdit.drawSelectedStudents();
        }
    }
}


classEdit.init();
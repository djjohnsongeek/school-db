class StudentGrades {

    finalGradeInputs = null;

    constructor()
    {
        this.finalGradeInputs = document.getElementsByClassName("student-grade-input");
        for (let input of this.finalGradeInputs)
        {
            input.addEventListener("change", this.updateFinalGrade);
        }
    }

    updateFinalGrade(event) {
        const input = event.currentTarget;
        let requestObj = {
            category: "student",
            action: "update",
            data: {
                class_id: input.dataset.classId,
                student_id: input.dataset.studentId,
                record_id: input.dataset.recordId,
                final_grade: input.value
            },
            successCallback: (response) => {
                Messages.addMessage("Student's grade updated successfully.", "success")
            },
            errorCallback: (response) => {
                // gets call on server or customer errors
            },
            finallyCallback: () => {

            }
        }
        AsyncApi.postRequest(requestObj);
    }
}

var studentGrades = new StudentGrades();
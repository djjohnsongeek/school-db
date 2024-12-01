class StudentEditPage {

    finalGradeInputs = null;

    constructor()
    {
        console.log("Constructing");
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
                final_grade: input.value
            },
            successCallback: (response) => {
                console.log("success");
            },
            errorCallback: (response) => {
                console.log("error");
            },
            finallyCallback: () => {
                console.log("finally!");
            }
        }

        console.log(requestObj.data);

        AsyncApi.postRequest(requestObj);
    }
}

var studentEdit = new StudentEditPage();
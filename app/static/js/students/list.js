let deleteRequestConfig = {
    category: "student",
    successMsg : "The student was successfully deleted.",
    rowToRemoveIdPrefix: "student-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
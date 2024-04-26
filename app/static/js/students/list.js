let deleteRequestConfig = {
    category: "student",
    itemName : "Student",
    rowToRemoveIdPrefix: "student-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
let deleteRequestConfig = {
    category: "staff",
    successMsg : "The staff member was successfully deleted.",
    rowToRemoveIdPrefix: "staff-member-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
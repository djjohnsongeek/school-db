let deleteRequestConfig = {
    category: "staff",
    itemName : "Staff member",
    rowToRemoveIdPrefix: "staff-member-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
let deleteRequestConfig = {
    category: "term",
    successMsg : "The term was successfully deleted.",
    rowToRemoveIdPrefix: "term-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
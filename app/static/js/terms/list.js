let deleteRequestConfig = {
    category: "term",
    itemName : "Term",
    rowToRemoveIdPrefix: "term-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
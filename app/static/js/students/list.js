let deleteRequestConfig = {
    category: "student",
    successMsg : "The student was successfully deleted.",
    rowToRemoveIdPrefix: "student-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));

$(document).ready( function () {
    const table = $('#students-table').DataTable();
    document.getElementsByClassName("dt-search")[0].style.display = "none";
    document.getElementById("students-search-input").addEventListener("keyup", (event) => {
        const queryString = event.currentTarget.value;
        table.search(queryString).draw();
    });
} );
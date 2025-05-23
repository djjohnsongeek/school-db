class StudentList
{
    constructor()
    {
        // Setup data table
        this.table = $('#students-table').DataTable({
            layout: {
                topStart: 'pageLength',
                topEnd: null,
                bottomStart: 'info',
                bottomEnd: 'paging'
            }
        });
        document.getElementById("students-search-input").addEventListener("keyup", (event) => {
            const queryString = event.currentTarget.value;
            this.table.search(queryString).draw();
        });
    
        // Setup table row buttons
        let deleteRequestConfig = {
            category: "student",
            successMsg : "The student was successfully deleted.",
            rowToRemoveIdPrefix: "student-row-",
            dataTable: this.table
        }
    
        document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
    }
}

$(document).ready( function () {
    const studentListPage = new StudentList();
});
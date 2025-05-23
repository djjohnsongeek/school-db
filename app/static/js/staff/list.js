class StaffList {

    constructor()
    {
        // Setup datatable
        this.table = $('#staff-table').DataTable({
            layout: {
                topStart: 'pageLength',
                topEnd: null,
                bottomStart: 'info',
                bottomEnd: 'paging'
            }
        });

        document.getElementById("staff-search-input").addEventListener("keyup", (event) => {
            const queryString = event.currentTarget.value;
            this.table.search(queryString).draw();
        });

        // Setup table row buttons
        let deleteRequestConfig = {
            category: "staff",
            successMsg : "The staff member was successfully deleted.",
            rowToRemoveIdPrefix: "staff-member-row-",
            dataTable: this.table
        };

        document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
        document.getElementById("pwreset-save-btn").addEventListener("click", function(event) {
            const modalElement = event.currentTarget.closest(".modal");
            const staffId = parseInt(modalElement.dataset.itemId);
            new_password = document.getElementById("pwreset-password").value;

            let options = {
                category: "password",
                action: "reset",
                data: {
                    staff_id: staffId,
                    password: new_password
                },
                successCallback: function(responseData) {
                    if (responseData.errors.length == 0)
                    {
                        Messages.addMessage("Password reset successfully!", "success");
                        document.getElementById("pwreset-password").value = "";
                        Modal.close(modalElement);
                    }
                },
                errorCallback: function() {
                    // dont close modal
                }
            };

            AsyncApi.postRequest(options);
        });
    }
}


$(document).ready( function () {
    var staffListPage = new StaffList();
});
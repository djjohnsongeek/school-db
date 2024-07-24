let deleteRequestConfig = {
    category: "staff",
    successMsg : "The staff member was successfully deleted.",
    rowToRemoveIdPrefix: "staff-member-row-",
}

document.getElementById("confirm-delete-btn").addEventListener("click", (event) => AppApi.deleteRequest(event, deleteRequestConfig));
document.getElementById("").addEventListener("click", function(event) {
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
                Messages.addMessage("Password reset successfully!", "is-success");
                // all is well
            }

            // error messages have already been displaye
        },
        errorCallback: function() {
             // dont close modal
        }
    };

    AsyncApi.postRequest(options);
});
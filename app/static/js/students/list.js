
// Delete Student Modal Confirm Button
document.getElementById("confirm-delete-btn").addEventListener("click", function(event) {
    const eventElement = event.currentTarget;
    const modalElement = eventElement.closest(".modal");
    const itemId = modalElement.dataset.itemId;
    Modal.close(modalElement);

    let options = {
        category: "student",
        action: "delete",
        data: {
            itemId: itemId
        },
        successCallback: function(response)
        {
            const id = response.data.itemId;
            let rowEl = document.getElementById(`student-row-${id}`);
            rowEl.remove();
            delete rowEl;

            Messages.addMessage("Student successfully deleted.", "success");
        },
        errorCallback: function() {
            console.log("Called error call back");
        }
    }
    AsyncApi.postRequest(options)
});

// Delete Staff Modal Confirm Button
document.getElementById("confirm-delete-btn").addEventListener("click", function(event) {
    const eventElement = event.currentTarget;
    const modalElement = eventElement.closest(".modal");
    const itemId = modalElement.dataset.itemId;
    Modal.close(modalElement);

    let options = {
        category: "staff",
        action: "delete",
        data: {
            itemId: itemId
        },
        successCallback: function(data)
        {
            console.log("Called success callback");
            console.log(data);
        },
        errorCallback: function() {
            console.log("Called error call back");
        }
    }
    AsyncApi.postRequest(options)
});
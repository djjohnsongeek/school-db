// Scripts to be run on each page

// Remove the parent of .delete elements on click
for (let element of document.getElementsByClassName("delete"))
{
    element.addEventListener("click", function(event) {
        const notification = event.currentTarget.parentNode;
        const container = notification.parentNode;
        container.removeChild(notification)
    });
}

// Modals Logic
var Modal = {
    initialize: function()
    {
        // trigger open logic
        for (let element of document.getElementsByClassName("modal-trigger"))
        {
            element.addEventListener("click", function(event) {
                const targetId = event.currentTarget.dataset.target;
                const itemId = event.currentTarget.dataset.itemId;
                const targetElement = document.getElementById(targetId);
                targetElement.dataset.itemId = itemId;
                Modal.open(targetElement);
            });
        }
        
        // escape keyboard shortcut
        document.addEventListener('keydown', function (event) {
            if(event.key === "Escape") {
                Modal.closeAll();
            }
        });

        // cancel button logic
        for (let element of document.getElementsByClassName("close-modal"))
        {
            element.addEventListener("click", function(event) {
                const modalElement = event.currentTarget.closest(".modal")
                if (modalElement)
                {
                    Modal.close(modalElement);
                }
            });
        }
    },
    open: function(element)
    {
        element.classList.add("is-active");
    },
    close: function(element)
    {
        element.classList.remove("is-active");
        delete element.dataset.itemId;
    },
    closeAll: function()
    {
        for (let modalElement of document.getElementsByClassName("modal"))
        {
            Modal.close(modalElement);
        }
    },
}

// Messages Logic
var Messages = {
    containerId: "app-messages-container",
    addMessage: function(msg, category)
    {
        const container = document.getElementById(this.containerId);
        let msgHtml = this.createMsgHtml(msg, category);
        container.appendChild(msgHtml);
    },
    addMessages: function(msgs, category)
    {
        for (let msg of msgs)
        {
            this.addMessage(msg, category);
        }
    },
    createMsgHtml(msg, category)
    {
        // validate category
        if (!["danger", "warning", "success"].includes(category))
        {
            throw new Error("Invalid message category detected.");
        }
        
        // Create div container
        let msgContainer = document.createElement("div");
        msgContainer.classList.add("notification");
        msgContainer.classList.add(`is-${category}`);
        let msgTextNode = document.createTextNode(msg);

        // Create delete button
        let msgDelBtn = document.createElement("button");
        msgDelBtn.classList.add("delete")

        // Link the two
        msgContainer.appendChild(msgDelBtn);
        msgContainer.appendChild(msgTextNode);
        
        // Add event listener
        msgDelBtn.addEventListener("click", function(event) {
            const notification = event.currentTarget.parentNode;
            const container = notification.parentNode;
            container.removeChild(notification)
        });

        return msgContainer;
    }
}

// Async Request logic

/*
requestObj = {
    category: "",
    action: "",
    data: {},
    successCallback: function(),
    errorCallback: function()
}
*/
// need to gracefully handle HTTP error codes automatically
var AsyncApi = {
    baseURL: "/api",
    postRequest: async function(requestObj)
    {
        const url = `${this.baseURL}/${requestObj.category}/${requestObj.action}`;
        options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify(requestObj.data),
        }
     
        fetch(url, options)
            .then((response) => {
                if (response.ok)
                {
                    response.json().then((responseData) => {
                        if (responseData.errors.length > 0)
                        {
                            Messages.addMessages(responseData.errors, "danger");
                        }
                        else {
                            requestObj.successCallback(responseData);
                        }
                    });
                }
                else {
                    Messages.addMessage(`A server error occured: ${response.status} `, "danger");
                    requestObj.errorCallback();
                }
            })
            .catch((error) => {
                console.log(error);
                Messages.addMessage("An unknown error occured.", "danger");
            });
    }
}


var AppApi = {
    deleteRequest: function(event, configObj) {
        const eventElement = event.currentTarget;
        const modalElement = eventElement.closest(".modal");
        const itemId = modalElement.dataset.itemId;
        Modal.close(modalElement);
    
        let options = {
            category: configObj.category,
            action: "delete",
            data: {
                itemId: itemId
            },
            successCallback: function(response)
            {
                const id = response.data.itemId;
                let rowEl = document.getElementById(`${configObj.rowToRemoveIdPrefix}${id}`);
                rowEl.remove();
                delete rowEl;
    
                Messages.addMessage(`${configObj.itemName} successfully deleted.`, "success");
            },
            errorCallback: function() {
                console.log("Called error call back");
            }
        }
        AsyncApi.postRequest(options);
    }
}

Modal.initialize();
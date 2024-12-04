// Scripts to be run on each page
var App = {
    init: function()
    {
        // Remove the parent of .delete-message elements on click
        for (let element of document.getElementsByClassName("delete-message"))
        {
            element.addEventListener("click", (event) => App.removeParent(event));
        }

        // Hide, Reveal Logic
        for (let element of document.getElementsByClassName("toggle"))
        {
            element.addEventListener("click", (event) => App.toggleVisible(event));
        }

        setInterval(App.popMessage, 4500);
    },
    toggleVisible: function(event) {
        const t = event.currentTarget.dataset.target;
        const targets = t.split(",");
        for (let target of targets)
        {
            const targetElm = document.getElementById(target);
            if (targetElm.classList.contains("is-hidden"))
            {
                targetElm.classList.remove("is-hidden");
            }
            else {
                targetElm.classList.add("is-hidden");
            }
        }
    },
    removeParent: function(event) {
        const notification = event.currentTarget.parentNode;
        const container = notification.parentNode;
        container.removeChild(notification)
    },
    popMessage: function()
    {
        const messages_container = document.getElementById("app-messages-container");
        if (messages_container)
        {
            messages = messages_container.children;
            if (messages.length > 0)
            {
                messages[0].remove();
            }
        }
    }
}



// Modals Logic
var Modal = {
    init: function()
    {
        // trigger open logic
        for (let element of document.getElementsByClassName("modal-trigger"))
        {
            element.addEventListener("click", Modal._openAndSetItemId);
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
            element.addEventListener("click", Modal._close);
        }
    },
    _openAndSetItemId: function(event)
    {
        const targetId = event.currentTarget.dataset.target;
        const itemId = event.currentTarget.dataset.itemId;
        const targetElement = document.getElementById(targetId);
        targetElement.dataset.itemId = itemId;
        Modal.open(targetElement);
    },
    _close: function(event) {
        const modalElement = event.currentTarget.closest(".modal");
        if (modalElement)
        {
            Modal.close(modalElement);
        }
    },
    open: function(element)
    {
        element.classList.add("is-active");
    },
    close: function(element)
    {
        element.classList.remove("is-active");
    },
    closeAll: function()
    {
        for (let modalElement of document.getElementsByClassName("modal"))
        {
            Modal.close(modalElement);
        }
    },
}

// General Utilities
var Util = {
    toHtml: function(html)
    {
        html = html.trim();

        const template = document.createElement("template");
        template.innerHTML = html;
        const result = template.content.children;
        if (result.length == 1)
        {
            return result[0];
        }
        else {
            return result;
        }
    },
    padNumber: function(n, target_len)
    {
        let nStr = n.toString();
        return nStr.padStart(target_len, "0");
    },
    formatDate: function(date)
    {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}-${Util.padNumber(month, 2)}-${Util.padNumber(day, 2)}`;
    }
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
    errorCallback: function(),
    finallyCallback: function()
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
                            requestObj.errorCallback();
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
                requestObj.errorCallback();
            })
            .finally()
            {
                if (typeof requestObj.errorCallback === 'function') {
                    requestObj.finallyCallback();
                }
            };
    },
    getRequest: async function(requestObj) {
        const paramStr = new URLSearchParams(requestObj.data).toString();
        const url = `${this.baseURL}/${requestObj.category}/${requestObj.action}?${paramStr}`;
        options = {
            method: "GET",
            headers: {
                "X-CSRFToken": csrf_token,
            },
        }
        fetch(url, options)
            .then((response) => {
                if (response.ok)
                {
                    response.json().then((responseData) => {
                        if (responseData.errors.length > 0)
                        {
                            Messages.addMessages(responseData.errors, "danger");
                            requestObj.errorCallback();
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
                requestObj.errorCallback();
            })
            .finally()
            {
                if (typeof requestObj.errorCallback === 'function') {
                    requestObj.finallyCallback();
                }
            }
    }
}


var AppApi = {
    /* DELETE Requests Config Obj
        {
            category: string
            itemName : string, 
            rowToRemoveIdPrefix: string
        }
    */
    deleteRequest: function(event, configObj) {
        AppApi.closeModal(event);
        const modalElement = event.currentTarget.closest(".modal");
        const itemId = modalElement.dataset.itemId;
        let options = {
            category: configObj.category,
            action: "delete",
            data: {
                itemId: itemId
            },
            successCallback: function(response)
            {
                if (response.errors.length == 0)
                {
                    const id = response.data.itemId;
                    let rowEl = document.getElementById(`${configObj.rowToRemoveIdPrefix}${id}`);
                    rowEl.remove();
                    delete rowEl;

                    if (configObj.successMsg)
                    {
                        Messages.addMessage(configObj.successMsg, "success");
                    }
                }
                else {
                    Messages.addMessages(response.errors, "danger");
                }

            },
            errorCallback: function() {
            }
        }
        AsyncApi.postRequest(options);
    },
    /* CREATE Requests Config Obj
        {
            category: string
            formData : FormData 
            successCallback: function
        }
    */
    createRequest: function(event, configObj) {
        AppApi.closeModal(event);
        let options = {
            category: configObj.category,
            action: "create",
            data: Object.fromEntries(configObj.formData),
            successCallback: function(response)
            {
                configObj.successCallback(response.data);
                Messages.addMessage(`${configObj.category} successfully created!`, "success")
            },
            errorCallback: function() {
                Messages.addMessage(`Failed to create ${configObj.category}`);
            }
        }
        AsyncApi.postRequest(options);
    },
    closeModal: function(event)
    {
        const eventElement = event.currentTarget;
        const modalElement = eventElement.closest(".modal");
        Modal.close(modalElement);
    },
}

App.init();
Modal.init();
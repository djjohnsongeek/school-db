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

// MODAL LOGIC
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
Modal.initialize();
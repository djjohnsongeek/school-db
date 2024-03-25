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
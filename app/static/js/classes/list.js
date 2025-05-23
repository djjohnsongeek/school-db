

class ClassList {
    constructor()
    {
        this.dataTable = $("#classes-table").DataTable({ 
            layout: {
                topStart: 'pageLength',
                topEnd: null,
                bottomStart: 'info',
                bottomEnd: 'paging'
            }
        });

        document.getElementById("classes-search-input").addEventListener("keyup", (event) => {
            const queryString = event.currentTarget.value;
            this.dataTable.search(queryString).draw();
        });

        const termsSelect = document.getElementById("class-list-terms-select");

        termsSelect.addEventListener("change", function(event) {
            termId = event.currentTarget.value;
            const url = new URL(window.location);
            url.searchParams.set("term_id", termId);
            window.location = url.href;
        });
    }
}

const classList = new ClassList();
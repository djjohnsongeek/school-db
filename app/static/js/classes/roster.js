document.getElementById("apply-changes-btn").addEventListener("click", function() {
    startDateInput = document.getElementById("start-date-input");
    numberOfDaysInput = document.getElementById("number-of-days-input");
    skipWeekendsSelect = document.getElementById("skip-weekends-select");

    url = new URL(window.location.href);

    url.searchParams.set("start_date", startDateInput.value);
    url.searchParams.set("days", numberOfDaysInput.value);
    url.searchParams.set("skip_weekends", skipWeekendsSelect.value)


    window.location.href = url.toString();
});

document.getElementById("print-btn").addEventListener("click", function() {
    print();
});
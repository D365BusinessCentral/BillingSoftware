function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteReference(id) {

    if (confirm('Are you sure you want to delete this Reference?') == true) {
        fetch("/delete-reference", {
            method: "POST",
            body: JSON.stringify({ referenceId: id }),
        }).then((_res) => {
            window.location.href = "/References";
        });
    } else {
        return 0;
    }
}

function deleteTestType(id) {

    if (confirm('Are you sure you want to delete this Test Type?') == true) {
        fetch("/delete-testType", {
            method: "POST",
            body: JSON.stringify({ testTypeId: id }),
        }).then((_res) => {
            window.location.href = "/TestTypes";
        });
    } else {
        return 0;
    }
}

function deleteTest(id) {

    if (confirm('Are you sure you want to delete this Test?') == true) {
        fetch("/delete-test", {
            method: "POST",
            body: JSON.stringify({ testId: id }),
        }).then((_res) => {
            window.location.href = "/Tests";
        });
    } else {
        return 0;
    }
}

function deleteReporter(id) {

    if (confirm('Are you sure you want to delete this Reporting Person?') == true) {
        fetch("/delete-reporter", {
            method: "POST",
            body: JSON.stringify({ reporterId: id }),
        }).then((_res) => {
            window.location.href = "/Reporters";
        });
    } else {
        return 0;
    }
}

function deleteEmployee(id) {

    if (confirm('Are you sure you want to delete this Employee?') == true) {
        fetch("/delete-employee", {
            method: "POST",
            body: JSON.stringify({ empId: id }),
        }).then((_res) => {
            window.location.href = "/Employees";
        });
    } else {
        return 0;
    }
}
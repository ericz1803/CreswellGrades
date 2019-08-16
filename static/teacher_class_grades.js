var currently_editing = [];
var assignment_queue = [];

//add new assignment
function newAssignment(e) {
    e.parentElement.innerHTML = '<button class="btn btn-primary" onclick="cancelSubmitNewAssignment(this)"><i class="fas fa-times"></i></button> <button class="btn btn-primary" onclick="submitNewAssignment(this)"><i class="fas fa-check"></i></button>';
    let elements = document.querySelectorAll(".new");
    for (let element of elements) {
        //select input type
        switch (element.parentElement.className) {
            case "name-row":
                element.innerHTML = `<input class="form-control input-sm" type="text" placeholder="Assignment Name">`;
                break;
            case "date-row":
                element.innerHTML = `<input class="form-control input-sm" type="date">`;
                let today = new Date();
                element.children[0].value = today.toISOString().substr(0,10);
                break;
            case "category-row":
                let contents = element.innerHTML;
                element.innerHTML = document.getElementById('category-selector').innerHTML;
                break;
            case "pts-row":
            case "num-row":
                element.innerHTML = `<input class="form-control input-sm" type="number" value="" step=0.1>`;
                break;
        }
        
        //fix padding
        element.style.paddingTop = '0.375rem';
        element.style.paddingBottom = '0.375rem';
    }
}

function cancelSubmitNewAssignment(e) {
    //TODO
    e.parentElement.innerHTML = '<button class="btn btn-primary" onclick="newAssignment(this)"><i class="fas fa-plus-circle"></i></button>';
    let elements = document.querySelectorAll(".new");
    values_json = {student_points: []};
    for (let element of elements) {
        switch (element.parentElement.className) {
            case "button-row":
                break;
            default:
                element.innerHTML = "";
        }
        //fix padding
        element.style.paddingTop = '0.75rem';
        element.style.paddingBottom = '0.75rem';
    }
}

function submitNewAssignment(e) {
    let valid = true;
    //check if everything is filled out
    let elements = document.querySelectorAll(".new");
    for (let element of elements) {
        switch (element.parentElement.className) {
            case "name-row":
            case "date-row":
            case "pts-row":
                if (element.children[0].value.length == 0) {
                    element.children[0].classList.add("is-invalid");
                    valid = false;
                } else {
                    element.children[0].classList.remove("is-invalid");
                }  
        }
        //fix padding
        element.style.paddingTop = '0.75rem';
        element.style.paddingBottom = '0.75rem';
    }
    //quit if not
    if (valid == false) {
        return;
    }

    //handle submission
    e.parentElement.innerHTML = '<button class="btn btn-primary" onclick="newAssignment(this)"><i class="fas fa-plus-circle"></i></button>';
    let class_id = document.getElementById("class-id").value;
    let values_json = {student_points: [], id: class_id};
    for (let element of elements) {
        switch (element.parentElement.className) {
            case "button-row":
                break;
            case "category-row":
                let e = element.children[0];
                values_json["category"] = parseInt(e.options[e.selectedIndex].value);
                element.innerHTML = "";
                break;
            case "num-row":
                let student_id = element.id.split('_')[1];
                let val = element.children[0].value;
                values_json.student_points.push([parseInt(student_id), parseFloat(val)]);
                element.innerHTML = "";
                break;
            case "pts-row":
                let v = element.children[0].value;
            
                values_json[element.id.split('_')[1]] = parseFloat(v);
                element.innerHTML = "";
                break;
            default:
                //name, date
                let val_ = element.children[0].value;
                
                values_json[element.id.split('_')[1]] = val_;
                element.innerHTML = "";
                break;
        }
    }
    console.log(values_json);

    //send json to server
    let secret_key = document.getElementById('secret-key').value;
    $.ajax({
        url: '/ajax/new-grades',
        type: "POST",
        headers: {
            'secret_key': secret_key,
        },
        data: JSON.stringify(values_json, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
            if (response["saved"]) {
                console.log("Saved.");
            } else {
                console.log("Unable to save");
            }
        }
    });
}

//edit assignment
function edit(e) {
    let p = e.parentElement;
    p.innerHTML = '<button class="btn btn-primary" onclick="doneEdit(this)"><i class="fas fa-check"></i></button>';
    if (currently_editing.includes(p.className)) {
        return;
    }
    currently_editing.push(p.className);
    let elements = document.querySelectorAll("." + p.className);
    

    //match button element
    for (let element of elements) {
        //select input type
        switch (element.parentElement.className) {
            case "name-row":
                element.innerHTML = `<input class="form-control input-sm" type="text" value="${element.innerHTML}">`;
                break;
            case "date-row":
                element.innerHTML = `<input class="form-control input-sm" type="date" value="${element.innerHTML}">`;
                break;
            case "category-row":
                let contents = element.innerHTML;
                element.innerHTML = document.getElementById('category-selector').innerHTML;
                for (let child of element.children[0].children) {
                    if (child.text == contents) {
                        child.selected = true;
                    }
                }
                break;
            case "pts-row":
            case "num-row":
                element.innerHTML = `<input class="form-control input-sm" type="number" value="${element.innerHTML}" step=0.1>`;
                break;
        }
        //fix padding
        element.style.paddingTop = '0.375rem';
        element.style.paddingBottom = '0.375rem';
    }
}

//sends json to server
/*
{
    assignment_id: int,
    date: str,
    name: str,
    points: int,
    category: int,
    student_points: [[student_id (int), student_points (int)], [student_id (int), student_points (int)]]
}
*/
function doneEdit(e) {
    let p = e.parentElement;
    p.innerHTML = '<button class="btn btn-primary" onclick="edit(this)"><i class="far fa-edit"></i></button>';
    currently_editing = currently_editing.filter(x => x != p.className);

    //remove input fields and package data into json
    values_json = {assignment_id: parseInt(p.className.slice(11), 10), student_points: []};
    let elements = document.querySelectorAll("." + p.className);
    for (let element of elements) {
        switch (element.parentElement.className) {
            case "button-row":
                break;
            case "category-row":
                let e = element.children[0];
                values_json["category"] = parseInt(e.options[e.selectedIndex].value);
                element.innerHTML = e.options[e.selectedIndex].text;
                break;
            case "num-row":
                let student_id = element.id.split('_')[1];
                let val = element.children[0].value;
                values_json.student_points.push([parseInt(student_id), parseFloat(val)]);
                element.innerHTML = val;
                break;
            case "pts-row":
                let v = element.children[0].value;
            
                values_json[element.id.split('_')[2]] = parseFloat(v);
                element.innerHTML = v;
                break;
            default:
                //name, date
                let val_ = element.children[0].value;
                
                values_json[element.id.split('_')[2]] = val_;
                element.innerHTML = val_;
                break;
        }
        //fix padding
        element.style.paddingTop = '0.75rem';
        element.style.paddingBottom = '0.75rem';
    }
    
    //send json to server
    let secret_key = document.getElementById('secret-key').value;
    $.ajax({
        url: '/ajax/update-grades',
        type: "POST",
        headers: {
            'secret_key': secret_key,
        },
        data: JSON.stringify(values_json, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
            if (response["saved"]) {
                console.log("Saved.");
            } else {
                console.log("Unable to save");
            }
        }
    });
}
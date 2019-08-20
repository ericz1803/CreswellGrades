//grade factor
var weights = {};
//lowest grades
var drop = {};
var a, b, c, d;

document.onload = get_values();
document.onload = calculate_grades();

//get weights, drop, and grade scale
function get_values() {
    //grade scale
    a = parseFloat(document.getElementById("a").value);
    b = parseFloat(document.getElementById("b").value);
    c = parseFloat(document.getElementById("c").value);
    d = parseFloat(document.getElementById("d").value);

    //weights
    let w = document.getElementById('weights');
    for (let i = 0; i < w.children.length; i++) {
        weights[i + 1] = parseFloat(w.children[i].value);
    }

    //drop
    let dr = document.getElementById('drop');
    for (let i = 0; i < w.children.length; i++) {
        drop[i + 1] = parseInt(dr.children[i].value);
    }
}

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
        element.style.paddingTop = '0.35rem';
        element.style.paddingBottom = '0.35rem';
    }
}

//cancel adding new assignment
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
                element.innerHTML = "&nbsp;";
        }
        //fix padding
        element.style.paddingTop = '0.75rem';
        element.style.paddingBottom = '0.75rem';
    }
}

//submits new assigment to server if valid
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
    //assemble values_json and clear column
    e.parentElement.innerHTML = '<button class="btn btn-primary" onclick="newAssignment(this)"><i class="fas fa-plus-circle"></i></button>';
    let class_id = document.getElementById("class-id").value;
    let values_json = {student_points: {}, id: class_id};
    for (let element of elements) {
        switch (element.parentElement.className) {
            case "button-row":
                break;
            case "category-row":
                let e = element.children[0];
                values_json["category"] = parseInt(e.options[e.selectedIndex].value);
                values_json["category-name"] = e.options[e.selectedIndex].text;
                element.innerHTML = "";
                break;
            case "num-row":
                let student_id = element.id.split('_')[1];
                let val = element.children[0].value;
                values_json.student_points[parseInt(student_id)] = parseFloat(val);
                element.innerHTML = "&nbsp;";
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
                //Add to list
                for (let element of elements) {
                    let new_element = document.createElement("td");
                    new_element.className = "assignment_" + response["id"];
                    switch (element.parentElement.className) {
                        case "name-row":
                            new_element.innerText = values_json["name"];
                            new_element.id = "assignment_" + response["id"] + "_name";
                            break;
                        case "button-row":
                            new_element.innerHTML = '<button class="btn btn-primary" onclick="edit(this)"><i class="far fa-edit"></i></button>';
                            break;
                        case "category-row":
                            new_element.innerHTML = `<input type="hidden" id="assignment_${response["id"]}_category_num" value="${values_json["category-name"]}"></input>` + values_json["category-name"];
                            new_element.id = "assignment_" + response["id"] + "_category";
                            break;
                        case "pts-row":
                            new_element.innerText = values_json["points"];
                            new_element.id = "assignment_" + response["id"] + "_points";
                            break;
                        case "date-row":
                            new_element.innerText = values_json["date"];
                            new_element.id = "assignment_" + response["id"] + "_date";
                            break;
                        case "num-row":
                            let student_id = parseInt(element.id.split('_')[1]);
                            let student_val = values_json.student_points[student_id];
                            if (student_val) {
                                new_element.innerText = student_val;
                            } else {
                                new_element.innerText = "";   
                            }
                            new_element.id = "student_" + student_id + "_assigment_" + response["id"] + "_points";
                            break;
                    }
                    element.parentElement.insertBefore(new_element, element.previousElementSibling);
                }

                //wait for DOM to update before calling calclulate_grades()
                setTimeout(calculate_grades(), 0);
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
        element.style.paddingTop = '0.35rem';
        element.style.paddingBottom = '0.35rem';
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
                element.innerHTML = `<input type="hidden" id="${element.className}_category_num" value="${e.options[e.selectedIndex].value}"></input>` + e.options[e.selectedIndex].text;
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
                calculate_grades();
            } else {
                console.log("Unable to save");
            }
        }
    });


}


//for sorting the drop array
function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] < b[0]) ? -1 : 1;
    }
}

function calculate_grades() {
    console.log("called");
    let rows = document.getElementsByClassName("num-row");
    for (let row of rows) {
        //points earned
        let earned = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
        };
        //points total
        let total = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
        };

        let cur_drop = {
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[],
            8:[],
        };
        
        let grades = row.children;
        console.log(grades.length);
        grades = Array.prototype.slice.call(grades, 2, grades.length - 2);
        for (let grade of grades) {
            if (grade.innerText) {
                let assignment_id = parseInt(grade.className.split('_')[1]);
                let category_num = parseInt(document.getElementById("assignment_" + assignment_id + "_category_num").value);
                let assignment_total = parseFloat(document.getElementById("assignment_" + assignment_id + "_points").innerText);
                let points_earned = parseFloat(grade.innerText);

                earned[category_num] += points_earned;
                total[category_num] += assignment_total;
                
                //drop or not
                if (drop[category_num] > 0) {
                    //check if cur_drop is at capacity
                    if (cur_drop[category_num].length < drop[category_num]) {
                        cur_drop[category_num].push([points_earned / assignment_total, points_earned, assignment_total]);
                    } else if ((points_earned / assignment_total) < cur_drop[category_num][cur_drop[category_num].length - 1][0]) {
                        cur_drop[category_num].pop();
                        cur_drop[category_num].push([points_earned / assignment_total, points_earned, assignment_total]);
                        cur_drop[category_num].sort(sortFunction);
                    }
                }
            }
        }

        //calculate total
        let total_weight = 0;
        let grade_total = 0;

        for (let i = 1; i <= 8; i++) {
            //drop from category i
            for (let val of cur_drop[i]) {
                earned[i] -= val[1];
                total[i] -= val[2];
            }

            //if category total is not 0, then add category to grade total
            if (total[i] > Number.EPSILON) {
                grade_total += earned[i] / total[i] * weights[i];
                total_weight += weights[i];
            }
        }


        grade_total = (grade_total / total_weight * 100).toFixed(2);
        
        //set grade letter
        let grade_letter_element = row.children[1].children[0];
        if (grade_total >= a) {
            grade_letter_element.innerText = "A";
        } else if (grade_total >= b) {
            grade_letter_element.innerText = "B";
        } else if (grade_total >= c) {
            grade_letter_element.innerText = "C";
        } else if (grade_total >= d) {
            grade_letter_element.innerText = "D";
        } else {
            grade_letter_element.innerText = "F";
        }

        //set grade total
        row.children[1].children[1].innerText = grade_total;
    }
}
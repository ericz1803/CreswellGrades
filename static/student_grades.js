//points earned
var earned = {};
//points total
var total = {};
//grade factor
var weights = {};
//lowest grades
var drop = {};
//grade scale
var a, b, c, d;

document.onload = get_grade();
document.onload = calculate_grades();

function get_grade() {
    //grade scale
    a = parseFloat(document.getElementById("a").value);
    b = parseFloat(document.getElementById("b").value);
    c = parseFloat(document.getElementById("c").value);
    d = parseFloat(document.getElementById("d").value);
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
    tables = document.getElementsByTagName("tbody");
    for (let table of tables) {
        //get category num
        let category = table.className.split('_')[1];
        //get category weight
        let weight = document.getElementById('category_value_' + category).value;
        //get number of assingments dropped
        let drop_num = document.getElementById('category_drop_' + category).value;

        earned[category] = 0
        total[category] = 0
        weights[category] = parseFloat(weight);
        drop[category] = [];

        //extract numbers from table
        for (let row of table.children) {
            let points_earned = parseFloat(row.children[2].innerText);
            let points_total = parseFloat(row.children[3].innerText);
            
            //only add to grade calculation if student grade exists
            if (points_earned || points_earned == 0) {
                row.children[4].innerText = (points_earned / points_total * 100).toFixed(2);
                earned[category] += points_earned;
                total[category] += points_total;
                
                //drop or not
                if (drop_num > 0) {
                    if (drop[category].length < drop_num) {
                        drop[category].push([points_earned / points_total, row.id]);
                    } else if ((points_earned / points_total) < drop[category][drop[category].length - 1][0]) {
                        drop[category].pop();
                        drop[category].push([points_earned / points_total, row.id]);
                        drop[category].sort(sortFunction);
                    }
                }
            }
        }
        for (let arr of drop[category]) {
            let row = document.getElementById(arr[1]);
            earned[category] -= parseFloat(row.children[2].innerText);
            total[category] -= parseFloat(row.children[3].innerText);
            row.children[0].innerHTML += ' <span data-toggle="tooltip" data-placement="top" title="dropped" class="badge badge-warning"><i class="fas fa-asterisk"></i></span>';
        }
        //calculate category totals
        let cat_pct = (earned[category] / total[category] * 100).toFixed(2);
        document.getElementById('category_' + category + '_total_points').innerText = earned[category];
        document.getElementById('category_' + category + '_total_earned').innerText = total[category];
        document.getElementById('category_' + category + '_total_percentage').innerText = cat_pct;
    }

    //calculate total
    let total_weight = 0;
    let grade_total = 0;

    for (let k of Object.keys(earned)) {
        if (total[k] > 0) {
            grade_total += earned[k] / total[k] * weights[k];
            total_weight += weights[k];
        }
    }

    grade_total = (grade_total / total_weight * 100).toFixed(2);

    console.log(grade_total);
    document.getElementById("grade-pct").innerText = grade_total;

    
    if (grade_total >= a) {
        document.getElementById("grade-letter").innerText = "A";
    } else if (grade_total >= b) {
        document.getElementById("grade-letter").innerText = "B";
    } else if (grade_total >= c) {
        document.getElementById("grade-letter").innerText = "C";
    } else if (grade_total >= d) {
        document.getElementById("grade-letter").innerText = "D";
    } else {
        document.getElementById("grade-letter").innerText = "F";
    }
}
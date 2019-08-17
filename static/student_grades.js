//points earned
var earned = {};
//points total
var total = {};
//grade factor
var weights = {};

document.onload = calculate_grades();

function calculate_grades() {
    tables = document.getElementsByTagName("tbody");
    for (let table of tables) {
        //get category num
        let category = table.className.split('_')[1];
        //get category weight
        let weight = document.getElementById('category_value_' + category).value;
        
        earned[category] = 0
        total[category] = 0
        weights[category] = parseFloat(weight);

        //extract numbers from table
        for (let row of table.children) {
            let points_earned = parseFloat(row.children[2].innerText);
            let points_total = parseFloat(row.children[3].innerText);

            //only add to grade calculation if student grade exists
            if (points_earned) {
                row.children[4].innerText = (points_earned / points_total * 100).toFixed(2);
                earned[category] += points_earned;
                total[category] += points_total;
            }
        }

        //calculate category totals
        let cat_pct = (earned[category] / total[category] * 100).toFixed(2);
        document.getElementById('category_' + category + '_total_points').innerText = earned[category];
        document.getElementById('category_' + category + '_total_earned').innerText = total[category];
        document.getElementById('category_' + category + '_total_percentage').innerText = cat_pct;
    }

    //calculate total
    console.log(earned);
    console.log(total);
    console.log(weights);

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
}
//https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript
function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

//randomly assign a class code on page startup
window.onload = function () {
    document.getElementById("join_code").value = makeid(16);
};

document.getElementById("reroll").addEventListener("click", function () {
    document.getElementById("join_code").value = makeid(16);
});

document.getElementById("add-new-category").addEventListener("click", function () {
    console.log("new category");
    if (document.getElementById("category8")) {
        alert("Maximum of 8 categories.")
        return;
    }

    for (var i=1; i<=8; i++) {
        var element = document.getElementById("category" + i);
        if (element) {
            continue;
        } else {
            var div = document.createElement('div');
            div.setAttribute('class', 'form-group row')
            div.setAttribute('id', 'category' + i)
            div.innerHTML = `
            <div class="col">
                <label for="category_name${i}">Category ${i} Name</label>
                <input type="text" class="form-control" id="category_name${i}" name="category_name${i}" required>
            </div>
            <div class="col-3">
                <label for="category_value${i}">Category ${i} Value (%)</label>
                <input type="number" class="form-control" id="category_value${i}" name="category_value${i}" min="1" max="100" required>
            </div>
            <div class="col-3">
                <label for="category_drop${i}">Category ${i} Drop Lowest</label>
                <input type="number" class="form-control" id="category_drop${i}" name="category_drop${i}" min="0" value=0 required>
            </div>
            `;
            document.getElementById('categories').appendChild(div);
            break;
        }
    }
});



document.getElementById("remove-category").addEventListener("click", function () {
    for (var i=8; i>1; i--) {
        var element = document.getElementById("category" + i);
        if (element) {
            document.getElementById("categories").removeChild(element);
            return;
        }
    }
    alert("At least 1 category required.")
});
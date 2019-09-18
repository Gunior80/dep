
document.addEventListener("DOMContentLoaded", function(event) {
    let parent = document.getElementById("id_departament");
    if (parent != null) {
        let elems = parent.children;
        let count = elems.length;
        for (let i = 0; i < elems.length; i++) {
            if (elems[i].children[0].children[0].checked === false) {
                count = count - 1;
            }
        }
        if (count === 0) {
            elems[0].children[0].children[0].checked = true;
        }
    }
    let is_staff = document.getElementById("id_is_staff");
    let pub = document.getElementById("id_public");
    if ((is_staff != null) && (pub != null)) {
        is_staff.onclick = function (){
            if (is_staff.checked === true) {
                pub.checked = false;
            }
        };
        pub.onclick = function (){
            if (pub.checked === true) {
                is_staff.checked = false;
            }
        };
    }
});

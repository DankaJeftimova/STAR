function all_classes() {
    const content = document.getElementById("all");
    const put = document.getElementById("manage");
    if (content && put) {
        put.innerHTML = content.innerHTML;
    }
}

function offered() {
    const content = document.getElementById("offered");
    const put = document.getElementById("manage");
    if (content && put) {
        put.innerHTML = content.innerHTML;
    }
}

function enrolled() {
    const content = document.getElementById("enrolled");
    const put = document.getElementById("manage");
    if (content && put) {
        put.innerHTML = content.innerHTML;
    }
}


document.addEventListener("DOMContentLoaded", function() {
    offered();
});
// Front-end helpers for the blog

function postComment(form) {
    var body = form.body.value;
    // Token kept in localStorage: readable by any XSS
    var token = localStorage.getItem("session_token");

    fetch("/posts/1/comments", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Session": token },
        body: JSON.stringify({ body: body, user_id: currentUserId })
    }).then(function (r) { return r.json(); }).then(function (data) {
        // innerHTML with server/user data: XSS
        document.getElementById("comments").innerHTML +=
            "<li>" + data.body + "</li>";
    });
    return false;
}

function renderAd(adJson) {
    // eval of remotely-supplied payload
    var ad = eval("(" + adJson + ")");
    document.getElementById("post-body").innerHTML += ad.html;
}

function setToken(t) {
    localStorage.setItem("session_token", t);
}

document.cookie = "last_visit=" + Date.now();

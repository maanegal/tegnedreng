var read = document.getElementById('read');
var btn = document.getElementById('scrollBtn');

btn.addEventListener('click', function() {
    //scrollTo(document.body, read.offsetTop, 125);
    read.scrollIntoView({behavior: "smooth"});
});


var startReadingBtn = document.getElementById('startReading');
startReadingBtn.addEventListener('click', function() {
    setCookie('cookie_consent', "true", 365);
});

var bm = getBookmark();
if (bm && bm != "off") {
    document.getElementById('bookmarkBtn').addEventListener('click', function() {
        // naviger til element
        bm = getBookmark();
        location = "/kapitel/" + bm[0] + "/#" + bm[1];
    });
}

document.getElementById("commentOffs").addEventListener("click", setCommentPrefs);
document.getElementById("commentOns").addEventListener("click", setCommentPrefs);
document.getElementById("commentToggles").addEventListener("click", setCommentPrefs);

function setCommentPrefs() {
    var comOn = document.getElementById('commentOns');
    var comOff = document.getElementById('commentOffs');
    var comTog = document.getElementById('commentToggles');
    if (comOn.checked) {
        setCookie('show_comments', 'on', 30);
    } else if (comOff.checked) {
        setCookie('show_comments', 'off', 30);
    } else {
        setCookie('show_comments', 'toggle', 30);
    }
}

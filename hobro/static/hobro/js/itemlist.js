bm = getBookmark(); // get bookmark value from cookie
if (bm != "off") {
if (!continued) {
    var bookBanner = document.getElementById('bookmark-banner');
    var bookNote = document.getElementById('bookmark-note');
    var bookBtn = document.getElementById('bookmark-go');
    var bookOff = document.getElementById('bookmark-off');
    var bookOffNote = document.getElementById('bookmark-off-note');

    // 'delete' button
    document.getElementById('bookmark-hide').addEventListener('click', function() { bookBanner.classList.remove('is-active'); });

    // 'Turn off' button
    bookOff.addEventListener('click', function() {
        bookBanner.classList.remove('is-active');
        setCookie('bookmark', "off", 14);
        document.getElementById("switchBook").checked = false;
        bookOffNote.classList.add('is-active');
        setTimeout(function(){
            bookOffNote.classList.remove('is-active');
        },6000);
    });

    // 'Go to' button
    bookBtn.addEventListener('click', function() {
        // naviger til element
        bm = getBookmark();
        bookBanner.classList.remove('is-active');
        location = "/kapitel/" + bm[0] + "/#" + bm[1];
    });

    // Initial notification click
    bookNote.addEventListener('click', function() {
        bookNote.classList.remove('is-active');
        bookBanner.classList.add('is-active');
    });

    // Initial notification appearance
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(function(){
            if (getBookmark()) {
                bookNote.classList.add('is-active');
            }
        },2800);
    });
};


    // following is for saving bookmark
    if (bm) { var cur = bm[1]; } else { var cur = 0; }

    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.intersectionRatio > 0) {
          var val = entry.target.id;
          if (/^\d+$/.test(val) && val > +cur ) { //is a number and bigger than cur (as number)
            setCookie('bookmark', number + '/' + val, 14);
            cur = val; // update current bookmark variable
          }
          observer.unobserve(entry.target);
        }
      });
    });

     // if bookmark is not turned off, make observer
    const elems = document.querySelectorAll('article');
    elems.forEach(elem => {
      observer.observe(elem);
    });
}

const sectionP = document.querySelector('section');
const sectionAfter = document.querySelectorAll('.section-flag');

sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.intersectionRatio > 0) {
      sectionP.classList.remove('make-transparent');
    } else {
      sectionP.classList.add('make-transparent');
    }
  });
});

sectionAfter.forEach(elem => {
  sectionObserver.observe(elem);
});

window.onscroll = function() {scrollPosition()};
function scrollPosition() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("theProgressBar").style.width = scrolled + "%";
}

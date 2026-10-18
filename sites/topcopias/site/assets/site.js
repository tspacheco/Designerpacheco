(function () {
  "use strict";
  var cab = document.querySelector(".cab"), btn = document.querySelector(".menu-btn");
  if (btn) btn.addEventListener("click", function () {
    var a = cab.classList.toggle("abierto");
    btn.setAttribute("aria-expanded", a ? "true" : "false");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && cab.classList.contains("abierto")) { cab.classList.remove("abierto"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
  });
  Array.prototype.forEach.call(document.querySelectorAll(".nav a"), function (a) {
    a.addEventListener("click", function () { cab.classList.remove("abierto"); if (btn) btn.setAttribute("aria-expanded", "false"); });
  });
})();

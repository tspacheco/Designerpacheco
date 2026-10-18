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

  /* Relieve 3D: las tarjetas se inclinan hacia el ratón (solo con puntero fino) */
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    Array.prototype.forEach.call(document.querySelectorAll(".serv, .paso, .tienda"), function (el) {
      el.setAttribute("data-tilt", "");
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "rotateX(" + (-y * 7) + "deg) rotateY(" + (x * 9) + "deg) translateZ(10px)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
  }
})();

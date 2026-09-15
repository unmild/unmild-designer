// Unmild Designer marketing site — small UI polish only, nothing load-bearing.
(function () {
  "use strict";

  // Footer year
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mobile nav toggle
  var toggle = document.getElementById("navToggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Screenshot lightbox — click any framed screenshot to zoom in.
  var shots = document.querySelectorAll(".shot img");
  if (shots.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Enlarged screenshot");
    lb.innerHTML =
      '<button class="lightbox-close" type="button" aria-label="Close">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
      "</button>" +
      '<img alt="">';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector("img");
    var lbClose = lb.querySelector(".lightbox-close");

    function openLightbox(src, alt) {
      lbImg.src = src;
      lbImg.alt = alt || "";
      lb.classList.add("is-open");
      lbClose.focus();
      document.documentElement.style.overflow = "hidden";
    }
    function closeLightbox() {
      lb.classList.remove("is-open");
      lbImg.src = "";
      document.documentElement.style.overflow = "";
    }
    lb.addEventListener("click", function (e) {
      if (e.target === lb) closeLightbox();
    });
    lbClose.addEventListener("click", closeLightbox);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && lb.classList.contains("is-open")) closeLightbox();
    });

    shots.forEach(function (img) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "shot-btn";
      img.parentNode.insertBefore(btn, img);
      btn.appendChild(img);
      btn.setAttribute("aria-label", "Enlarge screenshot: " + (img.alt || ""));
      btn.addEventListener("click", function () {
        openLightbox(img.currentSrc || img.src, img.alt);
      });
    });
  }
})();

document.addEventListener("DOMContentLoaded", () => {
  // --- Scroll reveal: add .in-view to .reveal elements as they enter viewport ---
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => observer.observe(el));
  } else {
    // No IntersectionObserver support: show everything immediately
    revealEls.forEach((el) => el.classList.add("in-view"));
  }

  // --- Auto-stagger: number the children of any .stagger container ---
  document.querySelectorAll(".stagger").forEach((group) => {
    Array.from(group.children).forEach((child, i) => {
      child.style.setProperty("--i", i);
    });
  });

  // --- Animate table rows in, staggered ---
  document.querySelectorAll("table.table tbody").forEach((tbody) => {
    Array.from(tbody.rows).forEach((row, i) => {
      // cap the delay so long tables don't take forever
      row.style.setProperty("--i", Math.min(i, 15));
      row.classList.add("row-enter");
    });
  });
});

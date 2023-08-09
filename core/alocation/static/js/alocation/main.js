
// navbar focus
window.addEventListener("load", (e) => {
    if (window.location.href.includes("renters/")) {
        document.querySelector("nav ul li").classList.toggle("selected")
    } else if (window.location.href.includes("locals/")) {
        document.querySelector("nav ul li:last-child").classList.toggle("selected")
    }
})

// search input focus
window.addEventListener("load", (e) => {
    const searchInput = document.querySelector("input[name=search-query]")
    if ( searchInput.value !== "") {
        const end = searchInput.value.length

        searchInput.setSelectionRange(end, end)
        searchInput.focus()
    }
})


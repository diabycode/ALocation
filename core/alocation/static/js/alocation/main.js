
// pagination
document.querySelectorAll(".pagination div.disable a").forEach((element) => {
    element.addEventListener("click", (e) => {
        e.preventDefault()
    })
})


// search input focus
const FocusSearchInput = () => {
    const searchInput = document.querySelector("input[name=search-query]")
    if ( searchInput.value !== "") {
        const end = searchInput.value.length

        searchInput.setSelectionRange(end, end)
        searchInput.focus()
    }
}


// navbar focus
const navbarFocus = (e) => {
    if (window.location.href.includes("renters/")) {
        document.querySelector("nav ul li").classList.toggle("selected")
    } else if (window.location.href.includes("locals/")) {
        document.querySelector("nav ul li:last-child").classList.toggle("selected")
    }
}


// On page is loaded
window.addEventListener("load", () => {
    FocusSearchInput()
    navbarFocus()
})


// user dropdown
document.querySelector(".profile-head").addEventListener("click", () => {
    document.querySelector("header .dropdown").classList.toggle("show")
})


// open filter options
document.querySelector(".filter-btn").addEventListener("click", () => {
    document.querySelector(".filter-options").classList.toggle("active")
})


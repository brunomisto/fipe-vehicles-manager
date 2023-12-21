const listsElement = document.querySelector("#lists");

fetch("/lists")
.then(response => response.json())
.then(result => {
    result.lists.forEach(list => {
        const listElement = document.createElement("li");
        listElement.innerText = list;
        listsElement.appendChild(listElement);
    });
})
.catch(error => {
    alert("An error occurred while loading your lists.")
});    
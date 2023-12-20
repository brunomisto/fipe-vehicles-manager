const listsElement = document.querySelector("#lists");

fetch("/lists")
.then(response => response.json())
.then(result => {
    result.lists.forEach(list => {
        const listElement = document.createElement("a");
        listElement.innerText = list;
        listsElement.appendChild(listElement);
    });
})
.catch(error => console.log(error));    
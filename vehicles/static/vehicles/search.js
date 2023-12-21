const api = "https://parallelum.com.br/fipe/api/v2";

const vehicleTypeSelect = document.querySelector("#vehicle-type");
const brandIdSelect = document.querySelector("#brand-id");
const modelIdSelect = document.querySelector("#model-id");
const yearIdSelect = document.querySelector("#year-id");
const addVehicleButton = document.querySelector("#add-vehicle");

const selectElements = [vehicleTypeSelect, brandIdSelect, modelIdSelect, yearIdSelect];

let vehicleType, brandId, modelId, yearId;

function updateSelect(path, currentSelect, targetSelect) {
    addVehicleButton.disabled = true;

    currentSelect.disabled = true;
    targetSelect.innerHTML = "";

    // Ensure all next elements are empty
    for (let i = selectElements.indexOf(targetSelect); i < selectElements.length; i++) {
        selectElements[i].innerHTML = "";
    }

    // Create option placeholder
    const startingOption = document.createElement("option");
    startingOption.selected = true;
    startingOption.disabled = true;
    startingOption.innerText = "Select one";
    targetSelect.appendChild(startingOption);

    // Fetch data
    fetch(api + path)
    .then(response => response.json())
    .then(result => {
        // Populate targetSelect
        for (const object of result) {
            const objectElement = document.createElement("option");
            objectElement.innerText = object.name;
            objectElement.value = object.code;
            targetSelect.appendChild(objectElement);
        }
        currentSelect.disabled = false;
    })
    .catch(error => {
        // Reset form and alert user
        selectElements[0].disabled = false;
        selectElements[0].childNodes[1].selected = true; // This selects the first option
        for (let i = 1; i < selectElements.length; i++) {
            selectElements[i].innerHTML = "";
            selectElements[i].disabled = false;
        }
        alert("The system failed to fetch FIPE api data, try again.");
    });
}

function updateSelectValues() {
    vehicleType = vehicleTypeSelect.value;
    brandId = brandIdSelect.value;
    modelId = modelIdSelect.value;
    yearId = yearIdSelect.value;
}

vehicleTypeSelect.addEventListener("input", () => {
    updateSelectValues();
    updateSelect(`/${vehicleType}/brands`, vehicleTypeSelect, brandIdSelect);
});

brandIdSelect.addEventListener("input", () => {
    updateSelectValues();
    updateSelect(`/${vehicleType}/brands/${brandId}/models`, brandIdSelect, modelIdSelect);
});

modelIdSelect.addEventListener("input", () => {
    updateSelectValues();
    updateSelect(`/${vehicleType}/brands/${brandId}/models/${modelId}/years`, modelIdSelect, yearIdSelect);
});

yearIdSelect.addEventListener("input", () => {
    updateSelectValues();
    addVehicleButton.disabled = false;
});
const pElem = document.getElementById("p");
const aElem = document.getElementById("a");
const bElem = document.getElementById("b");
const PxElem = document.getElementById("Px");
const PyElem = document.getElementById("Py");
const sElem = document.getElementById("s");

const curveFormationOptionSelector = document.getElementById("curve-options");
const generateNewCurveButton = document.getElementById("generatecurvebutton");
const predefinedCurveSelector = document.getElementById("predefined-curve-selector");

const generateCurveArea = document.getElementById("generatecurvearea");
const numBitsPElem = document.getElementById("new-curve-p-bits");

const curveFormationLogArea = document.getElementById("log-area-curveformation");
const curveFormationErrorArea = document.getElementById("error-area-curveformation");
const curveFormationLoaderArea = document.getElementById("loader-area-curveformation");

const step1LogArea = document.getElementById("log-area-step1");
const step1ErrorArea = document.getElementById("error-area-step1");
const step1LoaderArea = document.getElementById("loader-area-step1");

const step1To2Button = document.getElementById("step1to2button");
const BxElem = document.getElementById("Bx");
const ByElem = document.getElementById("By");

const kElem = document.getElementById("k");
const messageInputTypeSelector = document.getElementById("input-type-selector");
const textInputArea = document.getElementById("text-input-area");
const textInputField = document.getElementById("message-as-text-to-encrypt");
const pointInputArea = document.getElementById("point-input-area");
const pointInputFieldX = document.getElementById("Mx");
const pointInputFieldY = document.getElementById("My");
const leftPadEncryptElem = document.getElementById("left-pad-encrypt");
const rightPadEncryptElem = document.getElementById("right-pad-encrypt");
const encryptButton = document.getElementById("encrypt-button");

const MBeforeEncryptionElem = document.getElementById("M-value-before-encryption");
const encryptedM1Elem = document.getElementById("encrypted-M1-value");
const encryptedM2Elem = document.getElementById("encrypted-M2-value");

const M1XElem = document.getElementById("M1x");
const M1YElem = document.getElementById("M1y");
const M2XElem = document.getElementById("M2x");
const M2YElem = document.getElementById("M2y");
const leftPadDecryptElem = document.getElementById("left-pad-decrypt");
const rightPadDecryptElem = document.getElementById("right-pad-decrypt");
const decryptButton = document.getElementById("decrypt-button");

const sM1Elem = document.getElementById("sM1");
const MAfterDecryptionElem = document.getElementById("decrypted-M-value");
const decryptedIntegerElem = document.getElementById("decrypted-m");
const decryptedTextElem = document.getElementById("decrypted-m-text");

curveFormationOptionSelector.addEventListener("change", function(event) {
    for (const area of [step1LogArea, step1ErrorArea, step1LoaderArea]) {
        area.innerHTML = "";
    }

    const option = event.target.value;

    for (const area of [curveFormationLogArea, curveFormationErrorArea, curveFormationLoaderArea]) {
        area.innerHTML = "";
    }

    if (option === "input-yourself") {
        predefinedCurveSelector.classList.add("hidden");
        generateCurveArea.classList.add("hidden");
        for (const elem of [pElem, aElem, bElem, PxElem, PyElem, sElem]) {
            elem.disabled = false;
            elem.readOnly = false;
        }
    } else if (option === "predefined-curve") {
        predefinedCurveSelector.classList.remove("hidden");
        generateCurveArea.classList.add("hidden");
        selectPredefinedCurve(predefinedCurveSelector.value);
    } else if (option === "generate-new") {
        predefinedCurveSelector.classList.add("hidden");
        numBitsPElem.value = "";
        generateCurveArea.classList.remove("hidden");
        numBitsPElem.disabled = false;
    }
});

generateNewCurveButton.addEventListener("click", function() {
    generateNewCurve();
});

async function generateNewCurve() {
    for (const elem of [
        pElem, aElem, bElem, PxElem, PyElem,
    ]) {
        elem.value = "";
        elem.disabled = true;
        elem.readOnly = true;
    }
    numBitsPElem.disabled = true;

    const numBitsP = numBitsPElem.value;
    const validator = async () => {
        if (!isNumberValid(numBitsP) || numBitsP.startsWith("-")) {
            throw new Error("Invalid number of bits for p");
        }
    };

    try {
        const res = await callAPIFull(validator, "ECGenerate", `${numBitsP}`, "loader-area-curveformation", "error-area-curveformation", "log-area-curveformation", "Generating new curve...");
        if (null === res) return;

        const [p, a, b, Px, Py, s] = res.output.split(',');

        pElem.value = p;
        aElem.value = a;
        bElem.value = b;
        PxElem.value = Px;
        PyElem.value = Py;
        sElem.value = s;
    } finally {
        for (const elem of [
            numBitsPElem,
            pElem, aElem, bElem, PxElem, PyElem, sElem,
        ]) {
            elem.disabled = false;
        }
    }
}

async function selectPredefinedCurve(curveName) {
    for (const elem of [pElem, aElem, bElem, PxElem, PyElem]) {
        elem.value = "";
        elem.disabled = true;
        elem.readOnly = true;
    }

    const validator = async () => {};

    try {
        const res = await callAPIFull(validator, "ECSelectPredefined", `${curveName}`, "loader-area-curveformation", "error-area-curveformation", "log-area-curveformation", "Selecting predefined curve...");
        if (null === res) return;

        const [p, a, b, Px, Py, s] = res.output.split(',');
        pElem.value = p;
        aElem.value = a;
        bElem.value = b;
        PxElem.value = Px;
        PyElem.value = Py;
        sElem.value = s;
    } finally {
        for (const elem of [pElem, aElem, bElem, PxElem, PyElem, sElem]) {
            elem.disabled = false;
        }
    }
}

predefinedCurveSelector.addEventListener("change", function(event) {
    const curveName = event.target.value;
    selectPredefinedCurve(curveName);
});

messageInputTypeSelector.addEventListener("change", function(event) {
    const selectedType = event.target.value;

    textInputField.value = "";
    pointInputFieldX.value = "";
    pointInputFieldY.value = "";

    if (selectedType === "point") {
        textInputArea.style.display = "none";
        pointInputArea.style.display = "block";
    } else if (selectedType === "text") {
        textInputArea.style.display = "block";
        pointInputArea.style.display = "none";
    }
});

step1To2Button.addEventListener("click", async function() {
    step1To2Button.disabled = true;

    const INPUT_ELEMS = [pElem, aElem, bElem, PxElem, PyElem, sElem];

    const inputElemStates = INPUT_ELEMS.map(elem => ({ elem, disabled: elem.disabled, readOnly: elem.readOnly }));

    const validator = async () => {
        for (const elem of INPUT_ELEMS) {
            if (!isNumberValid(elem.value)) {
                throw new Error("Please enter valid numbers above.");
            }
        }
    };

    const p = pElem.value;
    const a = aElem.value;
    const b = bElem.value;
    const Px = PxElem.value;
    const Py = PyElem.value;
    const s = sElem.value;

    let validated = false;
    try {
        const res = await callAPIFull(validator, "ECValidate", `${p},${a},${b},${Px},${Py},${s}`, "loader-area-step1", "error-area-step1", "log-area-step1", "Validating curve parameters...");
        if (res === null) {
            return;
        }

        const [Bx, By] = res.output.split(',');
        BxElem.value = Bx;
        ByElem.value = By;

        for (const elem of INPUT_ELEMS) {
            elem.disabled = true;
        }
        step1To2Button.disabled = true;
        for (const e of [curveFormationOptionSelector, generateNewCurveButton, predefinedCurveSelector, numBitsPElem]) {
            e.disabled = true;
        }

        for (const e of [
            kElem, messageInputTypeSelector, textInputField, pointInputFieldX, pointInputFieldY, encryptButton,
            leftPadEncryptElem, rightPadEncryptElem,
            M1XElem, M1YElem, M2XElem, M2YElem, decryptButton,
            leftPadDecryptElem, rightPadDecryptElem,
        ]) {
            e.disabled = false;
        }

        validated = true;
    } finally {
        if (!validated) {
            step1To2Button.disabled = false;
            for (const { elem, disabled, readOnly } of inputElemStates) {
                elem.disabled = disabled;
                elem.readOnly = readOnly;
            }
        }
    }
});

encryptButton.addEventListener("click", async function() {
    const p = pElem.value;
    const a = aElem.value;
    const b = bElem.value;
    const k = kElem.value;
    const Px = PxElem.value;
    const Py = PyElem.value;
    const Bx = BxElem.value;
    const By = ByElem.value;
    const INPUT_ELEMS = [kElem, messageInputTypeSelector, textInputField, pointInputFieldX, pointInputFieldY, leftPadEncryptElem, rightPadEncryptElem, encryptButton];

    for (const elem of INPUT_ELEMS) {
        elem.disabled = true;
    }

    let payload;
    const Mx = pointInputFieldX.value;
    const My = pointInputFieldY.value;
    const leftpad = leftPadEncryptElem.value;
    const rightpad = rightPadEncryptElem.value;

    if (messageInputTypeSelector.value === "text") {
        payload = {
            p, a, b, Px, Py, Bx, By, k, leftpad, rightpad,
            type: "text",
            value: textInputField.value,
        };
    } else {
        payload = {
            p, a, b, Px, Py, Bx, By, k,
            type: "point",
            value: `${Mx},${My}`,
        };
    }

    const validator = async () => {
        if (messageInputTypeSelector.value === "text" && !textInputField.value) {
            throw new Error("Please enter a message to encrypt.");
        }
        if (messageInputTypeSelector.value === "point" && (!isNumberValid(Mx) || !isNumberValid(My))) {
            throw new Error("Please enter a valid point to encrypt.");
        }
        if (!isNumberValid(k)) {
            throw new Error("Please enter a valid k value.");
        }
        if (messageInputTypeSelector.value === "text" && (!isNumberValid(leftpad) || !isNumberValid(rightpad))) {
            throw new Error("Please enter valid padding values.");
        }
    };

    try {
        const res = await callAPIFull(validator, "ECElGamalEncrypt", JSON.stringify(payload), "loader-area-encrypt", "error-area-encrypt", "log-area-encrypt", "Encrypting message...");
        if (res === null) return;

        const [Mx, My, M1x, M1y, M2x, M2y] = res.output.split(',');

        MBeforeEncryptionElem.value = `(${Mx}, ${My})`;
        encryptedM1Elem.value = `(${M1x}, ${M1y})`;
        encryptedM2Elem.value = `(${M2x}, ${M2y})`;
    } finally {
        for (const elem of INPUT_ELEMS) {
            elem.disabled = false;
        }
    }
});

decryptButton.addEventListener("click", async function() {
    const p = pElem.value;
    const a = aElem.value;
    const b = bElem.value;
    const Px = PxElem.value;
    const Py = PyElem.value;
    const s = sElem.value;
    const INPUT_ELEMS = [M1XElem, M1YElem, M2XElem, M2YElem, decryptButton];

    for (const elem of INPUT_ELEMS) {
        elem.disabled = true;
    }

    const M1x = M1XElem.value;
    const M1y = M1YElem.value;
    const M2x = M2XElem.value;
    const M2y = M2YElem.value;

    const leftpad = leftPadDecryptElem.value;
    const rightpad = rightPadDecryptElem.value;

    const validator = async () => {
        if (!isNumberValid(M1x) || !isNumberValid(M1y) || !isNumberValid(M2x) || !isNumberValid(M2y)) {
            throw new Error("Please enter valid points to decrypt.");
        }

        if (!isNumberValid(leftpad) || !isNumberValid(rightpad)) {
            throw new Error("Please enter valid padding values. If you don't want to use padding, e.g. just want the point coordinates rather than a text message, enter 0 for both padding values.");
        }
    };

    try {
        const res = await callAPIFull(validator, "ECElGamalDecrypt", `${p},${a},${b},${Px},${Py},${s},${M1x},${M1y},${M2x},${M2y},${leftpad},${rightpad}`, "loader-area-decrypt", "error-area-decrypt", "log-area-decrypt", "Decrypting message...");
        if (res === null) return;

        const [sM1x, sM1y, Mx, My, m, mText] = res.output.split(',');
        sM1Elem.value = `(${sM1x}, ${sM1y})`;
        MAfterDecryptionElem.value = `(${Mx}, ${My})`;
        decryptedIntegerElem.value = m;
        decryptedTextElem.value = mText;
    } finally {
        for (const elem of INPUT_ELEMS) {
            elem.disabled = false;
        }
    }
});

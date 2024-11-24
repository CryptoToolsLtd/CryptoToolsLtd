const pElem = document.getElementById("p");
const aElem = document.getElementById("a");
const bElem = document.getElementById("b");
const gxElem = document.getElementById("gx");
const gyElem = document.getElementById("gy");
const dElem = document.getElementById("d");

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
const QxElem = document.getElementById("Qx");
const QyElem = document.getElementById("Qy");
const nElem = document.getElementById("n");



const sign_messageInputTypeSelector = document.getElementById("input-type-selector");
const sign_messageInput = document.getElementById("message");
const sign_kInput = document.getElementById("k");
const signButton = document.getElementById("sign-button");
const sign_correspondingMOutput = document.getElementById("corresponding-m");
const sign_x1y1Output = document.getElementById("x1-y1-value");
const sign_rOutput = document.getElementById("r-value");
const sign_hOutput = document.getElementById("h-value");
const sign_sOutput = document.getElementById("s-value");
const sign_signatureOutput = document.getElementById("signature");

const verify_messageNumberInput = document.getElementById("m-input-verify");
const verify_rInput = document.getElementById("r-input");
const verify_sInput = document.getElementById("s-input");
const verifyButton = document.getElementById("verify-button");
const verify_hOutput = document.getElementById("ver-hash-value");
const verify_wOutput = document.getElementById("ver-w-value");
const verify_u1Output = document.getElementById("ver-u1-value");
const verify_u2Output = document.getElementById("ver-u2-value");
const verify_x0y0Output = document.getElementById("ver-x0-y0-value");
const verify_vOutput = document.getElementById("ver-v-value");
const verificationResultOutput = document.getElementById("verification-result");

SIGN_AND_VERIFY_INPUT_ELEMS = [
    sign_messageInputTypeSelector,
    sign_messageInput,
    sign_kInput,
    signButton,

    verify_messageNumberInput,
    verify_rInput,
    verify_sInput,
    verifyButton,
];

function changeInputType() {
    const selectedType = sign_messageInputTypeSelector.value;

    if (selectedType === "number") {
        sign_messageInput.value = "";
        sign_messageInput.placeholder = "Enter number";
    } else if (selectedType === "text") {
        sign_messageInput.placeholder = "Enter text";
        sign_messageInput.value = "";
    }
}

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
        for (const elem of [pElem, aElem, bElem, gxElem, gyElem, dElem]) {
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
        pElem, aElem, bElem, gxElem, gyElem,
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
        gxElem.value = Px;
        gyElem.value = Py;
        dElem.value = s;
    } finally {
        for (const elem of [
            numBitsPElem,
            pElem, aElem, bElem, gxElem, gyElem, dElem,
        ]) {
            elem.disabled = false;
        }
    }
}

async function selectPredefinedCurve(curveName) {
    for (const elem of [pElem, aElem, bElem, gxElem, gyElem]) {
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
        gxElem.value = Px;
        gyElem.value = Py;
        dElem.value = s;
    } finally {
        for (const elem of [pElem, aElem, bElem, gxElem, gyElem, dElem]) {
            elem.disabled = false;
        }
    }
}

predefinedCurveSelector.addEventListener("change", function(event) {
    const curveName = event.target.value;
    selectPredefinedCurve(curveName);
});

sign_messageInputTypeSelector.addEventListener("change", function(event) {
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

    const INPUT_ELEMS = [pElem, aElem, bElem, gxElem, gyElem, dElem];

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
    const gx = gxElem.value;
    const gy = gyElem.value;
    const s = dElem.value;

    let validated = false;
    try {
        const res = await callAPIFull(validator, "ECValidate", `${p},${a},${b},${gx},${gy},${s}`, "loader-area-step1", "error-area-step1", "log-area-step1", "Validating curve parameters...");
        if (res === null) {
            return;
        }

        const [Qx, Qy] = res.output.split(',');
        QxElem.value = Qx;
        QyElem.value = Qy;

        for (const elem of INPUT_ELEMS) {
            elem.disabled = true;
        }
        step1To2Button.disabled = true;
        for (const e of [curveFormationOptionSelector, generateNewCurveButton, predefinedCurveSelector, numBitsPElem]) {
            e.disabled = true;
        }

        for (const e of SIGN_AND_VERIFY_INPUT_ELEMS) {
            e.disabled = false;
        }

        const res2 = await callAPIFull(validator, "ECOrderOfPoint", `${p},${a},${b},${gx},${gy},${gx},${gy}`, "loader-area-step1", "error-area-step1", "log-area-step1", "Calculating n, the order of point g...");
        if (res2 === null) {
            return;
        }

        const n = res2.output;
        nElem.value = n;

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

async function signMessage() {
    const INPUT_ELEMS = [
        sign_messageInputTypeSelector,
        sign_messageInput,
        sign_kInput,
        signButton,
    ];

    const p = pElem.value;
    const a = aElem.value;
    const b = bElem.value;
    const k = sign_kInput.value;
    const gx = gxElem.value;
    const gy = gyElem.value;
    const n = nElem.value;
    const d = dElem.value;

    for (const elem of INPUT_ELEMS) {
        elem.disabled = true;
    }

    try {
        /**
         * @type string
         */
        const message = sign_messageInput.value;
        const messageType = sign_messageInputTypeSelector.value === "number" ? "number" : "text";
        const validator = async () => {
            if (message === "") {
                throw new Error("Please enter a message to sign.");
            }

            if (messageType === "text" && message.includes(",")) {
                throw new Error("Please enter a message without commas.");
            }

            if (messageType === "number" && !isNumberValid(message)) {
                throw new Error("Please enter a valid number.");
            }

            if (!isNumberValid(k)) {
                throw new Error("Please enter a valid k value.");
            }
        };

        const res = await callAPIFull(validator, "ECDSASign", `${p},${a},${b},${gx},${gy},${n},${d},${k},${messageType},${message}`, "loader-area-sign", "error-area-sign", "log-area-sign", "Signing message...");
        if (res === null) return;

        const [m, x1, y1, r, h, s] = res.output.split(',');
        sign_correspondingMOutput.value = m;
        sign_x1y1Output.value = `(${x1}, ${y1})`;
        sign_rOutput.value = r;
        sign_hOutput.value = h;
        sign_sOutput.value = s;
        sign_signatureOutput.value = `(${r}, ${s})`;
    } finally {
        for (const elem of INPUT_ELEMS) {
            elem.disabled = false;
        }
    }
};

async function verifySignature() {
    const p = pElem.value;
    const a = aElem.value;
    const b = bElem.value;
    const gx = gxElem.value;
    const gy = gyElem.value;
    const n = nElem.value;
    const Qx = QxElem.value;
    const Qy = QyElem.value;
    const INPUT_ELEMS = [
        verify_messageNumberInput,
        verify_rInput,
        verify_sInput,
        verifyButton,
    ];

    for (const elem of INPUT_ELEMS) {
        elem.disabled = true;
    }

    const m = verify_messageNumberInput.value;
    const r = verify_rInput.value;
    const s = verify_sInput.value;

    const validator = async () => {
        if (!isNumberValid(m) || !isNumberValid(r) || !isNumberValid(s)) {
            throw new Error("Please enter valid numbers.");
        }
    };

    try {
        const res = await callAPIFull(validator, "ECDSAVerify", `${p},${a},${b},${gx},${gy},${n},${Qx},${Qy},${m},${r},${s}`, "loader-area-verify", "error-area-verify", "log-area-verify", "Verifying the signature against the message...");
        if (res === null) return;

        const [h, w, u1, u2, x0, y0, v, verdict] = res.output.split('`');

        verify_hOutput.value = h;
        verify_wOutput.value = w;
        verify_u1Output.value = u1;
        verify_u2Output.value = u2;
        verify_x0y0Output.value = `(${x0}, ${y0})`;
        verify_vOutput.value = v;
        verificationResultOutput.value = verdict;
    } finally {
        for (const elem of INPUT_ELEMS) {
            elem.disabled = false;
        }
    }
}

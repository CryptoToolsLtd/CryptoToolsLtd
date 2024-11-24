function changeInputType() {
    const inputField = document.getElementById("message");
    const selectedType = document.getElementById("input-type-selector").value;

    if (selectedType === "number") {
        inputField.value = "";
        inputField.placeholder = "Enter number";
    } else if (selectedType === "text") {
        inputField.placeholder = "Enter text";
        inputField.value = "";
    }
}

let p_certificate = "";
let certified_p = null;

function setPCertificate(p, cert) {
    p_certificate = cert;
    certified_p = p;
    console.log(`p_certificate: ${p_certificate}, certified_p: ${certified_p}`);
}
function invalidatePCertificate() {
    p_certificate = "";
    certified_p = null;
    console.log(`p_certificate: ${p_certificate}, certified_p: ${certified_p}`);
}

function enableStep1To2Button(enable) {
    if (enable) {
        document.getElementById("step1to2").disabled = false;
    } else {
        document.getElementById("step1to2").disabled = true;
    }
}

function on_p_change(event) {
    const p = event?.target?.value ?? document.getElementById("p").value;
    const enable = (p && document.getElementById("alpha").value && document.getElementById("a").value);
    enableStep1To2Button(enable);
    if (p !== certified_p) {
        invalidatePCertificate();
    }
}
function on_alpha_change(event) {
    const alpha = event?.target?.value ?? document.getElementById("alpha").value;
    const enable = (document.getElementById("p").value && alpha && document.getElementById("a").value);
    enableStep1To2Button(enable);
}
function on_a_change(event) {
    const a = event?.target?.value ?? document.getElementById("a").value;
    const enable = (document.getElementById("p").value && document.getElementById("alpha").value && a);
    enableStep1To2Button(enable);
}

const askNumberOfBits = (promptText, minNumOfBits, maxNumOfBits) => {
    let numberOfBits = parseInt(prompt(promptText));
    for (; ;) {
        if (isNaN(numberOfBits)) return null;
        if (numberOfBits > maxNumOfBits || numberOfBits < minNumOfBits) {
            numberOfBits = parseInt(prompt(`The number of bits must be >= ${minNumOfBits} and <= ${maxNumOfBits}.\n` + promptText));
        }
        return numberOfBits;
    }
};

async function generatestep1all() {
    const pElem = document.getElementById('p');
    const alphaElem = document.getElementById('alpha');
    const aElem = document.getElementById('a');
    const generateStep1AllButton = document.getElementById('generatestep1all');
    const generateStep1AlphaAButton = document.getElementById('generatestep1alphaa');
    const nextStepButton = document.getElementById('step1to2');

    const NEXT_STEP_BUTTON_DISABLED_BEFORE = nextStepButton.disabled;

    pElem.disabled = alphaElem.disabled = aElem.disabled = true;
    generateStep1AllButton.disabled = generateStep1AlphaAButton.disabled = true;
    nextStepButton.disabled = true;

    let generated = false;

    try {
        const numberOfBitsP = askNumberOfBits('Enter the number of bits of the prime number p:', 1, 8192);
        if (null === numberOfBitsP) return;

        const validator = async () => {};

        const res = await callAPIFull(validator, "ElGamalGeneratePAlphaA", `${numberOfBitsP}`, "loader-area-step1", "error-area-step1", "log-area-step1", "Generating p, α and a...");

        if (null === res) return;

        const [p, alpha, a, cert] = res.output.split(',');

        pElem.value = p;
        alphaElem.value = alpha;
        aElem.value = a;
        setPCertificate(p, cert);
        nextStepButton.disabled = false;
        generated = true;
    } finally {
        pElem.disabled = alphaElem.disabled = aElem.disabled = false;
        generateStep1AllButton.disabled = generateStep1AlphaAButton.disabled = false;
        if (!generated) nextStepButton.disabled = NEXT_STEP_BUTTON_DISABLED_BEFORE;
    }
}

async function generatestep1alphaa() {
    const pElem = document.getElementById('p');
    const alphaElem = document.getElementById('alpha');
    const aElem = document.getElementById('a');

    const generateStep1AllButton = document.getElementById('generatestep1all');
    const generateStep1AlphaAButton = document.getElementById('generatestep1alphaa');
    const nextStepButton = document.getElementById('step1to2');

    const NEXT_STEP_BUTTON_DISABLED_BEFORE = nextStepButton.disabled;

    pElem.disabled = alphaElem.disabled = aElem.disabled = true;
    generateStep1AllButton.disabled = generateStep1AlphaAButton.disabled = true;
    nextStepButton.disabled = true;

    let generated = false;

    try {
        const p = pElem.value;
        const validator = async () => {
            if (!isNumberValid(p)) {
                throw new Error("Please enter the prime number p.");
            }
        };

        const res = await callAPIFull(validator, "ElGamalGenerateAlphaA", `${p},${p_certificate}`, "loader-area-step1", "error-area-step1", "log-area-step1", "Generating α and a given prime number p...");

        if (null === res) return;

        const [alpha, a, cert] = res.output.split(',');

        alphaElem.value = alpha;
        aElem.value = a;
        setPCertificate(p, cert);
        nextStepButton.disabled = false;
        generated = true;
    } finally {
        pElem.disabled = alphaElem.disabled = aElem.disabled = false;
        generateStep1AllButton.disabled = generateStep1AlphaAButton.disabled = false;
        if (!generated) nextStepButton.disabled = NEXT_STEP_BUTTON_DISABLED_BEFORE;
    }
}

async function step1to2() {
    const pElem = document.getElementById('p');
    const alphaElem = document.getElementById('alpha');
    const aElem = document.getElementById('a');
    const betaCalculationElem = document.getElementById('beta-calculation');
    const betaValueElem = document.getElementById('beta-value');
    const publicKeyElem = document.getElementById('public-key');
    const privateKeyElem = document.getElementById('private-key');
    const nextStepButton = document.getElementById('step1to2');
    const generateStep1AllButton = document.getElementById('generatestep1all');
    const generateStep1AlphaAButton = document.getElementById('generatestep1alphaa');

    pElem.disabled = alphaElem.disabled = aElem.disabled = true;
    nextStepButton.disabled = true;
    generateStep1AllButton.disabled = generateStep1AlphaAButton.disabled = true;

    const p = pElem.value;
    const alpha = alphaElem.value;
    const a = aElem.value;

    const validator = async () => {
        if (!isNumberValid(p)) {
            throw new Error("Please enter the prime number p.");
        }
        if (!isNumberValid(alpha)) {
            throw new Error("Please enter the generator α.");
        }
        if (!isNumberValid(a)) {
            throw new Error("Please enter the private key a.");
        }
    };

    const res = await callAPIFull(validator, "ElGamalCalculateBeta", `${p},${alpha},${a},${p_certificate}`, "loader-area-step1", "error-area-step1", "log-area-step1", "Calculating β...");

    if (null === res) {
        pElem.disabled = alphaElem.disabled = aElem.disabled = false;
        nextStepButton.disabled = false;
        generateStep1AllButton.disabled = generateStep1AlphaAButton.disabled = false;
        return;
    }

    const [beta] = res.output.split(',');

    betaCalculationElem.value = `${alpha}^${a} mod ${p}`;
    betaValueElem.value = beta;
    publicKeyElem.value = `(${p}, ${alpha}, ${beta})`;
    privateKeyElem.value = `${a}`;

    for (const elem of [
        document.getElementById('k'),
        document.getElementById('generatek'),
        document.getElementById('message'),
        document.getElementById('input-type-selector'),
        document.getElementById('gamma-input'),
        document.getElementById('delta-input'),
        document.getElementById('x-input-verify'),
        document.getElementById('sign-button'),
        document.getElementById('verify-button'),
        ]) {
        elem.disabled = false;
    }
}

async function signMessage() {
    const kElem = document.getElementById('k');
    const messageElem = document.getElementById('message');
    const inputTypeSelector = document.getElementById('input-type-selector');
    const mElem = document.getElementById('m-before-encryption');
    const signatureElem = document.getElementById('signature');

    kElem.disabled = messageElem.disabled = inputTypeSelector.disabled = true;

    const p = document.getElementById('p').value;
    const alpha = document.getElementById('alpha').value;
    const a = document.getElementById('a').value;
    const k = kElem.value;
    const message = messageElem.value;
    const inputType = inputTypeSelector.value;

    const validator = async () => {
        if (!isNumberValid(k)) {
            throw new Error("Please enter a valid random number k.");
        }
        if (inputType === 'number' && !isNumberValid(message)) {
            throw new Error("Please enter a valid message.");
        }
    };

    const payload = {
        p,
        p_certificate,
        alpha,
        a,
        k,
        message,
        inputType,
    };

    try {
        const res = await callAPIFull(validator, "ElGamalSign", JSON.stringify(payload), "loader-area-sign", "error-area-sign", "log-area-sign", "Signing message...");

        if (null === res) {
            return;
        }

        const [m, gamma, delta] = res.output.split(',');

        mElem.value = m;
        signatureElem.value = `(${gamma}, ${delta})`;
    } finally {
        kElem.disabled = messageElem.disabled = inputTypeSelector.disabled = false;
    }
}

async function verifySignature() {
    const gammaElem = document.getElementById('gamma-input');
    const deltaElem = document.getElementById('delta-input');
    const xInputElem = document.getElementById('x-input-verify');

    gammaElem.disabled = deltaElem.disabled = xInputElem.disabled = true;

    try {
        const p = document.getElementById('p').value;
        const alpha = document.getElementById('alpha').value;
        const beta = document.getElementById('beta-value').value;

        const validator = async () => {
            if (!isNumberValid(gammaElem.value)) {
                throw new Error("Please enter a valid γ.");
            }
            if (!isNumberValid(deltaElem.value)) {
                throw new Error("Please enter a valid δ.");
            }
            if (!isNumberValid(xInputElem.value)) {
                throw new Error("Please enter a valid x.");
            }
        };

        const payload = {
            p,
            p_certificate,
            alpha,
            beta,
            gamma: gammaElem.value,
            delta: deltaElem.value,
            m: xInputElem.value,
        }
        const res = await callAPIFull(validator, "ElGamalVerify", JSON.stringify(payload), "loader-area-verify", "error-area-verify", "log-area-verify", "Verifying signature against message...");

        if (null === res) return;

        const [v1, v2, isEqual] = res.output.split(',');

        document.getElementById('v1-output').value = v1;
        document.getElementById('v2-output').value = v2;
        document.getElementById('verification-result').value = isEqual === 'true' ? 'YES, message is authentic.' : 'NO, message is not authentic! Someone tampered with the message!';
    } finally {
        gammaElem.disabled = deltaElem.disabled = xInputElem.disabled = false;
    }
}

async function generatek() {
    const kElem = document.getElementById('k');
    const generateKButton = document.getElementById('generatek');

    kElem.disabled = true;
    generateKButton.disabled = true;

    const validator = async () => {};

    try {
        const p = document.getElementById('p').value;
        const res = await callAPIFull(validator, "ElGamalSignatureGenerateK", `${p}`, "loader-area-genk", "error-area-genk", "log-area-genk", "Generating random number k...");

        if (null === res) return;

        const k = res.output;
        kElem.value = k;
    } finally {
        kElem.disabled = false;
        generateKButton.disabled = false;
    }
}

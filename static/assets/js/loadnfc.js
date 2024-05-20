document.getElementById('copy-link-button').addEventListener('click', async function () {
    // Create a dummy input element
    var dummyInput = document.createElement('input');

    // Set the value to the URL of the 'View Profile' button
    dummyInput.value = document.getElementById('view-profile-button').href;

    // Append the input element to the body
    document.body.appendChild(dummyInput);

    // Select the input content
    dummyInput.select();

    // Copy the selected text
    document.execCommand('copy');

    // Remove the input element
    document.body.removeChild(dummyInput);

    // Display a message
    alert('Link Copied');

    // Write URL to NFC card
    await writeTag();
});

async function writeTag() {
    if ("NDEFReader" in window) {
        const ndef = new NDEFReader();
        try {
            // Write URL type record to NFC card
            await ndef.write({ records: [{ recordType: "url", data: document.getElementById('view-profile-button').href }] });
            alert("NFC card loaded with URL!");
        } catch (error) {
            alert(error);
        }
    } else {
        alert("Web NFC is not supported.");
    }
}
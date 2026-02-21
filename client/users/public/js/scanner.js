/* Barcode Scanner Logic using Quagga2 */
document.addEventListener("DOMContentLoaded", () => {
    const scannerModal = document.getElementById('scannerModal');
    let isScannerRunning = false;

    if (!scannerModal) return;

    // 1. SCANNER INITIALIZATION
    function startScanner() {
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#interactive'),
                constraints: {
                    facingMode: "environment" // Use back camera
                },
            },
            decoder: {
                readers: ["ean_reader", "ean_8_reader", "upc_reader", "upc_e_reader"]
            },
            locate: true
        }, function (err) {
            if (err) {
                console.error("Quagga Init Error:", err);
                alert("Camera access failed. Please ensure you've granted permissions.");
                return;
            }
            console.log("Initialization finished. Ready to start");
            Quagga.start();
            isScannerRunning = true;
        });

        // 2. SUCCESSFUL SCAN DETECTION (with consistency check)
        const scanResults = new Map();
        const SCAN_THRESHOLD = 3; // Number of times same barcode must be seen

        Quagga.onDetected((data) => {
            if (data.codeResult && data.codeResult.code) {
                const barcode = data.codeResult.code;

                // Track frequency of this specific barcode
                const count = (scanResults.get(barcode) || 0) + 1;
                scanResults.set(barcode, count);

                if (count >= SCAN_THRESHOLD) {
                    console.log("Confirmed Barcode Detected:", barcode);

                    // Clear results for next time
                    scanResults.clear();

                    // Stop and Redirect
                    stopScanner();

                    // Close Modal
                    const modalInstance = bootstrap.Modal.getInstance(scannerModal);
                    if (modalInstance) modalInstance.hide();

                    // Vibration feedback if supported
                    if ("vibrate" in navigator) navigator.vibrate(200);

                    // Redirect to analysis page
                    window.location.href = `/analysis?barcode=${barcode}`;
                }
            }
        });

        // 3. DRAWING OVERLAYS (Optional but helps user see detection)
        Quagga.onProcessed((result) => {
            const drawingCtx = Quagga.canvas.ctx.overlay;
            const drawingCanvas = Quagga.canvas.dom.overlay;

            if (result) {
                if (result.boxes) {
                    drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
                    result.boxes.filter((box) => box !== result.box).forEach((box) => {
                        Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, { color: "green", lineWidth: 2 });
                    });
                }

                if (result.box) {
                    Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, { color: "#ffc107", lineWidth: 2 });
                }

                if (result.codeResult && result.codeResult.code) {
                    Quagga.ImageDebug.drawPath(result.line, { x: 'x', y: 'y' }, drawingCtx, { color: 'red', lineWidth: 3 });
                }
            }
        });
    }

    function stopScanner() {
        if (isScannerRunning) {
            Quagga.stop();
            isScannerRunning = false;
        }
    }

    // 4. MODAL EVENTS
    scannerModal.addEventListener('shown.bs.modal', () => {
        startScanner();
    });

    scannerModal.addEventListener('hidden.bs.modal', () => {
        stopScanner();
    });
});

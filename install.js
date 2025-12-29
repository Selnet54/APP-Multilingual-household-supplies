<!DOCTYPE html>
<html lang="sr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multilingual Household Supplies</title>
    
    <link rel="manifest" href="./manifest.json">
    <meta name="theme-color" content="#4CAF50">

    <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
</head>
<body>
    <button id="installBtn" style="display:none; padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
        Instaliraj Aplikaciju
    </button>

    <div id="python-output">
        <py-config>
            [[fetch]]
            files = ["./multi-jezik5a.py"]
        </py-config>

        <py-script>
            print("📦 Multilingual Household Supplies is starting...")
            import multi_jezik5a # Ovo učitava vašu logiku
        </py-script>
    </div>

    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js')
                    .then(reg => console.log('Service Worker registrovan!', reg))
                    .catch(err => console.err('Greška pri registraciji:', err));
            });
        }
    </script>
    
    <script src="./install.js"></script>
</body>
</html>

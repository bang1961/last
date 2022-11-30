var isServiceWorkerSurpported = 'serviceWorker' in navigator;
if (isServiceWorkerSurpported){
    widow.addEventListener("load", () => {
        navigator.serviceWorker
        .register("/service-worker.js")
        .then(registration => 
            console.log("Service Worker regisered", registration)
        )
        .catch(err => console.log(err));
    });
}
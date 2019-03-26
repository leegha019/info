if(parseInt(window.screen.availWidth) < 800){
    window.location.replace("http://localhost:5000/dev=1");
} else {
    window.location.replace("http://localhost:5000/?dev=2");
}
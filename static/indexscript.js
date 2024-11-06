document.addEventListener("DOMContentLoaded", function() {
    const text = "CYCLONIC";
    let index = 0;
    const speed = 250; 
    
    const cursor = document.createElement("span");
    cursor.className = "ind-cursor";
    document.getElementById("ind-typewriter").appendChild(cursor);
    
    function typeWriter() {
        if (index < text.length) {
            document.getElementById("ind-typewriter").innerHTML = text.substring(0, index + 1);
            document.getElementById("ind-typewriter").appendChild(cursor);
            index++;
            setTimeout(typeWriter, speed);
        } else {
            cursor.style.display = 'none'; 
        }
    }

    typeWriter();
});
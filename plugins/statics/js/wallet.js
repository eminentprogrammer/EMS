

const TestCard2 = document.getElementById("test-card2")
const TestCard3 = document.getElementById("test-card3")



myTimeout = setInterval(animate, 1000);   


function animate() {
    if (TestCard2.classList.contains("test-card-2")){
        TestCard2.classList.remove("test-card-2")
        TestCard3.classList.remove("test-card-3")
        TestCard2.classList.add("animate-test-card-2")
        TestCard3.classList.add("animate-test-card-3")
    }
    else{
        TestCard2.classList.remove("animate-test-card-2")
        TestCard3.classList.remove("animate-test-card-3")
        TestCard2.classList.add("test-card-2")
        TestCard3.classList.add("test-card-3")
    }
}

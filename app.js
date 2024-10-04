document.getElementById("submit").addEventListener("click", async function () {
    const question = document.getElementById("question").value;
    const loadingElement = document.getElementById("loading");
    const answerElement = document.getElementById("answer");
    
    // Reset previous response, but keep the heading visible
    answerElement.innerText = "You can see the results here...";
    
    // Show loading bar
    loadingElement.classList.remove("hidden");
  
    if (!question) {
      alert("Please enter a question.");
      loadingElement.classList.add("hidden"); // Hide loading bar
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: question }),
      });
  
      const data = await response.json();
  
      // Hide loading bar when the response is received
      loadingElement.classList.add("hidden");
  
      // Display the response, and keep the text "Here's what you want"
      if (data.answer) {
        answerElement.innerHTML = data.answer.replace(/\n/g, "<br>"); // Preserving formatting with line breaks
      } else {
        answerElement.innerText = "Error: " + data.error;
      }
    } catch (error) {
      answerElement.innerText = "Error fetching data from the server.";
      loadingElement.classList.add("hidden");
    }
  });
  
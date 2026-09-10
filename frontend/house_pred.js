document
  .getElementById("prediction-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    const area = Number(formData.get("area"));
    const bedrooms = Number(formData.get("bedrooms"));
    const location = formData.get("location");

    const result = document.getElementById("result");

    try {
      const response = await fetch(
        `/predict?area=${area}&bedrooms=${bedrooms}&location=${location}`,
      );

      if (!response.ok) {
        throw new Error("Prediction request failed");
      }

      const data = await response.json();

      const formattedPrice = Number(data.predicted_price).toLocaleString(
        "en-US",
      );

      result.textContent = `Predicted Price: ${formattedPrice} VND`;
    } catch (error) {
      result.textContent = "Error: Unable to predict price.";
      console.error(error);
    }
  });

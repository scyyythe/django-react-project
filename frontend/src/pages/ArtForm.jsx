import React, { useState } from "react";

function ArtForm() {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("");
  const [artStatus, setArtStatus] = useState("Available");
  const [price, setPrice] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = {
      title: title,
      category: category,
      art_status: artStatus,
      price: price,
      description: description,
    };

    // Get the token from localStorage
    const token = localStorage.getItem("access_token");

    if (!token) {
      console.error("User is not authenticated");
      alert("You need to login first.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/art/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      // Read the response as JSON (only once)
      const responseData = await response.json();
      console.log("Response Data:", responseData);

      if (response.ok) {
        console.log("Art created:", responseData);
        alert("Art created successfully!");
      } else {
        console.error("Error creating art:", responseData);
        alert("Error creating art. Please try again later.");
      }
    } catch (error) {
      console.error("Error creating art:", error);
      alert("Error creating art. Please try again later.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Artwork</h2>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        required
      />
      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit">Create Art</button>
    </form>
  );
}

export default ArtForm;

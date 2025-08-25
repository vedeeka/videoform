'use client';
import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
const [generatedCode, setGeneratedCode] = useState("");
const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();

  try {
    const res = await fetch("http://127.0.0.1:5000/generate_manim_code", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: text }),
    });

    const data = await res.json();
    console.log("Success:", data);

    // show in UI
    setGeneratedCode(data.manim_code);

    setText(""); // clear input
  } catch (error) {
    console.error("Error:", error);
  }
};



  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="flex">
        <input
          type="text"
          placeholder="Enter text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="border  border-black text-black rounded-lg p-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="ml-4 bg-blue-500 text-black px-4 py-2 rounded-lg hover:bg-blue-600 transition"
        >
          Submit
        </button>
      </form>
    </div>
  );
}

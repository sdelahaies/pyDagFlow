import React, { useCallback } from "react";
import "../index.css";

export const Button =  () => {
  const onClick = useCallback( async () => {
    console.log("Vite + React + TypeScript + Tailwind = ❤️"); 
    const formData = new FormData();
    const url="http://127.0.0.1:5000/run_from_react";
    try {
      // You can write the URL of your server or any other endpoint used for file upload
      const result = await fetch(url, {
        method: "POST",
        body: formData,
      });
      const data = await result.json();
      console.log(data);
      return data;
    } catch (error) {
      console.error(error);
    }
  }, []);

  return (
    <button
      onClick={onClick}
      className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded`}
    >
      Vite is better than Webpack
    </button>

    
  );
};

const API_BASE =
  import.meta.env.MODE === "development"
    ? "/api" 
    : "http://89.169.177.178:8081/api"; 

export default API_BASE;
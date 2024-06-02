import axios from "axios";

const request = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  headers: { "Content-Type": "application/json" },
});

/**
 * 請求攔截
 * Add a request interceptor
 */


request.interceptors.request.use( (config) => {
  console.log('request',config);
  return config;
},  (error) => {
  
  return Promise.reject(error);
});


request.interceptors.response.use( (config) => {
  console.log('response',config);
  
  return config;
},  (error) => {
  // 
  return Promise.reject(error);
});

export default request;
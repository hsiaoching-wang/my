import request from "@/utils/request";

export function generateData(data) {
  return request({
    url: "/generate",
    method: "post",
    data,
  });
}
export function enter2Data(data) {
  return request({
    url: "/enter",
    method: "post",
    data,
  });
}
export function getData(data) {
  return request({
    url: "/get",
    method: "post",
    data,
  });
}
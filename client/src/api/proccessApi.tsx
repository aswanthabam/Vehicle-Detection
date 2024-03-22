import axios from "axios";
import { ProcessResponse } from "../types";

export const processImage = async (file: File): Promise<ProcessResponse> => {
  var formData = new FormData();
  formData.append("file", file);
  try {
    var res = await axios.post(
      import.meta.env.VITE_SERVER_BASE_URL + "/process",
      formData
    );
    console.log(res);
    if (res.status === 200) {
      return {
        status: true,
        message: res.data.message,
        data: res.data.data,
      };
    } else {
      try {
        return { status: false, message: res.data.message, data: null };
      } catch (e) {
        console.error(e);
        return {
          status: false,
          message: "An unexpeceted error occured. Please try again later.",
          data: null,
        };
      }
    }
  } catch (e) {
    console.error(e);
    return {
      status: false,
      message: "An unexpeceted error occured. Please try again later.",
      data: null,
    };
  }
};

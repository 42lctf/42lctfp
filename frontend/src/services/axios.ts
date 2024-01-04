import { dispatchLogout } from "@/technical/events";
import axios from "axios";

export const AxiosErrorText = (axiosError: any): string => {
    return axiosError?.response?.data?.detail ||
        axiosError?.response?.statusText ||
        axiosError?.message;
};

const instance = axios.create({
    baseURL: import.meta.env.VITE_BASEURL
})

instance.interceptors.request.use(
    (req) => {
        req.baseURL = import.meta.env.VITE_BASEURL;
        return req;
    }
);


instance.interceptors.response.use(
    (response) => {
        // eslint-disable-next-line no-console
        if (import.meta.env.DEV && response.config.method !== 'OPTIONS') {
            console.log('inter res', response);
        }

        return response;
    },
    (error) => {
        // eslint-disable-next-line no-console
        if (import.meta.env.DEV && error.response.config.method !== 'OPTIONS') {
            console.log('myaxiosintercept', AxiosErrorText(error), error);
        }

        if (error.response && error.response.status === 401) {
            dispatchLogout();
        }

        return Promise.reject(error);
    }
);
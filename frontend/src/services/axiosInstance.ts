import { dispatchLogout } from '@/technical/events';
import axios from 'axios';

export const axiosClient = axios.create({
    baseURL: '/api/v1',
    withCredentials: true,
});

axiosClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            dispatchLogout();
        }
        return Promise.reject(error);
    }
);
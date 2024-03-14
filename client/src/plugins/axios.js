import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://10.10.20.24:8000',
});
export default instance;

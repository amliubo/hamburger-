import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://47.100.41.212:8000',
});
export default instance;

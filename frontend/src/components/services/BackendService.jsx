import axios from "axios";
import Utils from "../utils/Utils";

const API_URL = 'http://127.0.0.1:5000'
const AUTH_URL = 'http://127.0.0.1:5000'

class BackendService {
    login(login, password) {
        return axios.post(`${AUTH_URL}/login`, { login, password })
            .then(response => {
                console.log('Заголовки ответа:', response.headers);
                // Ваш код обработки данных или дальнейших действий
                return response; // Возвращаем ответ для дальнейшей обработки
            })
            .catch(error => {
                console.error('Произошла ошибка:', error);
                throw error; // Пробросим ошибку для обработки в другом месте кода, если это необходимо
            });
    }

    logout() {
        return axios.get(`${AUTH_URL}/logout`, { headers : {Authorization : Utils.getToken()}})
    }
}

export default new BackendService();
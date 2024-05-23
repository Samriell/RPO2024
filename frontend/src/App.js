import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SideBar from './components/SideBar'; // Импортируем компонент SideBar
import RegisterForm from './components/RegisterForm';
import NavigationBar from './components/NavigationBar';
import Home from './components/Home';
import 'bootstrap/dist/css/bootstrap.min.css';
import LoginForm from './components/LoginForm';
import WelcomePage from './components/WelcomePage';
import CountiesPage from './components/CountriesPage';

function App() {
  const [registeredUsers, setRegisteredUsers] = useState([]);
  const [isSideBarExpanded, setIsSideBarExpanded] = useState(true); // Состояние для отображения/скрытия SideBar

  // Функция для обработки регистрации пользователя
  function handleRegister(username, password) {
    // Проверяем, есть ли пользователь с таким именем
    const isUserExist = registeredUsers.some(user => user.username === username);
    if (isUserExist) {
      alert('User already exists!');
    } else {
      // Добавляем пользователя в список зарегистрированных пользователей
      setRegisteredUsers(prevUsers => [...prevUsers, { username, password }]);
      // Возвращаем объект, чтобы показать, что регистрация прошла успешно
      return { success: true, username };
    }
  }

  // Функция для обработки входа пользователя
  function handleLogin(username, password) {
    // Реализация входа пользователя
  }

  // Функция для переключения состояния SideBar
  function toggleSideBar() {
    setIsSideBarExpanded(!isSideBarExpanded);
  }

  return (
    <div className="App">
      <BrowserRouter>
        <SideBar expanded={isSideBarExpanded} /> {/* Помещаем SideBar здесь */}
        <NavigationBar />
        <div className="wrapper">
          <div id="content">
            <button onClick={toggleSideBar}>Toggle SideBar</button> {/* Кнопка для переключения состояния SideBar */}
            <Routes>
              <Route path="/" element={<Home />} />
              {/* Передаем функцию handleRegister компоненту RegisterForm */}
              <Route path="/register" element={<RegisterForm handleRegister={handleRegister} />} />
              {/* Передаем функцию handleLogin компоненту LoginForm */}
              <Route path="/login" element={<LoginForm handleLogin={handleLogin} />} />
              {/* Перенаправляем пользователя на страницу приветствия после успешной регистрации */}
              {registeredUsers.map(user => (
                user.success && <Navigate key={user.username} to={`/welcome/${user.username}`} />
              ))}
              <Route path="/welcome/:username" element={<WelcomePage />} />
              <Route path="/countries" element={<CountiesPage />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;

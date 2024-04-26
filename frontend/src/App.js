import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import RegisterForm from './components/RegisterForm';
import NavigationBar from './components/NavigationBar';
import Home from './components/Home';
import LoginForm from './components/LoginForm';
import WelcomePage from './components/WelcomePage';

function App() {
  const [registeredUsers, setRegisteredUsers] = useState([]);

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

  return (
    <div className="App">
      <BrowserRouter>
        <NavigationBar />
        <div className="container-fluid">
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
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;


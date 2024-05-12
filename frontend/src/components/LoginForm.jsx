import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setUserName } from './authReducer';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate(); // Подключаем useNavigate

  const handleLogin = (username, password) => {
    // Логика проверки логина и пароля
    if (username === 'Lissibeth' && password === '7777') {
        console.log('Login successful');
        return true;
    } else {
        console.log('Login failed');
        return false;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please enter both username and password.');
      return;
    }

    // Проверяем успешный вход
    if (handleLogin(username, password)) {
        // Действие после успешного входа
        dispatch(setUserName(username));
        
        // Перенаправление на страницу Welcome
        navigate('/welcome');
    } else {
        setError('Invalid username or password.');
    }
  };

  return (
    <div className="row justify-content-center mt-5">
      <div className="col-md-6">
        <div className="card">
          <h5 className="card-header">Login</h5>
          <div className="card-body">
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="username" className="form-label">
                  Username
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="password" className="form-label">
                  Password
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <button type="submit" className="btn btn-primary">
                Login
              </button>
              <Link to="/register" className="btn btn-link ms-2">
                Register
              </Link>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;

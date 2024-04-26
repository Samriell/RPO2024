import React from 'react';
import { Link, useParams } from 'react-router-dom';

const WelcomePage = () => {
  const { username } = useParams();

  return (
    <div className="row justify-content-center mt-5">
      <div className="col-md-6">
        <div className="card">
          <h5 className="card-header">Welcome, {username}!</h5> {/* Отображаем имя пользователя */}
          <div className="card-body">
            <p>You are now logged in.</p>
            <Link to="/" className="btn btn-primary">
              Go to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomePage;


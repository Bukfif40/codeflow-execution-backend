import { useEffect, useState } from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

function App() {
  const [health, setHealth] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [showRegister, setShowRegister] = useState(false);
  const [pendingLogin, setPendingLogin] = useState<{username: string, password: string} | null>(null);
  const [profile, setProfile] = useState<{username: string, role: string} | null>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((res) => res.json())
      .then((data) => setHealth(data.status))
      .catch(() => setError('Could not reach backend.'));
  }, []);

  // Fetch user profile when token changes
  useEffect(() => {
    if (token) {
      fetch('http://127.0.0.1:8000/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then(res => res.ok ? res.json() : null)
        .then(data => setProfile(data))
        .catch(() => setProfile(null));
    } else {
      setProfile(null);
    }
  }, [token]);

  // If registration just happened, auto-fill login
  useEffect(() => {
    if (pendingLogin) {
      // Optionally, auto-login here, but for now just pre-fill login form
    }
  }, [pendingLogin]);

  const handleLogout = () => setToken(null);

  return (
    <div className="health-container">
      <h1>Codeflow Frontend</h1>
      {!token ? (
        <>
          {showRegister ? (
            <>
              <RegisterForm onRegistered={(username, password) => {
                setShowRegister(false);
                setPendingLogin({username, password});
              }} />
              <p>Already have an account? <button onClick={() => setShowRegister(false)}>Login</button></p>
            </>
          ) : (
            <>
              <LoginForm onLogin={setToken} />
              <p>Don't have an account? <button onClick={() => setShowRegister(true)}>Register</button></p>
            </>
          )}
        </>
      ) : (
        <>
          <p>
            Backend status:{' '}
            {health ? <b className="health-ok">{health}</b> : error ? <b className="health-error">{error}</b> : 'Loading...'}
          </p>
          {profile ? (
            <div className="profile">
              <h2>Profile</h2>
              <p><b>Username:</b> {profile.username}</p>
              <p><b>Role:</b> {profile.role}</p>
            </div>
          ) : (
            <p>Loading profile...</p>
          )}
          <button onClick={handleLogout}>Logout</button>
        </>
      )}
    </div>
  );
}

export default App;

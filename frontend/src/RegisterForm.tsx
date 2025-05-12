import React, { useState } from 'react';

interface RegisterFormProps {
  onRegistered: (username: string, password: string) => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onRegistered }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setSuccess(false);
    try {
      const response = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'accept': 'application/json',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
      });
      const data = await response.json();
      if (response.ok && data.msg === 'User registered successfully') {
        setSuccess(true);
        onRegistered(username, password);
      } else {
        setError(data.detail || 'Registration failed.');
      }
    } catch (err) {
      setError('Could not connect to backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <h2>Register</h2>
      <div>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Registering...' : 'Register'}
      </button>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">Registration successful! You can now log in.</div>}
    </form>
  );
};

export default RegisterForm;

import { useEffect, useState } from 'react';

function App() {
  const [health, setHealth] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((res) => res.json())
      .then((data) => setHealth(data.status))
      .catch(() => setError('Could not reach backend.'));
  }, []);

  return (
    <div className="health-container">
      <h1>Codeflow Frontend Health Check</h1>
      <p>
        Backend status:{' '}
        {health ? <b className="health-ok">{health}</b> : error ? <b className="health-error">{error}</b> : 'Loading...'}
      </p>
      <p>Edit <code>src/App.tsx</code> to start building your app.</p>
    </div>
  );
}

export default App;

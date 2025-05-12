import React, { useState } from 'react';

interface SearchFormProps {
  token: string;
}

const SearchForm: React.FC<SearchFormProps> = ({ token }) => {
  const [query, setQuery] = useState('');
  const [provider, setProvider] = useState('bing');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults([]);
    try {
      const response = await fetch('http://127.0.0.1:8000/search?query=' + encodeURIComponent(query) + '&provider=' + encodeURIComponent(provider), {
        headers: {
          'Authorization': `Bearer ${token}`,
          'accept': 'application/json',
        },
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Search failed.');
      } else {
        const data = await response.json();
        setResults(data.results || []);
      }
    } catch (err) {
      setError('Could not connect to backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-form-container">
      <form onSubmit={handleSubmit} className="search-form">
        <h2>Web Search</h2>
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Enter your search query"
          required
        />
        <label htmlFor="provider-select">Provider:</label>
        <select id="provider-select" value={provider} onChange={e => setProvider(e.target.value)}>
          <option value="bing">Bing</option>
          <option value="ddg">DuckDuckGo</option>
          <option value="serpapi">SerpAPI (Premium)</option>
        </select>
        <button type="submit" disabled={loading}>{loading ? 'Searching...' : 'Search'}</button>
      </form>
      {error && <div className="error">{error}</div>}
      {results.length > 0 && (
        <div className="search-results">
          <h3>Results</h3>
          <div className="results-grid">
            {results.map((item, idx) => (
              <div className="result-card" key={idx} style={{border: '1px solid #ccc', borderRadius: 8, margin: '8px 0', padding: 12, background: '#fafaff'}}>
                {item.title && (
                  <div style={{fontWeight: 'bold', fontSize: '1.1em', marginBottom: 4}}>
                    {item.link ? (
                      <a href={item.link} target="_blank" rel="noopener noreferrer">{item.title}</a>
                    ) : item.title}
                  </div>
                )}
                {item.snippet && (
                  <div style={{marginBottom: 4}}>{item.snippet}</div>
                )}
                {item.link && !item.title && (
                  <div><a href={item.link} target="_blank" rel="noopener noreferrer">{item.link}</a></div>
                )}
                {/* Show raw JSON for any other fields */}
                {Object.keys(item).filter(k => !['title','snippet','link'].includes(k)).length > 0 && (
                  <pre style={{fontSize: '0.85em', color: '#555', background: '#f3f3f3', borderRadius: 4, padding: 4, marginTop: 4}}>{JSON.stringify(item, null, 2)}</pre>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchForm;

import { useState } from 'react';
import './App.css';

function App() {
  const [searchMode, setSearchMode] = useState('text');
  const [query, setQuery] = useState('');
  const [modality, setModality] = useState('');
  const [bodyPart, setBodyPart] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTime, setSearchTime] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleSearch = async () => {
    if (!query.trim() && !selectedImage) {
      setError('Please enter a search query or upload an image');
      return;
    }

    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const requestBody = {
        query: query.trim(),
        limit: 10,
        modality: modality || undefined,
        body_part: bodyPart || undefined,
      };

      if (selectedImage) {
        requestBody.image = selectedImage;
      }

      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data.results || []);
      setSearchTime(data.query_time_ms);
    } catch (err) {
      setError(err.message);
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSearch();
    }
  };

  return (
    <div className="app">
      {/* Hero Header */}
      <header className="hero">
        <div className="hero-content">
          <div className="logo-section">
            <div className="logo-icon">🏥</div>
            <h1 className="app-title">MediMatch</h1>
          </div>
          <p className="app-subtitle">
            AI-Powered Medical Case Search • Powered by CLIP Neural Networks
          </p>
          <div className="stats-bar">
            <div className="stat">
              <span className="stat-number">100+</span>
              <span className="stat-label">Medical Cases</span>
            </div>
            <div className="stat">
              <span className="stat-number">88%</span>
              <span className="stat-label">Accuracy</span>
            </div>
            <div className="stat">
              <span className="stat-number">&lt;200ms</span>
              <span className="stat-label">Query Time</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          {/* Search Section */}
          <section className="search-section">
            <div className="search-card">
              {/* Mode Tabs */}
              <div className="mode-tabs">
                <button
                  className={`mode-tab ${searchMode === 'text' ? 'active' : ''}`}
                  onClick={() => setSearchMode('text')}
                >
                  <span className="tab-icon">📝</span>
                  Text Search
                </button>
                <button
                  className={`mode-tab ${searchMode === 'image' ? 'active' : ''}`}
                  onClick={() => setSearchMode('image')}
                >
                  <span className="tab-icon">🖼️</span>
                  Image Search
                </button>
              </div>

              {/* Search Input */}
              <div className="search-input-section">
                {searchMode === 'text' ? (
                  <div className="text-search">
                    <input
                      type="text"
                      className="search-input"
                      placeholder="E.g., pneumonia, enlarged heart, chest consolidation..."
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      onKeyPress={handleKeyPress}
                      disabled={loading}
                    />
                    <button
                      className="search-button"
                      onClick={handleSearch}
                      disabled={loading || !query.trim()}
                    >
                      {loading ? (
                        <>
                          <span className="spinner"></span>
                          Searching...
                        </>
                      ) : (
                        <>
                          <span className="search-icon">🔍</span>
                          Search
                        </>
                      )}
                    </button>
                  </div>
                ) : (
                  <div className="image-search">
                    <div className="image-upload-zone">
                      <input
                        type="file"
                        id="image-upload"
                        accept="image/*"
                        onChange={handleImageUpload}
                        style={{ display: 'none' }}
                      />
                      <label htmlFor="image-upload" className="upload-label">
                        {selectedImage ? (
                          <div className="preview-container">
                            <img src={selectedImage} alt="Preview" className="image-preview" />
                            <p className="upload-text-small">Click to change image</p>
                          </div>
                        ) : (
                          <>
                            <div className="upload-icon">📤</div>
                            <p className="upload-text">Click to upload medical image</p>
                            <p className="upload-hint">Supports X-ray, CT, MRI images</p>
                          </>
                        )}
                      </label>
                    </div>
                    <button
                      className="search-button"
                      onClick={handleSearch}
                      disabled={loading || !selectedImage}
                    >
                      {loading ? (
                        <>
                          <span className="spinner"></span>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <span className="search-icon">🔍</span>
                          Find Similar Cases
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>

              {/* Filters */}
              <div className="filters">
                <div className="filter-group">
                  <label className="filter-label">Modality</label>
                  <select
                    className="filter-select"
                    value={modality}
                    onChange={(e) => setModality(e.target.value)}
                    disabled={loading}
                  >
                    <option value="">All modalities</option>
                    <option value="xray">X-ray</option>
                    <option value="ct">CT Scan</option>
                    <option value="mri">MRI</option>
                  </select>
                </div>
                <div className="filter-group">
                  <label className="filter-label">Body Part</label>
                  <select
                    className="filter-select"
                    value={bodyPart}
                    onChange={(e) => setBodyPart(e.target.value)}
                    disabled={loading}
                  >
                    <option value="">All body parts</option>
                    <option value="chest">Chest</option>
                    <option value="head">Head</option>
                    <option value="abdomen">Abdomen</option>
                  </select>
                </div>
              </div>
            </div>
          </section>

          {/* Error Message */}
          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
            </div>
          )}

          {/* Results Section */}
          {searchTime && (
            <div className="results-header">
              <h2>Search Results</h2>
              <span className="search-time">Found {results.length} cases in {searchTime.toFixed(0)}ms</span>
            </div>
          )}

          {results.length === 0 && !loading && !error && (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <h3>No results yet</h3>
              <p>Enter a search query or upload an image to find similar medical cases</p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="loading-spinner-large"></div>
              <p>Analyzing with AI neural networks...</p>
            </div>
          )}

          {/* Results Grid */}
          {results.length > 0 && (
            <section className="results-grid">
              {results.map((result) => (
                <div key={result.id} className="result-card">
                  <div className="card-header">
                    <div className="diagnosis-badge">
                      <span className="badge-icon">🏥</span>
                      {result.diagnosis}
                    </div>
                    <div className="similarity-score">
                      <div
                        className="score-circle"
                        style={{
                          background: `conic-gradient(#10b981 ${result.similarity_score * 100}%, #e5e7eb 0)`,
                        }}
                      >
                        <div className="score-inner">
                          {Math.round(result.similarity_score * 100)}%
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="card-content">
                    <div className="case-info">
                      <div className="info-row">
                        <span className="info-label">Case ID:</span>
                        <span className="info-value">{result.case_id}</span>
                      </div>
                      <div className="info-row">
                        <span className="info-label">Modality:</span>
                        <span className="info-value modality-tag">{result.modality}</span>
                      </div>
                      <div className="info-row">
                        <span className="info-label">Body Part:</span>
                        <span className="info-value">{result.body_part}</span>
                      </div>
                      <div className="info-row">
                        <span className="info-label">Patient:</span>
                        <span className="info-value">
                          {result.age}y / {result.gender}
                        </span>
                      </div>
                    </div>

                    <div className="findings">
                      <h4 className="findings-title">Clinical Findings</h4>
                      <p className="findings-text">{result.findings}</p>
                    </div>
                  </div>

                  <div className="card-footer">
                    <button className="view-details-btn">
                      View Full Details →
                    </button>
                  </div>
                </div>
              ))}
            </section>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p className="footer-text">
            Built with ❤️ using FastAPI, React, PostgreSQL & OpenAI CLIP
          </p>
          <div className="footer-links">
            <a href="https://github.com/devyani648/mediMatch" target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
            <span>•</span>
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
              API Docs
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
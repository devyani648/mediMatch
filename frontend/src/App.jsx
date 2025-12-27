import React, { useState } from 'react'
import SearchBar from './components/SearchBar'
import ImageUpload from './components/ImageUpload'
import CaseGrid from './components/CaseGrid'
import client from './api/client'

export default function App() {
  const [searchMode, setSearchMode] = useState('text')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const doSearch = async (payload) => {
    setLoading(true)
    setError(null)
    try {
      const res = await client.search(payload)
      setResults(res.data.results)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-4">
      <header className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">MediMatch</h1>
        <div>
          <button onClick={() => setSearchMode('text')} className={`mr-2 px-3 py-1 border rounded ${searchMode==='text'?'bg-blue-500 text-white':''}`}>Text</button>
          <button onClick={() => setSearchMode('image')} className={`px-3 py-1 border rounded ${searchMode==='image'?'bg-blue-500 text-white':''}`}>Image</button>
        </div>
      </header>

      <main>
        {searchMode === 'text' ? (
          <SearchBar onSearch={doSearch} loading={loading} />
        ) : (
          <ImageUpload onSearch={doSearch} loading={loading} />
        )}

        {loading && <div className="mt-4">Searching...</div>}
        {error && <div className="mt-4 text-red-600">{error}</div>}

        <div className="mt-6">
          <CaseGrid cases={results} />
        </div>
      </main>
    </div>
  )
}

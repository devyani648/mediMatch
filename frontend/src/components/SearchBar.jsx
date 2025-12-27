import React, { useState } from 'react'

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('')
  const [modality, setModality] = useState('all')
  const [bodyPart, setBodyPart] = useState('all')

  const submit = (e) => {
    e.preventDefault()
    if (!query) return
    onSearch({ query, modality: modality === 'all' ? null : modality, body_part: bodyPart === 'all' ? null : bodyPart })
  }

  return (
    <form onSubmit={submit} className="space-y-3">
      <div>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="E.g., pneumonia, bilateral infiltrates..." className="w-full p-2 border rounded" />
      </div>
      <div className="flex gap-2">
        <select value={modality} onChange={(e) => setModality(e.target.value)} className="p-2 border rounded">
          <option value="all">All modalities</option>
          <option value="xray">Xray</option>
          <option value="ct">CT</option>
          <option value="mri">MRI</option>
        </select>
        <select value={bodyPart} onChange={(e) => setBodyPart(e.target.value)} className="p-2 border rounded">
          <option value="all">All body parts</option>
          <option value="chest">Chest</option>
          <option value="brain">Brain</option>
          <option value="abdomen">Abdomen</option>
        </select>
        <button type="submit" disabled={loading || !query} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-60">Search</button>
      </div>
    </form>
  )
}

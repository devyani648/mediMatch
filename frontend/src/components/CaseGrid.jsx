import React from 'react'
import CaseCard from './CaseCard'

export default function CaseGrid({ cases }) {
  if (!cases || cases.length === 0) {
    return <div className="text-center text-gray-500">No results yet. Try a search above.</div>
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {cases.map((c) => (
        <CaseCard key={c.id} item={c} />
      ))}
    </div>
  )
}

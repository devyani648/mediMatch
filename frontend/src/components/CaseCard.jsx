import React from 'react'

function scoreColor(score) {
  if (score >= 0.9) return 'bg-green-500'
  if (score >= 0.8) return 'bg-blue-500'
  if (score >= 0.7) return 'bg-yellow-400'
  return 'bg-gray-300'
}

export default function CaseCard({ item }) {
  const score = item.similarity_score || 0
  const pct = Math.round(score * 100)

  return (
    <div className="border rounded p-3 hover:shadow">
      {item.image_url ? (
        <img src={item.image_url} alt={item.case_id} className="w-full h-40 object-cover rounded" />
      ) : (
        <div className="w-full h-40 bg-gray-100 flex items-center justify-center rounded">No image</div>
      )}
      <div className="flex items-center justify-between mt-2">
        <div>
          <div className="font-semibold">{item.diagnosis}</div>
          <div className="text-sm text-gray-600">{item.case_id}</div>
        </div>
        <div className={`text-white text-sm px-2 py-1 rounded ${scoreColor(score)}`}>{pct}%</div>
      </div>
      <div className="text-sm text-gray-700 mt-2 grid grid-cols-3 gap-2">
        <div>Modality: {item.modality}</div>
        <div>Body: {item.body_part}</div>
        <div>Age/Gender: {item.age}/{item.gender}</div>
      </div>
      <div className="text-sm text-gray-600 mt-2 line-clamp-2">{item.findings}</div>
      <div className="mt-3">
        <button className="px-3 py-1 border rounded">View Details</button>
      </div>
    </div>
  )
}

import React, { useRef, useState } from 'react'

function toBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = (err) => reject(err)
  })
}

export default function ImageUpload({ onSearch, loading }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [modality, setModality] = useState('all')
  const [bodyPart, setBodyPart] = useState('all')
  const inputRef = useRef()

  const handleFile = async (f) => {
    setFile(f)
    const b = await toBase64(f)
    setPreview(b)
  }

  const submit = async (e) => {
    e.preventDefault()
    if (!preview) return
    onSearch({ image: preview, modality: modality === 'all' ? null : modality, body_part: bodyPart === 'all' ? null : bodyPart })
  }

  return (
    <div>
      <form onSubmit={submit} className="space-y-3">
        <div className="border-2 border-dashed p-4 rounded" onClick={() => inputRef.current.click()}>
          {!preview ? (
            <div className="text-center text-gray-500">Click or drag to upload an image</div>
          ) : (
            <img src={preview} alt="preview" className="max-h-48 mx-auto" />
          )}
          <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={(e) => e.target.files && handleFile(e.target.files[0])} />
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
          <button type="submit" disabled={loading || !preview} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-60">Search</button>
          {preview && <button type="button" onClick={() => { setPreview(null); setFile(null); }} className="px-3 py-1 border rounded">Clear</button>}
        </div>
      </form>
    </div>
  )
}

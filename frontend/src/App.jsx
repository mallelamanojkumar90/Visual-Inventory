import { useState, useRef } from 'react'
import axios from 'axios'
import { Upload, CheckCircle, AlertCircle, Loader2, FileJson, Package } from 'lucide-react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setPreview(URL.createObjectURL(selectedFile))
      setResult(null)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setLoading(true)
    setError(null)
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      // Assuming backend is running on localhost:8000
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err) {
      console.error(err)
      setError(err.response?.data?.detail || 'An error occurred during processing.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo">
          <Package size={32} />
          <h1>Visual Inventory Manager</h1>
        </div>
        <p className="subtitle">AI-Powered Receipt & Shelf Analysis</p>
      </header>

      <main className="main-content">
        <div className="upload-section card">
          <div 
            className={`dropzone ${preview ? 'has-preview' : ''}`}
            onClick={() => fileInputRef.current.click()}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              accept="image/*" 
              hidden 
            />
            
            {preview ? (
              <div className="preview-container">
                <img src={preview} alt="Upload preview" className="preview-image" />
                <div className="overlay">
                  <Upload size={24} />
                  <span>Change Image</span>
                </div>
              </div>
            ) : (
              <div className="placeholder">
                <Upload size={48} />
                <p>Click or Drag to Upload Image</p>
                <span className="hint">Supports JPG, PNG (Receipts, Shelves)</span>
              </div>
            )}
          </div>

          <button 
            className="process-btn" 
            onClick={handleUpload} 
            disabled={!file || loading}
          >
            {loading ? (
              <>
                <Loader2 className="spin" size={20} /> Processing...
              </>
            ) : (
              <>
                <CheckCircle size={20} /> Analyze Inventory
              </>
            )}
          </button>

          {error && (
            <div className="error-message">
              <AlertCircle size={20} />
              <span>{error}</span>
            </div>
          )}
        </div>

        {result && (
          <div className="results-section">
            <div className="stats-cards">
              <div className="stat-card">
                <span className="label">Confidence</span>
                <span className={`value ${result.confidence_score > 0.8 ? 'high' : 'low'}`}>
                  {(result.confidence_score * 100).toFixed(0)}%
                </span>
              </div>
              <div className="stat-card">
                <span className="label">Items Found</span>
                <span className="value">{result.items.length}</span>
              </div>
              <div className="stat-card">
                <span className="label">Merchant</span>
                <span className="value">{result.merchant_name || 'Unknown'}</span>
              </div>
            </div>

            <div className="table-card card">
              <h2>Extracted Items</h2>
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Item Name</th>
                      <th>Category</th>
                      <th>Qty</th>
                      <th>Unit</th>
                      <th>Price/Unit</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.items.map((item, index) => (
                      <tr key={index}>
                        <td>{item.item_name}</td>
                        <td><span className="badge">{item.category}</span></td>
                        <td>{item.quantity}</td>
                        <td>{item.unit}</td>
                        <td>{item.unit_price ? `$${item.unit_price.toFixed(2)}` : '-'}</td>
                        <td>{item.total_price ? `$${item.total_price.toFixed(2)}` : '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="json-card card">
              <details>
                <summary><FileJson size={16} /> View Raw JSON</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </details>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

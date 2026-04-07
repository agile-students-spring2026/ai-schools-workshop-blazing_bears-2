import { useState, useEffect } from 'react'
import { fetchDistrictRankings } from '../api'
import './DistrictList.css'

export default function DistrictList({ stateCode, onSelectDistrict }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetchDistrictRankings(stateCode)
      .then((result) => {
        setData(result)
        setLoading(false)
      })
      .catch(() => {
        setError('Failed to load districts. Please try again.')
        setLoading(false)
      })
  }, [stateCode])

  if (loading) return <p className="status-msg">Loading districts...</p>
  if (error) return <p className="status-msg error">{error}</p>

  return (
    <div className="district-list">
      <h2>Top Districts in {stateCode}</h2>
      <div className="district-cards">
        {data.districtList.map((d) => {
          const rank = d.rankHistory?.[0]
          return (
            <button
              key={d.districtID}
              className="district-card"
              onClick={() => onSelectDistrict(d.districtID, stateCode)}
            >
              <span className="rank">#{rank?.rank || '—'}</span>
              <div className="district-info">
                <strong>{d.districtName}</strong>
                <span>{d.address.city}, {d.address.state}</span>
                <span>{d.numberTotalSchools} schools</span>
              </div>
              <span className="stars">{'★'.repeat(rank?.rankStars || 0)}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

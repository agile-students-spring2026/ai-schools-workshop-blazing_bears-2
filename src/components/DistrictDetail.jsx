import { useState, useEffect } from 'react'
import { fetchDistrictDetail, fetchSchools } from '../api'
import './DistrictDetail.css'

export default function DistrictDetail({ districtId, stateCode, onBack }) {
  const [district, setDistrict] = useState(null)
  const [schools, setSchools] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    Promise.all([
      fetchDistrictDetail(districtId),
      fetchSchools(stateCode, districtId),
    ])
      .then(([districtData, schoolsData]) => {
        setDistrict(districtData)
        setSchools(schoolsData)
        setLoading(false)
      })
      .catch(() => {
        setError('Failed to load district details.')
        setLoading(false)
      })
  }, [districtId, stateCode])

  if (loading) return <p className="status-msg">Loading district details...</p>
  if (error) return <p className="status-msg error">{error}</p>

  const rank = district.rankHistory?.[0]

  return (
    <div className="district-detail">
      <button className="back-btn" onClick={onBack}>← Back to list</button>
      <h2>{district.districtName}</h2>
      <div className="detail-meta">
        {rank && <span className="stars">{'★'.repeat(rank.rankStars)} Rank #{rank.rank} of {rank.rankOf}</span>}
        <span>Grades {district.lowGrade} - {district.highGrade}</span>
        <span>{district.numberTotalSchools} schools</span>
        <span>{district.phone}</span>
      </div>

      <h3>Schools in this District</h3>
      <div className="school-list">
        {schools.schoolList.map((s) => {
          const sRank = s.rankHistory?.[0]
          return (
            <div key={s.schoolid} className="school-card">
              <div className="school-info">
                <strong>{s.schoolName}</strong>
                <span>{s.schoolLevel} · Grades {s.lowGrade}–{s.highGrade}</span>
              </div>
              {sRank && (
                <span className="school-rank">
                  {'★'.repeat(sRank.rankStars)} #{sRank.rank}
                </span>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

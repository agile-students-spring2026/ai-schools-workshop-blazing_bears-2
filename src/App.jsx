import { useState } from 'react'
import StateSelector from './components/StateSelector'
import DistrictList from './components/DistrictList'
import DistrictDetail from './components/DistrictDetail'
import './App.css'

export default function App() {
  const [stateCode, setStateCode] = useState(null)
  const [selectedDistrict, setSelectedDistrict] = useState(null)

  function handleSelectState(code) {
    setStateCode(code)
    setSelectedDistrict(null)
  }

  function handleSelectDistrict(districtId, stCode) {
    setSelectedDistrict({ districtId, stateCode: stCode })
  }

  function handleBack() {
    setSelectedDistrict(null)
  }

  return (
    <div className="app">
      <h1>School District Evaluator</h1>
      <StateSelector onSelect={handleSelectState} />
      {stateCode && !selectedDistrict && (
        <DistrictList stateCode={stateCode} onSelectDistrict={handleSelectDistrict} />
      )}
      {selectedDistrict && (
        <DistrictDetail
          districtId={selectedDistrict.districtId}
          stateCode={selectedDistrict.stateCode}
          onBack={handleBack}
        />
      )}
    </div>
  )
}

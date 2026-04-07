const BASE_URL = '/api'
const APP_ID = '32e0c2e9'
const APP_KEY = 'fe67cad95da74a892758f35ecdaa46ae'

function authParams() {
  return `appID=${APP_ID}&appKey=${APP_KEY}`
}

export async function fetchDistrictRankings(stateCode) {
  const res = await fetch(
    `${BASE_URL}/v2.3/rankings/districts/${stateCode}?${authParams()}&perPage=20`
  )
  if (!res.ok) throw new Error('API request failed')
  return res.json()
}

export async function fetchDistrictDetail(districtId) {
  const res = await fetch(
    `${BASE_URL}/v2.3/districts/${districtId}?${authParams()}`
  )
  if (!res.ok) throw new Error('API request failed')
  return res.json()
}

export async function fetchSchools(stateCode, districtId) {
  const res = await fetch(
    `${BASE_URL}/v2.3/schools?st=${stateCode}&districtID=${districtId}&${authParams()}&perPage=30`
  )
  if (!res.ok) throw new Error('API request failed')
  return res.json()
}

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchDistrictRankings, fetchDistrictDetail, fetchSchools } from '../api'

const mockFetch = vi.fn()
global.fetch = mockFetch

beforeEach(() => {
  mockFetch.mockReset()
})

describe('fetchDistrictRankings', () => {
  it('fetches district rankings for a state', async () => {
    const mockData = {
      districtList: [{ districtID: '1', districtName: 'Test District' }],
      numberOfDistricts: 1,
    }
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    })

    const result = await fetchDistrictRankings('NY')

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/v2.3/rankings/districts/NY')
    )
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('appID=32e0c2e9')
    )
    expect(result).toEqual(mockData)
  })

  it('throws on failed request', async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 500 })
    await expect(fetchDistrictRankings('NY')).rejects.toThrow('API request failed')
  })
})

describe('fetchDistrictDetail', () => {
  it('fetches detail for a district', async () => {
    const mockData = { districtID: '3601120', districtName: 'Test' }
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    })

    const result = await fetchDistrictDetail('3601120')

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/v2.3/districts/3601120')
    )
    expect(result).toEqual(mockData)
  })

  it('throws on failed request', async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 404 })
    await expect(fetchDistrictDetail('bad')).rejects.toThrow('API request failed')
  })
})

describe('fetchSchools', () => {
  it('fetches schools for a district in a state', async () => {
    const mockData = {
      schoolList: [{ schoolid: '1', schoolName: 'Test School' }],
    }
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    })

    const result = await fetchSchools('NY', '3601120')

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/v2.3/schools')
    )
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('st=NY')
    )
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('districtID=3601120')
    )
    expect(result).toEqual(mockData)
  })

  it('throws on failed request', async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 500 })
    await expect(fetchSchools('NY', 'bad')).rejects.toThrow('API request failed')
  })
})

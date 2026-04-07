import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import DistrictList from '../components/DistrictList'
import * as api from '../api'

vi.mock('../api')

const mockRankingsData = {
  districtList: [
    {
      districtID: '3601120',
      districtName: 'Test District One',
      address: { city: 'Bronx', state: 'NY' },
      rankHistory: [{ year: 2025, rank: 1, rankOf: 874, rankStars: 5 }],
      numberTotalSchools: 3,
    },
    {
      districtID: '3600001',
      districtName: 'Test District Two',
      address: { city: 'Albany', state: 'NY' },
      rankHistory: [{ year: 2025, rank: 2, rankOf: 874, rankStars: 4 }],
      numberTotalSchools: 12,
    },
  ],
  numberOfDistricts: 2,
}

describe('DistrictList', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('shows loading state initially', () => {
    api.fetchDistrictRankings.mockReturnValue(new Promise(() => {}))
    render(<DistrictList stateCode="NY" onSelectDistrict={vi.fn()} />)
    expect(screen.getByText('Loading districts...')).toBeInTheDocument()
  })

  it('renders district rankings after loading', async () => {
    api.fetchDistrictRankings.mockResolvedValue(mockRankingsData)
    render(<DistrictList stateCode="NY" onSelectDistrict={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('Test District One')).toBeInTheDocument()
    })
    expect(screen.getByText('Test District Two')).toBeInTheDocument()
  })

  it('calls onSelectDistrict when a district is clicked', async () => {
    const user = userEvent.setup()
    api.fetchDistrictRankings.mockResolvedValue(mockRankingsData)
    const onSelectDistrict = vi.fn()
    render(<DistrictList stateCode="NY" onSelectDistrict={onSelectDistrict} />)

    await waitFor(() => {
      expect(screen.getByText('Test District One')).toBeInTheDocument()
    })

    await user.click(screen.getByText('Test District One'))
    expect(onSelectDistrict).toHaveBeenCalledWith('3601120', 'NY')
  })

  it('shows error message on API failure', async () => {
    api.fetchDistrictRankings.mockRejectedValue(new Error('API request failed'))
    render(<DistrictList stateCode="NY" onSelectDistrict={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('Failed to load districts. Please try again.')).toBeInTheDocument()
    })
  })
})

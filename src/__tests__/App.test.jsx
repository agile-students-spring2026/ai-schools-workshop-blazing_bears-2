import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from '../App'
import * as api from '../api'

vi.mock('../api')

const mockRankingsData = {
  districtList: [
    {
      districtID: '3601120',
      districtName: 'Top District',
      address: { city: 'Bronx', state: 'NY' },
      rankHistory: [{ year: 2025, rank: 1, rankOf: 874, rankStars: 5 }],
      numberTotalSchools: 3,
    },
  ],
  numberOfDistricts: 1,
}

const mockDistrict = {
  districtID: '3601120',
  districtName: 'Top District',
  phone: '(555) 999-0000',
  address: { city: 'Bronx', state: 'NY', street: '1 Main', zip: '10001' },
  lowGrade: 'K',
  highGrade: '8',
  numberTotalSchools: 3,
  rankHistory: [{ year: 2025, rank: 1, rankOf: 874, rankStars: 5 }],
}

const mockSchools = {
  schoolList: [
    {
      schoolid: '1',
      schoolName: 'Best Elementary',
      schoolLevel: 'Elementary',
      lowGrade: 'K',
      highGrade: '5',
      rankHistory: [{ year: 2025, rank: 1, rankOf: 500, rankStars: 5 }],
    },
  ],
}

describe('App', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders the title and state selector', () => {
    render(<App />)
    expect(screen.getByText('School District Evaluator')).toBeInTheDocument()
    expect(screen.getByRole('combobox')).toBeInTheDocument()
  })

  it('shows district list after selecting a state', async () => {
    const user = userEvent.setup()
    api.fetchDistrictRankings.mockResolvedValue(mockRankingsData)
    render(<App />)

    await user.selectOptions(screen.getByRole('combobox'), 'NY')

    await waitFor(() => {
      expect(screen.getByText('Top District')).toBeInTheDocument()
    })
  })

  it('shows district detail after clicking a district', async () => {
    const user = userEvent.setup()
    api.fetchDistrictRankings.mockResolvedValue(mockRankingsData)
    api.fetchDistrictDetail.mockResolvedValue(mockDistrict)
    api.fetchSchools.mockResolvedValue(mockSchools)
    render(<App />)

    await user.selectOptions(screen.getByRole('combobox'), 'NY')
    await waitFor(() => {
      expect(screen.getByText('Top District')).toBeInTheDocument()
    })

    await user.click(screen.getByText('Top District'))
    await waitFor(() => {
      expect(screen.getByText('Best Elementary')).toBeInTheDocument()
    })
  })

  it('goes back to district list from detail view', async () => {
    const user = userEvent.setup()
    api.fetchDistrictRankings.mockResolvedValue(mockRankingsData)
    api.fetchDistrictDetail.mockResolvedValue(mockDistrict)
    api.fetchSchools.mockResolvedValue(mockSchools)
    render(<App />)

    await user.selectOptions(screen.getByRole('combobox'), 'NY')
    await waitFor(() => {
      expect(screen.getByText('Top District')).toBeInTheDocument()
    })

    await user.click(screen.getByText('Top District'))
    await waitFor(() => {
      expect(screen.getByText('Best Elementary')).toBeInTheDocument()
    })

    // Re-mock rankings for when we go back
    api.fetchDistrictRankings.mockResolvedValue(mockRankingsData)
    await user.click(screen.getByRole('button', { name: /back/i }))
    await waitFor(() => {
      expect(screen.getByText('Top District')).toBeInTheDocument()
    })
  })
})

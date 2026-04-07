import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import DistrictDetail from '../components/DistrictDetail'
import * as api from '../api'

vi.mock('../api')

const mockDistrict = {
  districtID: '3601120',
  districtName: 'Test District',
  phone: '(555) 123-4567',
  address: { city: 'Bronx', state: 'NY', street: '123 Main St', zip: '10473' },
  lowGrade: 'K',
  highGrade: '12',
  numberTotalSchools: 5,
  rankHistory: [{ year: 2025, rank: 1, rankOf: 874, rankStars: 5 }],
}

const mockSchools = {
  schoolList: [
    {
      schoolid: '1',
      schoolName: 'School A',
      schoolLevel: 'Elementary',
      lowGrade: 'K',
      highGrade: '5',
      rankHistory: [{ year: 2025, rank: 10, rankOf: 2000, rankStars: 4 }],
    },
    {
      schoolid: '2',
      schoolName: 'School B',
      schoolLevel: 'High',
      lowGrade: '9',
      highGrade: '12',
      rankHistory: [{ year: 2025, rank: 50, rankOf: 1000, rankStars: 3 }],
    },
  ],
}

describe('DistrictDetail', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('shows loading state initially', () => {
    api.fetchDistrictDetail.mockReturnValue(new Promise(() => {}))
    api.fetchSchools.mockReturnValue(new Promise(() => {}))
    render(<DistrictDetail districtId="3601120" stateCode="NY" onBack={vi.fn()} />)
    expect(screen.getByText('Loading district details...')).toBeInTheDocument()
  })

  it('renders district detail and schools after loading', async () => {
    api.fetchDistrictDetail.mockResolvedValue(mockDistrict)
    api.fetchSchools.mockResolvedValue(mockSchools)
    render(<DistrictDetail districtId="3601120" stateCode="NY" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('Test District')).toBeInTheDocument()
    })
    expect(screen.getByText('School A')).toBeInTheDocument()
    expect(screen.getByText('School B')).toBeInTheDocument()
  })

  it('shows district info fields', async () => {
    api.fetchDistrictDetail.mockResolvedValue(mockDistrict)
    api.fetchSchools.mockResolvedValue(mockSchools)
    render(<DistrictDetail districtId="3601120" stateCode="NY" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('(555) 123-4567')).toBeInTheDocument()
    })
    expect(screen.getByText('Grades K - 12')).toBeInTheDocument()
    expect(screen.getByText('5 schools')).toBeInTheDocument()
  })

  it('calls onBack when back button is clicked', async () => {
    const user = userEvent.setup()
    api.fetchDistrictDetail.mockResolvedValue(mockDistrict)
    api.fetchSchools.mockResolvedValue(mockSchools)
    const onBack = vi.fn()
    render(<DistrictDetail districtId="3601120" stateCode="NY" onBack={onBack} />)

    await waitFor(() => {
      expect(screen.getByText('Test District')).toBeInTheDocument()
    })

    await user.click(screen.getByRole('button', { name: /back/i }))
    expect(onBack).toHaveBeenCalled()
  })

  it('shows error message on API failure', async () => {
    api.fetchDistrictDetail.mockRejectedValue(new Error('fail'))
    api.fetchSchools.mockRejectedValue(new Error('fail'))
    render(<DistrictDetail districtId="3601120" stateCode="NY" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('Failed to load district details.')).toBeInTheDocument()
    })
  })
})

# School District Evaluator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a React app that lets users select a US state, view ranked school districts, and drill into district details with schools.

**Architecture:** Vite + React SPA. An `api.js` module handles all SchoolDigger API calls. Three views: state selector → district rankings list → district detail with schools. All API calls mocked in tests via `vi.mock`.

**Tech Stack:** React 18, Vite, Vitest, React Testing Library, plain CSS

---

## File Structure

```
src/
  main.jsx              — App entry point, renders <App />
  App.jsx               — Router: manages current view state
  App.css               — Global styles
  api.js                — All SchoolDigger API fetch functions
  components/
    StateSelector.jsx   — Dropdown to pick a state
    StateSelector.css
    DistrictList.jsx    — Shows ranked districts for selected state
    DistrictList.css
    DistrictDetail.jsx  — Shows district info + schools list
    DistrictDetail.css
  __tests__/
    api.test.js
    App.test.jsx
    StateSelector.test.jsx
    DistrictList.test.jsx
    DistrictDetail.test.jsx
index.html
vite.config.js
package.json
```

---

### Task 1: Project Scaffold

**Files:**
- Create: `package.json`, `vite.config.js`, `index.html`, `src/main.jsx`, `src/App.jsx`, `src/App.css`

- [ ] **Step 1: Initialize Vite React project**

```bash
cd /Users/xinchen/Desktop/Code/ai-schools-workshop-blazing_bears-2
npm create vite@latest . -- --template react
```

If prompted about existing files, select "Ignore files and continue". This scaffolds the project.

- [ ] **Step 2: Install dependencies**

```bash
npm install
```

- [ ] **Step 3: Install test dependencies**

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

- [ ] **Step 4: Configure Vitest in vite.config.js**

Replace `vite.config.js` with:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/**/*.{js,jsx}'],
      exclude: ['src/main.jsx', 'src/setupTests.js'],
    },
  },
})
```

- [ ] **Step 5: Create test setup file**

Create `src/setupTests.js`:

```js
import '@testing-library/jest-dom'
```

- [ ] **Step 6: Add test scripts to package.json**

Add to `"scripts"` in `package.json`:

```json
"test": "vitest run",
"test:watch": "vitest",
"coverage": "vitest run --coverage"
```

- [ ] **Step 7: Verify dev server starts**

```bash
npm run dev
```

Expected: Vite dev server starts on localhost. Kill it after confirming.

- [ ] **Step 8: Commit**

```bash
git add package.json package-lock.json vite.config.js index.html src/ .gitignore
git commit -m "chore: scaffold Vite React project with Vitest"
```

---

### Task 2: API Module

**Files:**
- Create: `src/api.js`, `src/__tests__/api.test.js`

- [ ] **Step 1: Write failing tests for api module**

Create `src/__tests__/api.test.js`:

```js
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx vitest run src/__tests__/api.test.js
```

Expected: FAIL — module `../api` not found.

- [ ] **Step 3: Implement api.js**

Create `src/api.js`:

```js
const BASE_URL = 'https://api.schooldigger.com'
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx vitest run src/__tests__/api.test.js
```

Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/api.js src/__tests__/api.test.js
git commit -m "feat: add SchoolDigger API module with tests"
```

---

### Task 3: StateSelector Component

**Files:**
- Create: `src/components/StateSelector.jsx`, `src/components/StateSelector.css`, `src/__tests__/StateSelector.test.jsx`

- [ ] **Step 1: Write failing tests**

Create `src/__tests__/StateSelector.test.jsx`:

```jsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import StateSelector from '../components/StateSelector'

describe('StateSelector', () => {
  it('renders a select dropdown with all 50 states', () => {
    render(<StateSelector onSelect={vi.fn()} />)
    const select = screen.getByRole('combobox')
    expect(select).toBeInTheDocument()
    // 50 states + 1 placeholder option
    const options = screen.getAllByRole('option')
    expect(options.length).toBe(51)
  })

  it('shows placeholder text by default', () => {
    render(<StateSelector onSelect={vi.fn()} />)
    expect(screen.getByRole('option', { name: 'Select a state...' })).toBeInTheDocument()
  })

  it('calls onSelect when a state is chosen', async () => {
    const user = userEvent.setup()
    const onSelect = vi.fn()
    render(<StateSelector onSelect={onSelect} />)

    await user.selectOptions(screen.getByRole('combobox'), 'NY')
    expect(onSelect).toHaveBeenCalledWith('NY')
  })
})
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx vitest run src/__tests__/StateSelector.test.jsx
```

Expected: FAIL — module not found.

- [ ] **Step 3: Implement StateSelector**

Create `src/components/StateSelector.jsx`:

```jsx
const STATES = [
  { code: 'AL', name: 'Alabama' }, { code: 'AK', name: 'Alaska' },
  { code: 'AZ', name: 'Arizona' }, { code: 'AR', name: 'Arkansas' },
  { code: 'CA', name: 'California' }, { code: 'CO', name: 'Colorado' },
  { code: 'CT', name: 'Connecticut' }, { code: 'DE', name: 'Delaware' },
  { code: 'FL', name: 'Florida' }, { code: 'GA', name: 'Georgia' },
  { code: 'HI', name: 'Hawaii' }, { code: 'ID', name: 'Idaho' },
  { code: 'IL', name: 'Illinois' }, { code: 'IN', name: 'Indiana' },
  { code: 'IA', name: 'Iowa' }, { code: 'KS', name: 'Kansas' },
  { code: 'KY', name: 'Kentucky' }, { code: 'LA', name: 'Louisiana' },
  { code: 'ME', name: 'Maine' }, { code: 'MD', name: 'Maryland' },
  { code: 'MA', name: 'Massachusetts' }, { code: 'MI', name: 'Michigan' },
  { code: 'MN', name: 'Minnesota' }, { code: 'MS', name: 'Mississippi' },
  { code: 'MO', name: 'Missouri' }, { code: 'MT', name: 'Montana' },
  { code: 'NE', name: 'Nebraska' }, { code: 'NV', name: 'Nevada' },
  { code: 'NH', name: 'New Hampshire' }, { code: 'NJ', name: 'New Jersey' },
  { code: 'NM', name: 'New Mexico' }, { code: 'NY', name: 'New York' },
  { code: 'NC', name: 'North Carolina' }, { code: 'ND', name: 'North Dakota' },
  { code: 'OH', name: 'Ohio' }, { code: 'OK', name: 'Oklahoma' },
  { code: 'OR', name: 'Oregon' }, { code: 'PA', name: 'Pennsylvania' },
  { code: 'RI', name: 'Rhode Island' }, { code: 'SC', name: 'South Carolina' },
  { code: 'SD', name: 'South Dakota' }, { code: 'TN', name: 'Tennessee' },
  { code: 'TX', name: 'Texas' }, { code: 'UT', name: 'Utah' },
  { code: 'VT', name: 'Vermont' }, { code: 'VA', name: 'Virginia' },
  { code: 'WA', name: 'Washington' }, { code: 'WV', name: 'West Virginia' },
  { code: 'WI', name: 'Wisconsin' }, { code: 'WY', name: 'Wyoming' },
]

import './StateSelector.css'

export default function StateSelector({ onSelect }) {
  return (
    <div className="state-selector">
      <label htmlFor="state-select">Choose a state to explore districts:</label>
      <select
        id="state-select"
        defaultValue=""
        onChange={(e) => onSelect(e.target.value)}
      >
        <option value="" disabled>Select a state...</option>
        {STATES.map((s) => (
          <option key={s.code} value={s.code}>{s.name}</option>
        ))}
      </select>
    </div>
  )
}
```

Create `src/components/StateSelector.css`:

```css
.state-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  margin: 2rem 0;
}

.state-selector label {
  font-size: 1.1rem;
  font-weight: 500;
}

.state-selector select {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  min-width: 250px;
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx vitest run src/__tests__/StateSelector.test.jsx
```

Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/StateSelector.jsx src/components/StateSelector.css src/__tests__/StateSelector.test.jsx
git commit -m "feat: add StateSelector component with tests"
```

---

### Task 4: DistrictList Component

**Files:**
- Create: `src/components/DistrictList.jsx`, `src/components/DistrictList.css`, `src/__tests__/DistrictList.test.jsx`

- [ ] **Step 1: Write failing tests**

Create `src/__tests__/DistrictList.test.jsx`:

```jsx
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx vitest run src/__tests__/DistrictList.test.jsx
```

Expected: FAIL — module not found.

- [ ] **Step 3: Implement DistrictList**

Create `src/components/DistrictList.jsx`:

```jsx
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
```

Create `src/components/DistrictList.css`:

```css
.district-list {
  max-width: 700px;
  margin: 0 auto;
}

.district-list h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.district-cards {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.district-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  text-align: left;
  font: inherit;
  width: 100%;
}

.district-card:hover {
  background: #f0f4ff;
  border-color: #99b;
}

.rank {
  font-size: 1.3rem;
  font-weight: 700;
  color: #336;
  min-width: 3rem;
  text-align: center;
}

.district-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.district-info span {
  font-size: 0.85rem;
  color: #666;
}

.stars {
  color: #f5a623;
  font-size: 1.1rem;
}

.status-msg {
  text-align: center;
  padding: 2rem;
  color: #555;
}

.status-msg.error {
  color: #c00;
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx vitest run src/__tests__/DistrictList.test.jsx
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/DistrictList.jsx src/components/DistrictList.css src/__tests__/DistrictList.test.jsx
git commit -m "feat: add DistrictList component with tests"
```

---

### Task 5: DistrictDetail Component

**Files:**
- Create: `src/components/DistrictDetail.jsx`, `src/components/DistrictDetail.css`, `src/__tests__/DistrictDetail.test.jsx`

- [ ] **Step 1: Write failing tests**

Create `src/__tests__/DistrictDetail.test.jsx`:

```jsx
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx vitest run src/__tests__/DistrictDetail.test.jsx
```

Expected: FAIL — module not found.

- [ ] **Step 3: Implement DistrictDetail**

Create `src/components/DistrictDetail.jsx`:

```jsx
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
```

Create `src/components/DistrictDetail.css`:

```css
.district-detail {
  max-width: 700px;
  margin: 0 auto;
}

.back-btn {
  background: none;
  border: none;
  color: #336;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
}

.back-btn:hover {
  text-decoration: underline;
}

.district-detail h2 {
  margin-bottom: 0.5rem;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  color: #555;
}

.detail-meta .stars {
  color: #f5a623;
}

.school-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.school-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fff;
}

.school-info {
  display: flex;
  flex-direction: column;
}

.school-info span {
  font-size: 0.85rem;
  color: #666;
}

.school-rank {
  color: #f5a623;
  white-space: nowrap;
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx vitest run src/__tests__/DistrictDetail.test.jsx
```

Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/DistrictDetail.jsx src/components/DistrictDetail.css src/__tests__/DistrictDetail.test.jsx
git commit -m "feat: add DistrictDetail component with tests"
```

---

### Task 6: App Component (Router)

**Files:**
- Modify: `src/App.jsx`
- Modify: `src/App.css`
- Create: `src/__tests__/App.test.jsx`

- [ ] **Step 1: Write failing tests**

Create `src/__tests__/App.test.jsx`:

```jsx
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
npx vitest run src/__tests__/App.test.jsx
```

Expected: FAIL — App doesn't render expected content.

- [ ] **Step 3: Implement App.jsx**

Replace `src/App.jsx` with:

```jsx
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
```

Replace `src/App.css` with:

```css
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #222;
}

.app h1 {
  text-align: center;
  color: #224;
  margin-bottom: 0;
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
npx vitest run src/__tests__/App.test.jsx
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Run full test suite with coverage**

```bash
npx vitest run --coverage
```

Expected: All tests PASS, coverage at or near 100% for all files in `src/` (excluding `main.jsx`).

- [ ] **Step 6: Commit**

```bash
git add src/App.jsx src/App.css src/__tests__/App.test.jsx
git commit -m "feat: wire up App with state routing and full test coverage"
```

---

### Task 7: Final Cleanup and Deploy

**Files:**
- Modify: `index.html` (set title)
- Modify: `.gitignore` (add `dist/`)

- [ ] **Step 1: Update index.html title**

In `index.html`, change the `<title>` tag to:

```html
<title>School District Evaluator</title>
```

- [ ] **Step 2: Verify full build works**

```bash
npm run build
```

Expected: Build succeeds, output in `dist/`.

- [ ] **Step 3: Verify all tests pass with coverage**

```bash
npx vitest run --coverage
```

Expected: 100% coverage on all source files.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "chore: update page title and finalize for deploy"
```

- [ ] **Step 5: Deploy to Vercel**

```bash
npx vercel --prod
```

Follow prompts. Expected: App is live at a Vercel URL.

- [ ] **Step 6: Record the deployment URL in README.md**

Update `README.md` with the live URL.

```bash
git add README.md
git commit -m "docs: add deployment URL to README"
```

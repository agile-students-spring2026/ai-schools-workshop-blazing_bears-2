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

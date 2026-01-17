import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Statistics } from './Statistics';
import { Haircut } from '../types';

const mockHaircuts: Haircut[] = [
  { id: '1', name: 'Corte', price: 1500, date: '2026-01-17' },
  { id: '2', name: 'Corte', price: 1500, date: '2026-01-17' },
  { id: '3', name: 'Barba', price: 1000, date: '2026-01-17' },
  { id: '4', name: 'Corte y Barba', price: 2200, date: '2026-01-16' },
  { id: '5', name: 'Corte', price: 1500, date: '2026-01-15' },
  { id: '6', name: 'Barba', price: 1000, date: '2026-01-15' },
];

describe('Statistics Component', () => {
  beforeEach(() => {
    render(<Statistics haircuts={mockHaircuts} />);
  });

  it('renders summary statistics', () => {
    expect(screen.getByText('Total Ingresos')).toBeInTheDocument();
    expect(screen.getByText('Total Cortes')).toBeInTheDocument();
    expect(screen.getByText('Promedio Diario')).toBeInTheDocument();
    expect(screen.getByText('Servicio Popular')).toBeInTheDocument();
  });

  it('displays total haircut count', () => {
    expect(screen.getByText(mockHaircuts.length.toString())).toBeInTheDocument();
  });

  it('renders chart cards', () => {
    expect(screen.getByText('Ingresos Ultimos 7 Dias')).toBeInTheDocument();
    expect(screen.getByText('Cantidad de Cortes por Dia')).toBeInTheDocument();
    expect(screen.getByText('Distribucion por Servicio')).toBeInTheDocument();
    expect(screen.getByText('Cortes por Dia')).toBeInTheDocument();
  });

  it('renders service table', () => {
    expect(screen.getByText('Detalle por Servicio')).toBeInTheDocument();
    expect(screen.getByText('Servicio')).toBeInTheDocument();
    expect(screen.getByText('Cantidad')).toBeInTheDocument();
    expect(screen.getByText('Ingresos')).toBeInTheDocument();
    expect(screen.getByText('Participacion')).toBeInTheDocument();
  });

  it('renders revenue values', () => {
    const revenueElements = screen.getAllByText(/\$/);
    expect(revenueElements.length).toBeGreaterThan(0);
  });
});

describe('Statistics with empty data', () => {
  it('handles empty haircuts array', () => {
    render(<Statistics haircuts={[]} />);
    expect(screen.getByText('Total Ingresos')).toBeInTheDocument();
    expect(screen.getByText('0')).toBeInTheDocument();
  });
});

describe('Statistics service distribution', () => {
  it('shows all services in table', () => {
    render(<Statistics haircuts={mockHaircuts} />);
    const table = screen.getByRole('table');
    expect(table).toBeInTheDocument();
    expect(screen.getByText('Corte', { selector: 'td' })).toBeInTheDocument();
    expect(screen.getByText('Barba', { selector: 'td' })).toBeInTheDocument();
    expect(screen.getByText('Corte y Barba', { selector: 'td' })).toBeInTheDocument();
  });
});

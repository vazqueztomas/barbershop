import React from 'react';
import { HaircutCreate } from '../types';

interface HaircutFormProps {
  onSubmit: (haircut: HaircutCreate) => void;
  initialData?: HaircutCreate;
  onCancel?: () => void;
}

export function HaircutForm({ onSubmit, initialData, onCancel }: HaircutFormProps) {
  const today = new Date().toISOString().split('T')[0];
  const [formData, setFormData] = React.useState<HaircutCreate>({
    clientName: initialData?.clientName || '',
    serviceName: initialData?.serviceName || '',
    price: initialData?.price ?? 0,
    date: initialData?.date || today,
    time: initialData?.time || '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'price' ? (value === '' ? 0 : parseFloat(value)) : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // No enviar el campo time si está vacío
    const submitData = { ...formData };
    if (!submitData.time || submitData.time.trim() === '') {
      delete submitData.time;
    }
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="haircut-form">
      <div className="form-group">
        <label htmlFor="clientName">Nombre del cliente:</label>
        <input
          type="text"
          id="clientName"
          name="clientName"
          value={formData.clientName}
          onChange={handleChange}
          placeholder="Ej: Juan Pérez"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="serviceName">Servicio:</label>
        <input
          type="text"
          id="serviceName"
          name="serviceName"
          value={formData.serviceName}
          onChange={handleChange}
          placeholder="Ej: Degradado, Clásico, etc."
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="time">Hora (opcional):</label>
        <input
          type="time"
          id="time"
          name="time"
          value={formData.time || ''}
          onChange={handleChange}
        />
      </div>
      <div className="form-group">
        <label htmlFor="price">Precio (ARS):</label>
        <input
          type="number"
          id="price"
          name="price"
          value={formData.price || ''}
          onChange={handleChange}
          step="0.01"
          min="0"
          placeholder="0.00"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="date">Fecha:</label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          max={today}
          required
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="submit-btn">
          {initialData ? 'Actualizar' : 'Crear'}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="cancel-btn">
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}

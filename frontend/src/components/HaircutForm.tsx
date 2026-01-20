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
    const submitData = { ...formData };
    if (!submitData.time || submitData.time.trim() === '') {
      delete submitData.time;
    }
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <div>
          <label htmlFor="clientName" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Cliente
          </label>
          <input
            type="text"
            id="clientName"
            name="clientName"
            value={formData.clientName}
            onChange={handleChange}
            placeholder="Nombre del cliente"
            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all duration-200"
            required
          />
        </div>
        <div>
          <label htmlFor="serviceName" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Servicio
          </label>
          <input
            type="text"
            id="serviceName"
            name="serviceName"
            value={formData.serviceName}
            onChange={handleChange}
            placeholder="Ej: Degradado, Clásico"
            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all duration-200"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <div>
          <label htmlFor="price" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Precio (ARS)
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price || ''}
            onChange={handleChange}
            step="0.01"
            min="0"
            placeholder="0"
            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all duration-200"
            required
          />
        </div>
        <div>
          <label htmlFor="date" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Fecha
          </label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            max={today}
            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all duration-200"
            required
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <div>
          <label htmlFor="time" className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
            Hora (opcional)
          </label>
          <input
            type="time"
            id="time"
            name="time"
            value={formData.time || ''}
            onChange={handleChange}
            className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition-all duration-200"
          />
        </div>
      </div>

      <div className="flex flex-wrap gap-4 pt-2">
        <button
          type="submit"
          className="px-6 py-2.5 bg-gray-900 hover:bg-gray-800 text-white rounded-lg text-sm font-medium transition-all duration-200 shadow-sm hover:shadow-md"
        >
          {initialData ? 'Actualizar' : 'Crear'}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-all duration-200"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}

import React from 'react';

interface PriceEditorProps {
  currentPrice: number;
  newPrice: string;
  onNewPriceChange: (price: string) => void;
  onSave: () => void;
  onCancel: () => void;
}

export function PriceEditor({
  currentPrice,
  newPrice,
  onNewPriceChange,
  onSave,
  onCancel,
}: PriceEditorProps) {
  const formatCurrency = (amount: number) => {
    if (isNaN(amount) || amount === null || amount === undefined) {
      return '$0,00';
    }
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
    }).format(amount);
  };

  return (
    <div className="price-editor">
      <div className="price-editor-content">
        <h4>Modificar Precio</h4>
        <p>Precio actual: {formatCurrency(currentPrice)}</p>
        <div className="price-input-group">
          <label>Nuevo precio (ARS):</label>
          <input
            type="number"
            value={newPrice}
            onChange={(e) => onNewPriceChange(e.target.value)}
            step="100"
            min="0"
            autoFocus
          />
        </div>
        <div className="price-editor-actions">
          <button onClick={onSave} className="save-btn">
            Guardar
          </button>
          <button onClick={onCancel} className="cancel-btn">
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
}
